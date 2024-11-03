import RPi.GPIO as GPIO
import time

class DistanceCalculatorManager:
    trigger_pin = None
    echo_pin = None
        
    def SetupDistanceSensor(self):
        print("set distance pin function triggered")
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        global trigger_pin
        trigger_pin = 8
        global echo_pin
        echo_pin = 10
        GPIO.setup(trigger_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)
        
    def CalculateDistance(self, trigger_pin, echo_pin):
        print("calculate distance function triggered")
        GPIO.output(trigger_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(trigger_pin, GPIO.LOW)

        while GPIO.input(echo_pin) == 0:
            pulse_start = time.time()

        while GPIO.input(echo_pin) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 34300 / 2
        print(distance)
        return distance
    
    def CheckDistance(self, _distance, threshold):
        if _distance < threshold:
            return True;

    def GetTriggerPin(self):
        return trigger_pin
    def GetEchoPin(self):
        return echo_pin
        
    """SetPinsForDistanceCalculator() 
     
    while True:
        CalculateDistance(trigger_pin, echo_pin)"""
        
