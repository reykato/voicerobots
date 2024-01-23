import RPi.GPIO as GPIO          
import time

class Motors:
    def __init__(self, l1, l2, r1, r2, l_en, r_en):
        self.l1 = l1
        self.l2 = l2
        self.r1 = r1
        self.r2 = r2
        self.l_en = l_en
        self.r_en = r_en
        GPIO.setmode(GPIO.BCM)
        p1 = GPIO.PWM(l_en,1000)
        p2 = GPIO.PWM(r_en,1000)
        p1.start(100) 
        p2.start(100)
        GPIO.setup(self.l1,GPIO.OUT)
        GPIO.setup(self.l2,GPIO.OUT)
        GPIO.setup(self.r1,GPIO.OUT)
        GPIO.setup(self.r2,GPIO.OUT)
        GPIO.output(self.l1,GPIO.LOW)
        GPIO.output(self.l2,GPIO.LOW)
        GPIO.output(self.r1,GPIO.LOW)
        GPIO.output(self.r2,GPIO.LOW)
    
    def all_off(self):
        GPIO.output(self.l1,GPIO.LOW)
        GPIO.output(self.l2,GPIO.LOW)
        GPIO.output(self.r1,GPIO.LOW)
        GPIO.output(self.r2,GPIO.LOW)

    def forward_for_ms(self, time_in_ms):
        endtime = (time.monotonic()*1000) + time_in_ms
        while (endtime - (time.monotonic()*1000) >= 0):
            GPIO.output(self.l1,GPIO.HIGH)
            GPIO.output(self.l2,GPIO.LOW)
            GPIO.output(self.r1,GPIO.LOW)
            GPIO.output(self.r2,GPIO.HIGH)
        self.all_off()
        return
    
    def backward_for_ms(self, time_in_ms):
        endtime = (time.monotonic()*1000) + time_in_ms
        while (endtime - (time.monotonic()*1000) >= 0):
            GPIO.output(self.l1,GPIO.LOW)
            GPIO.output(self.l2,GPIO.HIGH)
            GPIO.output(self.r1,GPIO.HIGH)
            GPIO.output(self.r2,GPIO.LOW)
        self.all_off()
        return
    
    def set_duty_cycle(self, x, y):
        '''Uses the x and y inputs to calculate and output the duty cycle
          for the motors, controlling the speed and trajectory of the robot
          
          Parameters:
            x (float): x-axis value (turning)
            y (float): y-axis value (speed)'''
        
        # calculate the duty cycle for each motor, also in interval [-1, 1]
        l_duty_cycle = max(min(1, y + x), -1)
        r_duty_cycle = max(min(1, y - x), -1)


        # set the direction of the motors
        if l_duty_cycle < 0:                # backwards
            GPIO.output(self.l1,GPIO.LOW)
            GPIO.output(self.l2,GPIO.HIGH)
        elif l_duty_cycle > 0:              # forwards
            GPIO.output(self.l1,GPIO.HIGH)
            GPIO.output(self.l2,GPIO.LOW)
        else:                               # stop
            GPIO.output(self.l1,GPIO.LOW)
            GPIO.output(self.l2,GPIO.LOW)
        
        if r_duty_cycle < 0:                # backwards
            GPIO.output(self.r1,GPIO.HIGH)
            GPIO.output(self.r2,GPIO.LOW)
        elif r_duty_cycle > 0:              # forwards
            GPIO.output(self.r1,GPIO.LOW)
            GPIO.output(self.r2,GPIO.HIGH)
        else:                               # stop
            GPIO.output(self.r1,GPIO.LOW)
            GPIO.output(self.r2,GPIO.LOW)


        # set the duty cycle for the motors, abs(duty_cycle) forces the
        # interval on [0, 1]. the sign only specifies direction
        # which is handled above
        self.l_en.setDutyCycle(abs(l_duty_cycle))
        self.r_en.setDutyCycle(abs(r_duty_cycle))
        
        