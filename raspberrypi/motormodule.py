from numpy import mat
import RPi.GPIO as GPIO
from time import sleep


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class Motor:
    def __init__(self, enA, in1, in2, enB, in3, in4):
        self.enA = enA
        self.in1 = in1
        self.in2 = in2
        self.enB = enB
        self.in3 = in3
        self.in4 = in4
        GPIO.setup(self.enA, GPIO.OUT)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.enB, GPIO.OUT)
        GPIO.setup(self.in3, GPIO.OUT)
        GPIO.setup(self.in4, GPIO.OUT)
        self.pwmA = GPIO.PWM(self.enA, 1000)
        self.pwmA.start(0)
        self.pwmB = GPIO.PWM(self.enB, 1000)
        self.pwmB.start(0)

    def forward(self, dist=60):
        DEFAULT_DIST = 60
        DEFAULT_TIME = 1
        time = DEFAULT_TIME * (dist / DEFAULT_DIST)
        self.pwmA.ChangeDutyCycle(100)
        self.pwmB.ChangeDutyCycle(100)
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.HIGH)
        GPIO.output(self.in4, GPIO.LOW)
        sleep(time)
    
    def forward_with_time(self, time=0.01):
        self.pwmA.ChangeDutyCycle(100)
        self.pwmB.ChangeDutyCycle(100)
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.HIGH)
        GPIO.output(self.in4, GPIO.LOW)
        sleep(time)
        
    def backward(self, dist=60):
        DEFAULT_DIST = 60
        DEFAULT_TIME = 1
        time = DEFAULT_TIME * (dist / DEFAULT_DIST)
        self.pwmA.ChangeDutyCycle(100)
        self.pwmB.ChangeDutyCycle(100)
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.HIGH)
        sleep(time)
        
    def backward_with_time(self, time=0.01):
        self.pwmA.ChangeDutyCycle(100)
        self.pwmB.ChangeDutyCycle(100)
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.HIGH)
        sleep(time)

    def left(self, time=0.01):
        self.pwmA.ChangeDutyCycle(100)
        self.pwmB.ChangeDutyCycle(100)
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)
        GPIO.output(self.in3, GPIO.HIGH)
        GPIO.output(self.in4, GPIO.LOW)
        sleep(time)

    def right(self, time=0.01):
        self.pwmA.ChangeDutyCycle(100)
        self.pwmB.ChangeDutyCycle(100)
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.HIGH)
        # 0.0258
        # 180 derece 1.322
        # 90 derece 0.672
        # 0.02405
        sleep(time)

    def stop(self, time=0):
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
        sleep(time)

