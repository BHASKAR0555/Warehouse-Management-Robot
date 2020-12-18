import RPi.GPIO as GPIO                    #Import GPIO library
import time

#Import time library
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)                    # programming the GPIO by BCM pin numbers

TRIG = 7
ECHO = 11


m11=33
m12=31
m21=35
m22=37

GPIO.setup(TRIG,GPIO.OUT)                  # initialize GPIO Pin as outputs
GPIO.setup(ECHO,GPIO.IN)                   # initialize GPIO Pin as input
#GPIO.setup(led,GPIO.OUT)                  

GPIO.setup(m11,GPIO.OUT)
GPIO.setup(m12,GPIO.OUT)
GPIO.setup(m21,GPIO.OUT)
GPIO.setup(m22,GPIO.OUT)

#GPIO.output(led, 1)

time.sleep(5)



def forward():
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 1)
    print ("Forward")

def back():
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print ("back")


while True:
 i=0
 avgDistance=0
 for i in range(5):
  GPIO.output(TRIG, False)                 #Set TRIG as LOW
  time.sleep(0.1)                                   #Delay

  GPIO.output(TRIG, True)                  #Set TRIG as HIGH
  time.sleep(0.00001)                           #Delay of 0.00001 seconds
  GPIO.output(TRIG, False)                 #Set TRIG as LOW

  while GPIO.input(ECHO)==0:              #Check whether the ECHO is LOW
       #GPIO.output(led, False)             
     pulse_start = time.time()

  while GPIO.input(ECHO)==1:              #Check whether the ECHO is HIGH
       #GPIO.output(led, False) 
    pulse_end = time.time()
  pulse_duration = pulse_end - pulse_start #time to get back the pulse to sensor

  distance = pulse_duration * 17150        #Multiply pulse duration by 17150 (34300/2) to get distance
  distance = round(distance,2)                 #Round to two decimal points
  avgDistance=avgDistance+distance

  avgDistance=avgDistance/5
  print(avgDistance)
 
  if avgDistance < 15:      #Check whether the distance is wiGPIO.setwarnings(False)thin 15 cm rangeGPIO.setwarnings(False)
     back()
     time.sleep(0.001)
    
  else:
    forward()
    time.sleep(0.001)