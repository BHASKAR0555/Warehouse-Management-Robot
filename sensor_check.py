import RPi.GPIO as GPIO                    #Import GPIO library
import time

#Import time library
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)                    # programming the GPIO by BCM pin numbers

TRIG1 = 37
ECHO1 = 35
TRIG2 = 31
ECHO2 = 29
TRIG3 = 11
ECHO3 = 13

GPIO.setup(TRIG1,GPIO.OUT)                  # initialize GPIO Pin as outputs
GPIO.setup(ECHO1,GPIO.IN)
GPIO.setup(TRIG2,GPIO.OUT)                  # initialize GPIO Pin as outputs
GPIO.setup(ECHO2,GPIO.IN)
GPIO.setup(TRIG3,GPIO.OUT)                  # initialize GPIO Pin as outputs
GPIO.setup(ECHO3,GPIO.IN)    



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
     
     
      return distance
    
    
while True:
    disc = sonar(TRIG1,ECHO1)
    print(disc)
    time.sleep(0.01)
    disr = sonar(TRIG2,ECHO2)
    print(disr)
    time.sleep(0.01)
   
    disl = sonar(TRIG3,ECHO3)
    print(disl)
    