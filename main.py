import cv2 as cv

cap = cv.VideoCapture("SampleClip1.avi")
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("No frame received. Exiting... ")
        break

    if cv.waitKey(1) == ord("q"):
        break

    cv.imshow("Frame", frame)