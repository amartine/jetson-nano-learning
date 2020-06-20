import cv2
import numpy as np
import time
from threading import Thread

status = True
startTimeCam1 = time.time()
startTimeCam2 = time.time()
elapsedTimeAverage1 = 0
elapsedTimeAverage2 = 0


cv2.namedWindow('0')
cv2.moveWindow('0',200,100)
cv2.namedWindow('1')
cv2.moveWindow('1',860,100)

class MyCamera(Thread):
    global camera1, camera2, status
    def __init__ (self, camSet, camIndex,camName):
        Thread.__init__(self)
        self.cameraSettings = camSet
        self.cameraIndex = camIndex
        self.CameraName = camName
    def run(self):
        if status:
            if (self.cameraSettings != ''):
                camera1= cv2.VideoCapture(self.cameraSettings)
                frameReader (camera1, self.CameraName)
            else:
                camera2 = cv2.VideoCapture(self.cameraIndex)
                frameReader (camera2, self.CameraName)

def frameReader(camera, cameraName):
    global status, startTimeCam1, startTimeCam2, elapsedTimeAverage1, elapsedTimeAverage2
    if camera.isOpened():
        ret, frame= camera.read()
        
    else:
        ret = False
    while ret:
        ret, frame= camera.read()
        if cameraName == '0':
            t = time.time() - startTimeCam1
            elapsedTimeAverage1 = .9*elapsedTimeAverage1 + .1*t   
            FPS = str(round(1/elapsedTimeAverage1,1))
        if cameraName == '1':
            t = time.time() - startTimeCam2
            elapsedTimeAverage2 = .9*elapsedTimeAverage2 + .1*t   
            FPS = str(round(1/elapsedTimeAverage2,1))

        cv2.rectangle(frame,(0,0),(130,40),(0,0,255),-1)
        cv2.putText(frame, FPS + ' fps',(3,28), font,0.75,(66,174,255),2)
        startTimeCam1 = time.time()
        startTimeCam2 = time.time()
        cv2.imshow(cameraName,frame)
        
        if (cv2.waitKey(1)==ord('q')):
            break
    status = False
    


dispW=640
dispH=480
flip=0
font = cv2.FONT_HERSHEY_SIMPLEX
elapsedTimeAverage = 0 



startTime = time.time()

thread1 = MyCamera('nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink',0,'0')
thread2 = MyCamera('',1,'1')

thread1.daemon = True
thread2.daemon = True

thread1.start()
thread2.start()


while True:
    if status == False:
        break
try:
    camera1.release()
except:
    pass
try:
    camera2.release()
except:
    pass
cv2.destroyAllWindows()