import cv2
import numpy as np

class cube:
    def __init__(self) -> None:
        pass

    def find_corners(self,image,size):
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
    def calibrate(self,img,size=30):
        img = cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_AREA)
        cv2.imshow('calibrate',img)
        cv2.waitKey(1)
        conrner = self.find_corners(img,size)
        if conrner!=False:
            objpoints, imagepoints = conrner
        else:
            return False
        cv2.destroyAllWindows()

        im_shape=(1920, 1080)
        __, mtx, dist, __, __ = cv2.calibrateCamera(objpoints, imagepoints,im_shape,None,None)

        np.savez('camera_matrix',mtx=mtx,dist=dist)
    
# c = cube()
# img = cv2.imread('1.jpg')
# c.calibrate(img)
