from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

camera = PiCamera()
image_width = 640
image_height = 480
camera.resolution = (image_width, image_height)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(image_width, image_height))
center_image_x = image_width / 2
center_image_y = image_height / 2
minimum_area = 250
maximum_area = 100000

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

MOTOR1B=40
MOTOR1E=38
MOTOR2B=36
MOTOR2E=32
MOTOR3B=16
MOTOR3E=18


GPIO_TRIGGER1 = 37      #Left ultrasonic sensor
GPIO_ECHO1 = 35

GPIO_TRIGGER2 = 31      #Front ultrasonic sensor
GPIO_ECHO2 = 29

GPIO_TRIGGER3 = 11      #Right ultrasonic sensor
GPIO_ECHO3 = 13

GPIO.setup(MOTOR1B,GPIO.OUT)
GPIO.setup(MOTOR1E,GPIO.OUT)
GPIO.setup(MOTOR2B,GPIO.OUT)
GPIO.setup(MOTOR2E,GPIO.OUT)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(MOTOR3B,GPIO.OUT)
GPIO.setup(MOTOR3E,GPIO.OUT)

GPIO.setup(GPIO_TRIGGER1,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO1,GPIO.IN)      # Echo
GPIO.setup(GPIO_TRIGGER2,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO2,GPIO.IN)
GPIO.setup(GPIO_TRIGGER3,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO3,GPIO.IN)
GPIO.setup(LED_PIN,GPIO.OUT)

pwm1 = GPIO.PWM(3,1000)
pwm1.start(150)
pwm2 = GPIO.PWM(5,1000)
pwm2.start(150)

#####################################################################


def forward():
    GPIO.output(MOTOR1B, GPIO.LOW)
    GPIO.output(MOTOR1E, GPIO.HIGH)
    GPIO.output(MOTOR2B, GPIO.LOW)
    GPIO.output(MOTOR2E, GPIO.HIGH)

def leftturn():
    GPIO.output(MOTOR1B, GPIO.HIGH)
    GPIO.output(MOTOR1E, GPIO.LOW)
    GPIO.output(MOTOR2B, GPIO.LOW)
    GPIO.output(MOTOR2E, GPIO.LOW)

def rightturn():
    GPIO.output(MOTOR1B, GPIO.LOW)
    GPIO.output(MOTOR1E, GPIO.HIGH)
    GPIO.output(MOTOR2B, GPIO.LOW)
    GPIO.output(MOTOR2E, GPIO.LOW)

def stop():
    GPIO.output(MOTOR1B, GPIO.LOW)
    GPIO.output(MOTOR1E, GPIO.LOW)
    GPIO.output(MOTOR2B, GPIO.LOW)
    GPIO.output(MOTOR2E, GPIO.LOW)

def up():
    GPIO.output(MOTOR3B, GPIO.HIGH)
    GPIO.output(MOTOR3E, GPIO.LOW)

def down():
    GPIO.output(MOTOR3B, GPIO.LOW)
    GPIO.output(MOTOR3E, GPIO.HIGH)

def stay():
    GPIO.output(MOTOR3B, GPIO.LOW)
    GPIO.output(MOTOR3E, GPIO.LOW)


######################  ULTRASONIC SENSORS ###############################


GPIO.output(GPIO_TRIGGER1, False)
GPIO.output(GPIO_TRIGGER2, False)
GPIO.output(GPIO_TRIGGER3, False)

# Allow module to settle
def sonar(GPIO_TRIGGER,GPIO_ECHO):

    start=0
    stop=0
    # Set pins as output and input
    GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
    GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

    # Set trigger to False (Low)
    GPIO.output(GPIO_TRIGGER, False)

    # Allow module to settle
    time.sleep(0.01)

    #while distance > 5:
    #Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    begin = time.time()
    while GPIO.input(GPIO_ECHO)==0 and time.time()<begin+0.05:
        start = time.time()
    while GPIO.input(GPIO_ECHO)==1 and time.time()<begin+0.1:
        stop = time.time()

    # Calculate pulse length
    elapsed = stop-start
    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34000

    # That was the distance there and back so halve the value
    distance = distance / 2

    print(distance)
    # Reset GPIO settings
    return distance

disl = sonar(GPIO_TRIGGER1,GPIO_ECHO1) #distance  from left ultrasonic sensor
disc = sonar(GPIO_TRIGGER2,GPIO_ECHO2) #distance  from front ultrasonic sensor
disr = sonar(GPIO_TRIGGER3,GPIO_ECHO3) #distance  from right ultrasonic sensor


####################### OpenCV  ############################################


lower_color = np.array([48, 93, 71])
upper_color = np.array([112, 191, 255])

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    color_mask = cv2.inRange(hsv, lower_color, upper_color)
    color_mask = cv2.erode(color_mask, None, iterations=2)
    color_mask = cv2.dilate(color_mask, None, iterations=2)
    image2, countours, hierarchy = cv2.findContours(color_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    object_area = 0
    object_x = 0
    object_y = 0

    for contour in countours:
        x, y, width, height = cv2.boundingRect(contour)
        found_area = width * height
        center_x = x + (width / 2)
        center_y = y + (height / 2)
        if object_area < found_area:
            object_area = found_area
            object_x = center_x
            object_y = center_y
    if object_area > 0:
        ball_location = [object_area, object_x, object_y]
    else:
        ball_location = None


 ###############################################################################
 ###############################################################################



    if ball_location:
        if (ball_location[0] > minimum_area) and (ball_location[0] < maximum_area):
            if ball_location[1] > (center_image_x + (image_width/3)):
                pwm1.ChangeDutyCycle(70)
                pwm2.ChangeDutyCycle(70)
                if disr>15:
                    rightturn()
                elif disr<15:
                    forward()
                print("Turning right")
            elif ball_location[1] < (center_image_x - (image_width/3)):
                pwm1.ChangeDutyCycle(70)
                pwm2.ChangeDutyCycle(70)
                if disl>15:
                    leftturn()
                elif disl<15:
                    forward()
                print("Turning left")
            else:
                pwm1.ChangeDutyCycle(150)
                pwm2.ChangeDutyCycle(150)
                forward()
                print("Forward")
        elif (ball_location[0] < minimum_area):
            pwm1.ChangeDutyCycle(70)
            pwm2.ChangeDutyCycle(70)
            if disc>15 and disl>15 and disr>15:
                leftturn()
            elif disl<15 and disc>15:
                forward()
                time.sleep(1)
                leftturn()
            elif disc<15 and disl<15 and disr>15:
                rightturn()
            print("Target isn't large enough, searching")
        elif (ball_location[0] < minimum_area) and disc<12:
            stop()
            time.sleep(1)
            up()
            time.sleep(4)
            stay()
            print("Target large enough, stopping")

    else:
        pwm1.ChangeDutyCycle(70)
        pwm2.ChangeDutyCycle(70)
        leftturn()
        print("Target not found, searching")

    rawCapture.truncate(0)
