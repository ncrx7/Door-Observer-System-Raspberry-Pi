import RPi.GPIO as GPIO
import time

class Checker:
	def CheckWithLed(timeLed):
		ledPin = 33
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(ledPin, GPIO.OUT)
		GPIO.output(ledPin, GPIO.HIGH)
		time.sleep(timeLed)
		GPIO.cleanup(33)
