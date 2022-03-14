import cv2
import time
import numpy as np

#print(cv2.__version__)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

logo = cv2.imread("assets/logo.png",0)
size = 100
gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
logo = cv2.resize(gray,(size,size),interpolation =cv2.INTER_CUBIC)
_, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

while True:
    # Read the a frame from webcam
    _,frame = cap.read()

    #resize the image in case that our processing power is low
    frame = cv2.resize(frame,(640,480))

    #flip the image so it feels like a mirror
    frame = cv2.flip(frame,1)
    """
    #add the FPS to the image
    text = "FPS" + str(int(1/(time.time()-last_time)))
    last_time = time.time()
    cv2.putText(frame,text,(10,38),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
    """
    #roi = region of interest
    roi = frame[-size-10:10,-size-10:10] 
    roi[np.where(mask)] = 0
    roi += logo
    # Show the frame in a window
    cv2.imshow("cam",frame)

    # Check if q has been pressed to quit
    if cv2.waitKey(1) == ord('q'):
        break
