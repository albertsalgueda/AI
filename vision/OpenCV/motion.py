import cv2
import numpy as np

# Setup camera
cap = cv2.VideoCapture(0)
# Set a smaller resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#let camara adjust ratio and lighting
for _ in range(15):
    _, frame = cap.read()
frame = cv2.resize(frame,(640,480))
frame = cv2.flip(frame,1)

img2gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
img2gray = cv2.GaussianBlur(img2gray,(25,25),0)
last_frame = img2gray

while cap.isOpened():
    # Capture frame-by-frame
    _, frame = cap.read()
    frame = cv2.resize(frame,(640,480))
    frame = cv2.flip(frame,1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (25, 25), 0)
 
    abs_diff = cv2.absdiff(last_frame, gray)
    last_frame = gray
 
    _, ad_mask = cv2.threshold(abs_diff, 15, 255, cv2.THRESH_BINARY)
 
    cv2.imshow("Abs diff mask", ad_mask)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()