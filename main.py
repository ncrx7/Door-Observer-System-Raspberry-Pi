import cv2
import threading
import RPi.GPIO as GPIO
import time
#from DistanceCalculatorManager import SetupDistanceSensor
#from DistanceCalculatorManager import CalculateDistance
#from DistanceCalculatorManager import GetTriggerPin
#from DistanceCalculatorManager import GetEchoPin
from MotionDetectionManager import MotionDetectionManager
from CameraControlManager import CameraControlManager
from DistanceCalculatorManager import DistanceCalculatorManager
from EmailSender import EmailSender
from Checker import Checker


cameraControlInstance = None
distanceCalculatorManager = None
motionDetectionManager = None
emailSender = None

def main():
    Checker.CheckWithLed(5)
    Initialize()
    cameraControlInstance.StartVideoCaptureOnThread()
    Program()
            
def Initialize():
    global cameraControlInstance
    global distanceCalculatorManager
    global motionDetectionManager
    global emailSender
    cameraControlInstance = CameraControlManager()
    distanceCalculatorManager = DistanceCalculatorManager()
    motionDetectionManager = MotionDetectionManager()
    emailSender = EmailSender()
    distanceCalculatorManager.SetupDistanceSensor()
    motionDetectionManager.SetupMotionSensor()
    
def Program():
    while True:
        motionValue = motionDetectionManager.GetMotionValue()
        print(motionValue)
        if motionValue == 1 and cameraControlInstance.unknownPerson:
            #print("hareket tespit edildi")
            distance = distanceCalculatorManager.CalculateDistance(distanceCalculatorManager.GetTriggerPin(), distanceCalculatorManager.GetEchoPin())
            print(f"Ultrasonik mesafe: {distance} cm")
            if distanceCalculatorManager.CheckDistance(distance, 20):
                print("foto alınacak")
                homePhoto = cameraControlInstance.TakePhoto()
                emailSender.send_email("se.batuhan.uysal@gmail.com", homePhoto)
                cameraControlInstance.ProcessImage(homePhoto)
        time.sleep(0.5)    

if __name__ == "__main__":
    main()


