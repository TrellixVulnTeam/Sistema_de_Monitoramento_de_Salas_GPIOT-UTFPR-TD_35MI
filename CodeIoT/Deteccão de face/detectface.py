# -*- coding: utf-8 -*-
import cv2
import sys

x=0
y=0

cascPath = "classifier/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
font=cv2.FONT_HERSHEY_SIMPLEX
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50),
    )
    if len(faces) >= 1:
     print "Face detect"
     for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 100), 1)
        stringxy="+%s,%s"%(x,y) 
        cv2.putText(frame,stringxy,(x+w/2,y+h/2),font, 1,(0,0,255),1)
        cv2.imwrite('face.jpg', frame)
    else:
        print "Not face "
        cv2.imwrite('face.jpg', frame)
    cv2.imshow('Video', frame)
    print x,y,
    print"\n"
    font=cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(faces,'x,y',(x,y),font, 2,(255,255,255),1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

        
video_capture.release()
cv2.destroyAllWindows()