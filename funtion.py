import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
drawing=False
class SeamCarving:
    def __init__(self,QT,filename,height_new=0,width_new=0,is_remove_object=False):
        self.QT=QT
        self.filename=filename
        self.height_new=height_new
        self.width_new=width_new
        self.is_remove_object=is_remove_object

        self.image_input=cv2.imread(self.filename)
        self.image_temp=self.image_input.copy()
        self.height_org,self.width_org=self.image_input.shape[:2]
        self.image_process=self.image_input.copy()
        self.seams_record=[]
        self.rect_object=(0,0,0,0)
        self.processbar_total=0
        self.processbar_check=0
        if(self.is_remove_object==True):
            cv2.namedWindow('image')
            cv2.setMouseCallback('image',self.draw_Object)
            while(1):
                cv2.imshow('image',self.image_input)
                k = cv2.waitKey(1) & 0xFF
                if k == ord('m'):
                    mode = not mode
                elif k == 27:
                    break
            cv2.destroyAllWindows()
        elif(abs(self.height_org-self.height_new)!=0 or abs(self.width_org-self.width_new)!=0):
            self.resize_image()
            pass
        else:
            pass
        cv2.imwrite('output\\image_output.jpg',self.image_process)
        self.QT.progressBar.setProperty("value",100)
    def resize_image(self):
        seams_col,seams_height = self.width_new-self.width_org,self.height_new-self.height_org
        self.processbar_total=abs(seams_col)+abs(seams_height)
        self.QT.text_process.append(str(seams_height)+" "+str(seams_col))
        print(str(seams_height)+" "+str(seams_col))
        
        if(seams_col < 0):
            self.reduce_image(abs(seams_col))
            self.image_temp=self.image_process
        else:
            self.expand_image(abs(seams_col))
            self.image_temp=self.image_process
        if(seams_height != 0):
            self.image_process = self.rotate_image(self.image_process, 1)
            self.image_temp = self.rotate_image(self.image_temp, 1)
            if(seams_height < 0):
                self.reduce_image(abs(seams_height))
                self.image_temp=self.image_process
            else:
                self.expand_image(abs(seams_height))
                self.image_temp=self.image_process
            self.image_process = self.rotate_image(self.image_process, 0)
            self.image_temp = self.rotate_image(self.image_temp, 0)

    def reduce_image(self,num_seams,is_remove_object=False):
        if(is_remove_object==False):
            energy=self.calculate_Enery()
            
        else:
            energy=self.calculate_Enery_Custom()
        self.energy_temp=energy.copy()
        cv2.imwrite("output\\Energy.jpg",energy)
        
        self.seams_record=[]
        img_seam=self.image_temp.copy()
        # Reduce image
        for i in range(num_seams):
            # self.QT.text_process.append(str(self.image_process.shape[:2]))
            
            seam = self.find_seam(self.image_process,energy)
            self.seams_record.append(seam)
            img_seam = self.draw_seam_old(img_seam,seam)
            self.image_process=self.delete_seam(self.image_process,seam)
            if(is_remove_object==False):
                energy=self.calculate_Enery()
            else:
                energy=self.calculate_Enery_Custom(i)
            self.QT.text_process.append("Delete Seam "+ str(i+1))
            print("Delete Seam "+ str(i+1))
            
            self.processbar_check+=1
            self.QT.progressBar.setProperty("value", (self.processbar_check/self.processbar_total)*100)
        # seams_record_temp= self.seams_record.copy()
        # image_process_temp=self.image_process.copy()
        # for i in range(len(self.seams_record)):
        #     seam = seams_record_temp.pop()
        #     image_process_temp = draw_seam2(image_process_temp,seam)
    def expand_image(self,num_seams):
        #Expand image
        self.reduce_image(num_seams)
        self.image_process=self.image_temp.copy()
        for i in range(len(self.seams_record)):
            seam = self.seams_record.pop(0)
            self.image_process=self.add_seam(self.image_process,seam,i)
            # self.seams_record = self.update_seams(self.seams_record, seam)
            print("Add Seam "+ str(i+1))
    def draw_Object(self,event,x,y,flags,param):
        global ix,iy,drawing
        clone=self.image_input.copy()

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix,iy = x,y

        elif event == cv2.EVENT_MOUSEMOVE: 
            if drawing: 
                self.image_input[iy:y, ix:x] = clone[iy:y, ix:x] 
                cv2.rectangle(self.image_input,(ix,iy),(x,y),(0,255,0),2)

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            self.image_input[0:self.height_org, 0:self.width_org] = clone[0:self.height_org, 0:self.width_org] 
            cv2.rectangle(self.image_input,(ix,iy),(x,y),(0,255,0),2)
            self.rect_object=(ix,iy,x-ix,y-iy)
            cv2.imwrite('output\\mask_Object.jpg',self.image_input)
            self.remove_Object()
    def remove_Object(self):
        self.image_input=self.image_temp.copy()
        x,y,w,h=self.rect_object
        num_seams=w + 10
        self.processbar_total=num_seams*2
        self.reduce_image(num_seams,self.is_remove_object)
        self.image_temp=self.image_process.copy()
        self.expand_image(num_seams)
        self.QT.text_process.append('Nhan phim bat ky de tiep tuc')
    def rotate_image(self, image, ccw):
        m, n, ch = image.shape
        output = np.zeros((n, m, ch), dtype=np.uint8)
        if ccw:
            image_flip = np.fliplr(image)
            for c in range(ch):
                for row in range(m):
                    output[:, row, c] = image_flip[row, :, c]
        else:
            for c in range(ch):
                for row in range(m):
                    output[:, m - 1 - row, c] = image[row, :, c]
        return output
    def calculate_Enery(self):

        # Convert img to grayscale
        gray = cv2.cvtColor(self.image_process, cv2.COLOR_BGR2GRAY) 
        # Find sobel_x and _y 
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3) 
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3) 
        # sobel_x = cv2.Scharr(gray, cv2.CV_64F, 1, 0) 
        # sobel_y = cv2.Scharr(gray, cv2.CV_64F, 0, 1) 
        abs_sobel_x = cv2.convertScaleAbs(sobel_x) 
        abs_sobel_y = cv2.convertScaleAbs(sobel_y) 
        return cv2.addWeighted(abs_sobel_x, 0.5, abs_sobel_y, 0.5, 0)
    def calculate_Enery_Custom(self,subnum=0):
        x,y,w,h=self.rect_object
        energy=self.calculate_Enery().astype(np.float64)
        energy[y:y+h,x:x+w-subnum]=-100
        return energy
    def find_seam(self,img,energy):

        rows,cols=img.shape[:2]
        # Create array index seam
        seam = np.zeros(img.shape[0]) 
        # Dist_to is matrix use Dynamic Programming to find Seam
        dist_to = np.zeros(img.shape[:2]) + float('inf')
        dist_to[0,:] = np.zeros(img.shape[1]) 
        # edge_to use to reverse index seam
        edge_to = np.zeros(img.shape[:2]) 
        for row in range(rows-1):
            for col in range(cols):
                if(col!=0 and dist_to[row+1,col-1]>dist_to[row][col]+energy[row+1,col-1]):
                    dist_to[row+1,col-1]=dist_to[row][col]+energy[row+1,col-1]
                    edge_to[row+1, col-1] = 1 
                if(dist_to[row+1,col]>dist_to[row][col]+energy[row+1,col]):
                    dist_to[row+1,col]=dist_to[row][col]+energy[row+1,col]
                    edge_to[row+1, col] = 0 
                if(col!= cols-1 and dist_to[row+1,col+1]>dist_to[row][col]+energy[row+1,col+1]):
                    dist_to[row+1,col+1]=dist_to[row][col]+energy[row+1,col+1]
                    edge_to[row+1, col+1] = -1 
        # Find min value in last rows of image
        seam[rows-1] = np.argmin(dist_to[rows-1, :])
        for i in (x for x in reversed(range(rows)) if x > 0): 
            seam[i-1] = seam[i] + edge_to[i, int(seam[i])] 
        return(seam)
    def delete_seam(self,img,seam):
        rows,cols=img.shape[:2]
        # From each index seam translate col to left
        for row in range(rows):
            for col in range(int(seam[row]),cols-1):
                img[row,col]=img[row,col+1]
        img = img[:, 0:cols-1] 
        return img 
    def add_seam(self,img, seam,i): 
        rows, cols = img.shape[:2]
        seam=seam+i
        # add new col from last col image
        zero_col_mat = np.zeros((rows,1,3), dtype=np.uint8) 
        img = np.hstack((img, zero_col_mat)) 
        # Get average pixel from left and right col
        # From last col -> index seam col : translate col to right
        print(rows, cols)
        # self.QT.text_process.append(str(rows)+" "+str(cols))
        print(str(rows)+" "+str(cols))
        
        for row in range(rows): 
            for col in range(cols, int(seam[row]), -1): 
                img[row, col] = img[row, col-1]
            if(int(seam[row])<0):
                img[row, int(seam[row])] =img[row, int(seam[row])+1].astype(int)
            elif(int(seam[row])>=cols):
                img[row, int(seam[row])] =img[row, int(seam[row])-1].astype(int)
            else:
                img[row, int(seam[row])] =((img[row, int(seam[row])-1].astype(int)+ img[row, int(seam[row])+1].astype(int))/2 ).astype(int)
        return img 
    def update_seams(self,seams_record, current_seam):
        output = []
        # after add_seam if current_seam <= seam need to translate 2 col
        for seam in seams_record:
            seam[np.where(seam >= current_seam)] += 2
            output.append(seam)
        return output
    def draw_seam_old(self,img,seam):
        img_seam = np.copy(img)
        for i,j in enumerate(seam):
            img_seam[i,int(j)]=(0,255,0)
        return img_seam
    def draw_seam2(self,img, seam): 
        rows, cols = img.shape[:2] 
        # add new col from last col image
        zero_col_mat = np.zeros((rows,1,3), dtype=np.uint8) 
        img = np.hstack((img, zero_col_mat)) 
        # Get average pixel from left and right col
        # From last col -> index seam col : translate col to right
        for row in range(rows): 
            for col in range(cols, int(seam[row]), -1): 
                img[row, col] = img[row, col-1] 
            img[row, int(seam[row])] =(0.0,0.0,0.0)
        return img 
    def show_image_process(self):
        cv2.imshow("Image After Process",self.image_process)
    def show_image_org(self):
        cv2.imshow("Image Orginal",self.image_orginal)
    def show_enery(self):
        cv2.imshow("Image Energy",self.energy_temp)

# if __name__=='__main__':
#     imagedir="C:\\Users\\DUCANH\\Desktop\\test_seam.jpg"
#     test=SeamCarving(imagedir,334,274,is_remove_object=False)