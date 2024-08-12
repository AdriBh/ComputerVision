# We took the track py code and convert into oop type code
import mediapipe as mp
import cv2
import time

class HandDetector():
    # We are gonna take as parameters the parameters of the Hands Object
    # Initializing the Hands objects
    def __init__(self,Mode=False,maxHands=2,min_det_confi=0.5,min_track_confi=0.5):
        self.Mode = Mode

        #self.model_complexity = complexity

        self.maxHands = maxHands

        self.min_det_confi = min_det_confi

        self.min_track_confi = min_track_confi

        self.mpHands = mp.solutions.hands

        self.mpDraw = mp.solutions.drawing_utils

        self.hands = self.mpHands.Hands(
            static_image_mode=self.Mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.min_det_confi,
            min_tracking_confidence=self.min_track_confi
        )
    
    def findHands(self,img,draw=True):
        # This is the part that will be in the while loop
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) # we do this bcuz hands object takes rgb image only

        self.results = self.hands.process(imgRGB)

        #print(results.multi_hand_landmarks)
        # below code runs if hand is detected

        if self.results.multi_hand_landmarks:

            for handLms in self.results.multi_hand_landmarks:

                if draw:

                    self.mpDraw.draw_landmarks(img,
                                        handLms,
                                        self.mpHands.HAND_CONNECTIONS # DRAWS THE HAND CONNECTION
                    )

        return img
    
    def findPosition(self,img,handNo = 0,draw = True):

        lmList = []

        if self.results.multi_hand_landmarks:
            # There can be number of hands in a single frame (we are choosing one of them and printing the dots posi and returining it)

            myhand = self.results.multi_hand_landmarks[handNo]

            for id,lm in enumerate(myhand.landmark):
                
                #print(id,lm)

                height,width,channel  = img.shape # we do this because we want to extract the coordinate of the landmarks (dot coord which is centre x amd centre y)

                centre_x , centre_y = int(lm.x*width) , int(lm.y*height) # Converting the decimal coordinate to pixel value (earlier it was normalized)

                #print(id,centre_x,centre_y)

                lmList.append([id,centre_x,centre_y])

                if draw:
                    cv2.circle(img,(centre_x,centre_y),10,(255,0,255),cv2.FILLED)
        return lmList




   

def main():
    # copy this code in other py files to use this module

    prevTime = 0

    curTime = 0

    cap = cv2.VideoCapture(0) 
    detector = HandDetector()
    while True:
        success,img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)   
        if len(lmList)!=0:
            print(lmList)

        curTime = time.time()
        fps = 1/(curTime-prevTime)
        prevTime = curTime

        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,color = (255,0,255),thickness=3)

        cv2.imshow("Image",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # press 'q' to exit the loop
            break
    cap.release()
    cv2.destroyAllWindows()



if __name__=="__main__":
    main()