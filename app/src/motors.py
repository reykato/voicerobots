import RPi.GPIO as GPIO          
import time

class Motors:
    MAX_FREQUENCY = 1000

    def __init__(self, left_dir, left_step, right_dir, right_step):
        '''
        The Motors object abstracts GPIO initialization and PWM
        signal management to provide functions for moving the robot.

        Parameters:
            - left_pins ([int]): pins which connect to left motor [in1, in2, in3, in4]
            - right_pins ([int]): pins which connect to right motor [in1, in2, in3, in4]
        '''

        self.left_dir = left_dir
        self.left_step = left_step
        self.right_dir = right_dir
        self.right_step = right_step

        # setup motor control pins as outputs
        GPIO.setmode(GPIO.BCM)
        GPIO.output(left_dir, GPIO.LOW)
        GPIO.output(right_dir, GPIO.LOW)
        
        self.left_pwm = GPIO.PWM(left_step, 0)
        self.right_pwm = GPIO.PWM(right_step, 0) 

        self.left_pwm.start(50)
        self.right_pwm.start(50)


    def set_stepper_speed(self, x, y):
        # Calculate motor speeds 
        left_speed = (y + x) / 2  
        right_speed = (y - x) / 2

        # Ensure motor speeds are within valid range [-1, 1]
        left_speed = max(min(left_speed, 1), -1)  
        right_speed = max(min(right_speed, 1), -1)

        self.left_pwm.ChangeFrequency(self.MAX_FREQUENCY*left_speed)
        self.left_pwm.ChangeFrequency(self.MAX_FREQUENCY*right_speed)

    def set_duty_cycle(self, x, y):
        '''
        Uses the x and y inputs to calculate and output the duty cycle
        for the motors, controlling the speed and trajectory of the robot
          
        Parameters:
            - x (float [-1, 1]): x-axis value (turning speed)
            - y (float [-1, 1]): y-axis value (forward/backward speed)
        '''
        
        # calculate the duty cycle for each motor, also in interval [-1, 1]
        l_duty_cycle = max(min(1.0, y - x), -1.0)
        r_duty_cycle = max(min(1.0, y + x), -1.0)
        

        # set the direction of the motors
        if r_duty_cycle < 0:                # backward
            GPIO.output(self.left_1,GPIO.LOW)
            GPIO.output(self.left_2,GPIO.HIGH)
        elif r_duty_cycle > 0:              # forward
            GPIO.output(self.left_1,GPIO.HIGH)
            GPIO.output(self.left_2,GPIO.LOW)
        else:                               # stop
            GPIO.output(self.left_1,GPIO.LOW)
            GPIO.output(self.left_2,GPIO.LOW)
        
        if l_duty_cycle < 0:                # backward
            GPIO.output(self.right_1,GPIO.HIGH)
            GPIO.output(self.right_2,GPIO.LOW)
        elif l_duty_cycle > 0:              # forward
            GPIO.output(self.right_1,GPIO.LOW)
            GPIO.output(self.right_2,GPIO.HIGH)
        else:                               # stop
            GPIO.output(self.right_1,GPIO.LOW)
            GPIO.output(self.right_2,GPIO.LOW)

        # set the duty cycle for the motors, abs(duty_cycle) forces the
        # interval on [0, 1]. the sign only specifies direction
        # which is handled above
        self.left_pwm.ChangeDutyCycle(abs(l_duty_cycle*100*self.SPEED_LEFT))
        self.right_pwm.ChangeDutyCycle(abs(r_duty_cycle*100*self.SPEED_RIGHT))
            