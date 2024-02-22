import RPi.GPIO as GPIO          
import time

class Motors:
    SPEED_LEFT = 0.75
    SPEED_RIGHT = 0.75


    def __init__(self, left_1, left_2, right_1, right_2, left_enable, right_enable):
        '''
        The Motors object abstracts GPIO initialization and PWM
        signal management to provide functions for moving the robot.

        Parameters:
            - left_1 (int): pin which connects to 'in1' on the motor driver
            - left_2 (int): pin which connects to 'in2' on the motor driver
            - right_1 (int): pin which connects to 'in3' on the motor driver
            - right_2 (int): pin which connects to 'in4' on the motor driver
            - left_enable (int): pin which connects to 'enA' on the motor driver
            - right_enable (int): pin which connects to 'enB' on the motor driver
        '''

        # l1 and l2 are the two connections to the left motor
        self.left_1 = left_1
        self.left_2 = left_2

        # l1 and l2 are the two connections to the right motor
        self.right_1 = right_1
        self.right_2 = right_2

        # l_en is the 'enable' connection to the left motor
        # r_en is the 'enable' connection to the right motor
        self.left_enable = left_enable
        self.right_enable = right_enable

        # setup motor control pins as outputs
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

        # start the PWM signal at 100% duty cycle
        self.left_pwm.start(100)
        self.right_pwm.start(100)
        
        # set all motors off
        GPIO.output(self.left_1,GPIO.LOW)
        GPIO.output(self.left_2,GPIO.LOW)
        GPIO.output(self.right_1,GPIO.LOW)
        GPIO.output(self.right_2,GPIO.LOW)
    
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
            