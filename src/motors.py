import RPi.GPIO as GPIO          
from time import time

def Motors():
    def __init__(self, in1 = -1, in2 = -1, in3 = -1, in4 = -1):
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1,GPIO.OUT)
        GPIO.setup(self.in2,GPIO.OUT)
        GPIO.setup(self.in3,GPIO.OUT)
        GPIO.setup(self.in4,GPIO.OUT)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)
    
    def forward_for_ms(self, time_in_ms):
        endtime = time.monotonic() + time_in_ms
        while (endtime - time.monotonic() >= 0):
            GPIO.output(self.in1,GPIO.HIGH)
            GPIO.output(self.in2,GPIO.LOW)
            GPIO.output(self.in3,GPIO.LOW)
            GPIO.output(self.in4,GPIO.HIGH)
        return
    
    def forward_for_ms(self, time_in_ms):
        endtime = time.monotonic() + time_in_ms
        while (endtime - time.monotonic() >= 0):
            GPIO.output(self.in1,GPIO.LOW)
            GPIO.output(self.in2,GPIO.HIGH)
            GPIO.output(self.in3,GPIO.HIGH)
            GPIO.output(self.in4,GPIO.LOW)
        return