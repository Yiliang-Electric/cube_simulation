import cv2
import numpy as np
import math

class cube:
    def __init__(self) -> None:
        pass

    def find_corners(self,image):
        size = 30
        objp = np.zeros((6*9,3), np.float32)
        objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)*size
        objpoints = []
        imagepoints = []
        gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        ret,corners=cv2.findChessboardCorners(gray,(9,6),None) 
        if ret == True:
            objpoints.append(objp)
            imagepoints.append(corners)
            return objpoints,imagepoints
        else:
            return False

    #first time run, create calibration config with chess board
    def calibrate(self,img):
        img = cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_AREA)
        cv2.imshow('calibrate',img)
        cv2.waitKey(1)
        conrner = self.find_corners(img)
        if conrner!=False:
            objpoints, imagepoints = conrner
        else:
            return False
        cv2.destroyAllWindows()

        im_shape=(1920, 1080)
        __, mtx, dist, __, __ = cv2.calibrateCamera(objpoints, imagepoints,im_shape,None,None)

        np.savez('camera_matrix',mtx=mtx,dist=dist)

    def draw_cube(self,img, corners, imgpts):
        imgpts = np.int32(imgpts).reshape(-1,2)
        img = cv2.drawContours(img, [imgpts[:4]],-1,(0,255,0),3)
        for i,j in zip(range(4),range(4,8)):
            img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),3)
        img = cv2.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)
        return img

    def draw(self,img, corners, imgpts):
        corner = tuple(corners[0].ravel())
        img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
        img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
        img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
        return img

    # def point_T1(self,rec):
    #     objp = np.zeros((9*6,3), np.float32)
    #     objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
    #     list = []
    #     if math.dist(rec[0][0],rec[1][0])>math.dist(rec[1][0],rec[2][0]):
    #         x_v1 = (rec[1][0]-rec[0][0])/8
    #         x_v2 = (rec[2][0]-rec[3][0])/8
    #         for j in range(6):
    #                 for i in range(9):
    #                     list.append(rec[0][0]+x_v1*i+(rec[3][0] + x_v2*i -rec[0][0]-x_v1*i)/5*j)
    #     else:
    #         x_v1 = (rec[0][0]-rec[3][0])/8
    #         x_v2 = (rec[1][0]-rec[2][0])/8
    #         for j in range(6):
    #             for i in range(9):
    #                 list.append(rec[3][0]+x_v1*i+(rec[2][0] + x_v2*i -rec[3][0]-x_v1*i)/5*j)
    #     return objp,np.array(list,np.float32)

    def point_T1(self,rec):
        list = []
        x_v1 = (rec[0][0]-rec[3][0])/8
        x_v2 = (rec[1][0]-rec[2][0])/8
        for j in range(6):
            for i in range(9):
                list.append(rec[3][0]+x_v1*i+(rec[2][0] + x_v2*i -rec[3][0]-x_v1*i)/5*j)
        return np.array(list,np.float32)

    #polygon to conrner
    def mask_corner(self,contour1):
        image = np.zeros([1080,1920,3],dtype=np.uint8)
        image.fill(255)
        for i in range(0,len(contour1),2):
            cv2.circle(image, (contour1[i][0],contour1[i+1][0]), 1, (0,0,0), 1)
        image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        image = cv2.GaussianBlur(image,(5,5),0)
        image = cv2.Canny(image,50,100)
        contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour = contours[0]
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.05 * perimeter, True)
        return approx    

    #transform corner to function need
    def set_original_quadrilateral(self,corner):
        #1--4
        #|  |
        #2--3
        x_v1 = (corner[3]-corner[0])/8
        x_v2 = (corner[2]-corner[1])/8
        l = []
        for j in range(6):
            for i in range(9):
                t = np.append((corner[0]+x_v1*i+(corner[1] + x_v2*i -corner[0]-x_v1*i)/5*j),[0])
                l.append(t)
        self.objp = np.array(l,np.float32)

    def read_config(self):
        with np.load('camera_matrix.npz') as file:
            self.mtx,self.dist=[file[i] for i in ['mtx','dist']] 

    # def show(self,img,polygon):
    def show(self,img,corner):
        # self.objp = np.zeros((9*6,3), np.float32)
        # self.objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
        img = cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_AREA)
        # corner = self.mask_corner(polygon)
        # if len(corner)!=4:
        #     return img
        point = self.point_T1(corner)
        x,y = 9,6
        axis = np.float32([[0,0,0], [0,y,0], [x,y,0], [x,0,0],
                        [0,0,3],[0,y,3],[x,y,3],[x,0,3] ])
        _,rvec,tvec,_=cv2.solvePnPRansac(self.objp,point,self.mtx,self.dist)
        imgpts,_=cv2.projectPoints(axis,rvec,tvec,self.mtx,self.dist)
        frame = self.draw_cube(img,point,imgpts)
        return frame
