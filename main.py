import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time

#img = cv2.imread('emp.jpg')

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

with open('strings.text', 'r') as f:
    myDataList = f.read()

with open('rentry.text', 'r') as f1:
    myList = f1.read()

while True:
    success, img = cap.read()
    code = decode(img)
    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')
        time.sleep(2)

        with open('rentry.text', 'r') as f1:
            myList = f1.read()

        if myData in myDataList:
            myOutput = "Authorised"
            myColor = (0, 255, 0)
            myDataList = myDataList.replace(myData, '0')
            with open('strings.text', 'w') as file1:
                file1.write(myDataList)
            with open('rentry.text', 'a') as file2:
                file2.writelines(myData+"\n")
            print("Data Shifted")

        else:
            if myData in myList:
                myOutput = "Re-Entering"
                myColor = (255, 0, 0)
            else:
                myOutput = "Un-authorised"
                myColor = (0, 0, 255)

        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, myColor, 5)
        pts2 = barcode.rect
        cv2.putText(img, myOutput, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, myColor, 2)

    cv2.imshow('Authentication Result', img)
    cv2.waitKey(5)
