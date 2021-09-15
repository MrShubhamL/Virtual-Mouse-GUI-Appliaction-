from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from tkinter import*
from PyQt5.uic import loadUiType
import sys
import math
import cv2
import numpy as np
import time
import autopy
import Hand_Tracking_Module as htm


pi,_ = loadUiType('virtual.ui')
class mouse_vi(QMainWindow,pi):
    count = 0
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Virtual Mouse")
        self.setWindowIcon(QIcon('src/icons/power_module.png'))
        self.setGeometry(500,500,800,450)
        self.setupUi(self)
        self.handelButton()
        self.show()


    def handelButton(self):
        self.pushButton.clicked.connect(self.controlling)

    def controlling(self):
            
        wCam, hCam = 800, 500
        frameR = 100 #frame Reduction
        smoothening = 8


        cap = cv2.VideoCapture(1)
        cap.set(3, wCam)
        cap.set(4, hCam)

        detector = htm.handDetector(maxHands=1)
        wScr, hScr = autopy.screen.size()

        pTime = 0
        plocX, plocY = 0, 0
        clocX, clocY = 0, 0

        while True:
            # 1. Find the Hand Landmark
            success, img = cap.read()

            img = detector.findHands(img)
            lmList, bbox = detector.findPosition(img)


        #   # 2.  Get the tip of the index and middel fingers
            if len(lmList)!=0:
                x1,y1 = lmList[8][1:]
                x2,y2 = lmList[12][1:]
        #         # print(x1,y1,x2,y2)



        #     # 3. Check which fingers are up
                fingers = detector.fingerUp()
        #         # print(fingers)

                cv2.rectangle(img,(frameR, frameR),(wCam-frameR, hCam-frameR),(255,0,255),2)
        #        # 4. Only Index Finger : Moving Mode
                if fingers[1]==1 and fingers[2] ==0:
                    # 5. Convert Coordinate
                    x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
                    y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))


        #         # 6. Smoothen Values
                    clocX = plocX + (x3 - plocX) / smoothening
                    clocY = plocY + (y3 - plocY) / smoothening

        #         # 7. Move Mouse
                    autopy.mouse.move(wScr-clocX, clocY)
                    cv2.circle(img,(x1,y1), 15, (255, 0, 255), cv2.FILLED)
                    plocX,plocY = clocX,clocY

        #         # 8. Both fingers are up : Clicking Mode
                if fingers[1]==1 and fingers[2] ==1:
                    length =  math.hypot(x2-x1, y2-y1)
                    # length =  math.hypot(8, 12)
                    # lineInfo=  math.hypot(8, 12)
                    print(length)



        #         # 10. Click mouse if distance short
                    if length < 50:
                        # cv2.circle(img,(lineInfo[4], lineInfo[5]),15,(0,255,0),cv2.FILLED)
                        cv2.circle(img,(x1,y1), 15, (255, 0, 255), cv2.FILLED)
                        autopy.mouse.click()


        # 11. Frame Rate
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            cv2.putText(img,str(int(fps)),(20, 50), cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)


            cv2.imshow("Video",img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break



def main():
    app = QApplication(sys.argv)
    window = mouse_vi()
    window.show()
    sys.exit(app.exec_())
    # app.exec_()


if __name__ == '__main__':
    main()
    