import cv2 as cv
import numpy as np

kernel = np.ones((3,3), dtype=np.uint8)

cap = cv.VideoCapture(0)

ret, frame_last = cap.read()
grey_last = cv.cvtColor(frame_last, cv.COLOR_BGR2GRAY)

while cap.isOpened():

    ret, frame = cap.read()

    if not ret:
        print("No frame received. Exiting... ")
        break

    if cv.waitKey(1) == ord("q"):
        break


    grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    grey_diff = cv.subtract(grey, grey_last)
    grey_diff = cv.medianBlur(grey_diff, 3)

    frame_last = frame
    grey_last = grey

    mask = cv.adaptiveThreshold(grey_diff, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV, 11, 3)
    mask = cv.medianBlur(mask, 3)

    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel, iterations=1)

    contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    cv.drawContours(frame, contours, -1, (0, 255, 0), 3)

    cv.imshow("Frame", frame)
    cv.imshow("Grey", grey)
    cv.imshow("grey_diff", grey_diff)
    cv.imshow("mask", mask)