import cv2
import numpy as np
import configparser

class c:
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
    def calibrate(self,img,file,size=30):
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
        # self.write_config(mtx,dist)
        np.savez(file,mtx=mtx,dist=dist)
        return True

    # def write_config(self,mtx,dis):
    #     config = configparser.ConfigParser()
    #     config['mtx'] = {}
    #     for i in range(len(mtx)):
    #         config['mtx'][str(i)] = str(mtx[i])
    #     config['dis'] = {}
    #     for i in range(len(dis)):
    #         config['dis'][str(i)] = str(dis[i])
    #     with open ('calibration.ini','w') as configfile:
    #         config.write(configfile)
    
# cc = c()
# img = cv2.imread('1.jpg')
# cc.calibrate(img)
