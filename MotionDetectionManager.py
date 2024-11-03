import RPi.GPIO as GPIO
import time

"""GPIO.setmode(GPIO.BOARD)
motion_pin = 37

GPIO.setup(motion_pin, GPIO.IN)

while True:
    if GPIO.input(motion_pin):
        print("hareket alarmı")
        print(GPIO.input(motion_pin))"""

class MotionDetectionManager:
    def __init__(self):
        self.motion_pin = 37
        
    def SetupMotionSensor(self):
        print("set motion pin function triggered")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.motion_pin, GPIO.IN)
    
    def GetMotionValue(self):
        return GPIO.input(self.motion_pin)
        
