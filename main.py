#print("YOO")
import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

wCam, hCam = 640, 480
#framesize(the working region)
frameRed = 100
#for make movement smooth
smooth = 7

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
plocX, plocY = 0, 0
clocX, clocy = 0, 0
#no of hand required is only 1
detector = htm.handDetector(maxHands=1)
wScreen, hScreen = autopy.screen.size()


#print(wScreen,hScreen) (1440,900)

while True:
    success, img = cap.read()
    #finding the hand landmarks
    img = detector.findHands(img)
    #lmlist will have all coordinate of 21 points
    #detect position & draw bounding box
    lmList, bbox = detector.findPosition(img)

    if len(lmList)!=0:
        #now getting tip of index and middle finger
        #getting reeq tip point from 21 points
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        #print(x1, y1, x2, y2)

        #now finidng fingers which are up (done in tracking module)
        fingers = detector.fingersUp()
        #if fingers== [0, 0, 1, 0, 0]:
            #print("Dont do that here Fck Off!!")

        # reducing frame size in which pointer will work
        cv2.rectangle(img, (frameRed, frameRed), (wCam - frameRed, hCam - frameRed), (255, 0, 255), 2)

        #check if only index finger is moving
        if fingers[1] == 1 and fingers[2] == 0:

            # converting coordinates to get the location
            x3 = np.interp(x1, (frameRed, wCam-frameRed), (0, wScreen))
            y3 = np.interp(y1, (frameRed, hCam-frameRed), (0,hScreen))

            #making movement smooth
            clocX = plocX + (x3 - plocX) / smooth
            clocY = plocY + (y3 - plocY) /smooth

            #moving mouse
            autopy.mouse.move(wScreen-clocX,clocY)
            #to flip wScreen-x3
            #creating a circle pointer
            cv2.circle(img, (x1,y1), 15, (255,0,255),cv2.FILLED)
            plocX, plocY = clocX, clocY

        #if the middle finger also up along with index finger
        if fingers[1] == 1 and fingers[2] == 1:
            #finding distance btw the two finger
            length, img, _ = detector.findDistance(8, 12, img)
            #print(length)
            #if distance below 40 click
            if length < 40:
                cv2.circle(img, (x1, y1), 15, (255, 255, 0), cv2.FILLED)

                #clicking the left mouse button
                autopy.mouse.click()





    #setting frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0),3)

    #displaying
    cv2.imshow("Image",img)
    cv2.waitKey(1)

