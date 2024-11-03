import cv2
import time
import threading
import dlib
import numpy as np
from simple_facerec import SimpleFacerec
from EmailSender import EmailSender
from Checker import Checker
#from deepface import DeepFace

class CameraControlManager:
    def __init__(self):
        self.lastPhotoTime = 0
        self.photoInterval = 10
        self.imgCounter = 0
        self.canProccesImage = True
        self.unknownPerson = False
        self.detector = dlib.get_frontal_face_detector()
    def StartVideoCapture(self):
        sfr = SimpleFacerec()
        sfr.load_encoding_images("/home/ncrxbatu/Desktop/doorobserveproject/images/")
        
        
        self.cap = cv2.VideoCapture(0) 
        if not self.cap.isOpened():
            print("Kamera bağlı değil.")
            return None
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            
        if self.cap is None:
            return
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Frame alınamadı.")
                break
            
            face_locations, face_names = sfr.detect_known_faces(frame)
            self.unknownPerson = False
            for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,0), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2),(0, 0, 200), 2)
                
                if name == "Unknown":
                    self.unknownPerson = True
                    print(name)
                else:
                    self.unknownPerson = False
                    print("else worked")
            print(self.unknownPerson)
                
            cv2.imshow("USB kamera logitech", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        self.cap.release()
        cv2.destroyAllWindows()
        
    def StartVideoCaptureOnThread(self):
        VideoCaptureThread = threading.Thread(target = self.StartVideoCapture)
        VideoCaptureThread.start()
        
    def TakePhoto(self):
        currentTime = time.time()
        if currentTime - self.lastPhotoTime >= self.photoInterval:
            self.canProccesImage = True
            if not self.cap.isOpened():
                print("take photo camera is not worked")
                return None
            ret, frame = self.cap.read()
            if not ret:
                print("take photo frame is not recieved")
                return None
            imgName = "/home/ncrxbatu/Desktop/doorobserveproject/home_photo_{}.png".format(self.imgCounter)
            cv2.imwrite(imgName, frame)
            self.imgCounter += 1
            """cv2.imshow("Captured Photo", frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()"""
            self.lastPhotoTime = time.time()
            Checker.CheckWithLed(2)
            return frame
        else:
            print("time out take photo")
            self.canProccesImage = True
            return None
        
    def ProcessImage(self, frame):
            if self.canProccesImage and frame is not None:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
                sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)

                abs_sobelx = np.absolute(sobelx)
                abs_sobely = np.absolute(sobely)

                sobel_combined = cv2.addWeighted(abs_sobelx, 0.5, abs_sobely, 0.5, 0)

                _, binary_output = cv2.threshold(sobel_combined, 50, 255, cv2.THRESH_BINARY)

                imgNameSobel = "/home/ncrxbatu/Desktop/doorobserveproject/sobel_photo_{}.png".format(self.imgCounter)
                cv2.imwrite(imgNameSobel, sobel_combined)
                imgNameBinary = "/home/ncrxbatu/Desktop/doorobserveproject/binary_photo_{}.png".format(self.imgCounter)
                cv2.imwrite(imgNameBinary, binary_output)
                """cv2.imshow('Original Frame', frame)
                cv2.imshow('Sobel Filter', sobel_combined)
                cv2.imshow('Binary Output', binary_output)
                cv2.waitKey(0)
                cv2.destroyAllWindows()"""
            
        
        
    
