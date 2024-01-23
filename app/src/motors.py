import RPi.GPIO as GPIO          
import time

class Motors:
    def __init__(self, l1, l2, r1, r2, l_en, r_en):
        # l1 and l2 are the two connections to the left motor
        self.left_1 = l1
        self.left_2 = l2

        # l1 and l2 are the two connections to the right motor
        self.right_1 = r1
        self.right_2 = r2

        # l_en is the 'enable' connection to the left motor
        # r_en is the 'enable' connection to the right motor
        self.left_enable = l_en
        self.right_enable = r_en

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.left_1,GPIO.OUT)
        GPIO.setup(self.left_2,GPIO.OUT)
        GPIO.setup(self.right_1,GPIO.OUT)
        GPIO.setup(self.right_2,GPIO.OUT)
        GPIO.setup(self.left_enable, GPIO.OUT)
        GPIO.setup(self.right_enable, GPIO.OUT)


        # declare a PWM signal at 1kHz on l_en and r_en
        # l_pwm and r_pwm are used for setting the speed of each motor
        self.left_pwm = GPIO.PWM(self.left_enable, 1000)
        self.right_pwm = GPIO.PWM(self.right_enable, 1000)

        # start the PWM signal at 0% duty cycle
        self.left_pwm.start(0) 
        self.right_pwm.start(0)

        
        # set all motors off
        GPIO.output(self.left_1,GPIO.LOW)
        GPIO.output(self.left_2,GPIO.LOW)
        GPIO.output(self.right_1,GPIO.LOW)
        GPIO.output(self.right_2,GPIO.LOW)
    
    def all_off(self):
        self.left_pwm.setDutyCycle(0)
        self.right_pwm.setDutyCycle(0)

    def forward_for_ms(self, time_in_ms):
        end_time = (time.monotonic()*1000) + time_in_ms
        while (end_time - (time.monotonic()*1000) >= 0):
            GPIO.output(self.left_1,GPIO.HIGH)
            GPIO.output(self.left_2,GPIO.LOW)
            GPIO.output(self.right_1,GPIO.LOW)
            GPIO.output(self.right_2,GPIO.HIGH)
        self.all_off()
        return
    
    def backward_for_ms(self, time_in_ms):
        end_time = (time.monotonic()*1000) + time_in_ms
        while (end_time - (time.monotonic()*1000) >= 0):
            GPIO.output(self.left_1,GPIO.LOW)
            GPIO.output(self.left_2,GPIO.HIGH)
            GPIO.output(self.right_1,GPIO.HIGH)
            GPIO.output(self.right_2,GPIO.LOW)
        self.all_off()
        return
    
    def set_duty_cycle(self, x, y):
        '''Uses the x and y inputs to calculate and output the duty cycle
          for the motors, controlling the speed and trajectory of the robot
          
          Parameters:
            x (float): x-axis value (turning)
            y (float): y-axis value (speed)'''
        
        # calculate the duty cycle for each motor, also in interval [-1, 1]
        l_duty_cycle = max(min(1.0, y + x), -1.0)
        r_duty_cycle = max(min(1.0, y - x), -1.0)


        # set the direction of the motors
        if l_duty_cycle < 0:                # backward
            GPIO.output(self.left_1,GPIO.LOW)
            GPIO.output(self.left_2,GPIO.HIGH)
        elif l_duty_cycle > 0:              # forward
            GPIO.output(self.left_1,GPIO.HIGH)
            GPIO.output(self.left_2,GPIO.LOW)
        else:                               # stop
            GPIO.output(self.left_1,GPIO.LOW)
            GPIO.output(self.left_2,GPIO.LOW)
        
        if r_duty_cycle < 0:                # backward
            GPIO.output(self.right_1,GPIO.HIGH)
            GPIO.output(self.right_2,GPIO.LOW)
        elif r_duty_cycle > 0:              # forward
            GPIO.output(self.right_1,GPIO.LOW)
            GPIO.output(self.right_2,GPIO.HIGH)
        else:                               # stop
            GPIO.output(self.right_1,GPIO.LOW)
            GPIO.output(self.right_2,GPIO.LOW)

        # set the duty cycle for the motors, abs(duty_cycle) forces the
        # interval on [0, 1]. the sign only specifies direction
        # which is handled above
        self.left_pwm.ChangeDutyCycle(abs(l_duty_cycle))
        self.right_pwm.ChangeDutyCycle(abs(r_duty_cycle))
            