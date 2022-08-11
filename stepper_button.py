#!/usr/bin/python

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
control_pins = [7,11,13,15]

for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)

ledPin = 12
buttonPin = 16

GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]

# 1024 steps is 90 degrees
# 4096 steps is 360 degrees

deg1 = int(50 * 11.3777777777 / 8)
deg2 = int((360-50) * 11.3777777777 /8)

while True:
  buttonState = GPIO.input(buttonPin)
  if buttonState == False:
    GPIO.output(ledPin, GPIO.HIGH)

    for step in range(0,deg1):
      for halfstep in range(7,-1,-1):
        for pin in range(4):
          GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
        time.sleep(0.002)

    time.sleep(1)

    for step in range(deg2):
      for halfstep in range(7,-1,-1):
        for pin in range(4):
          GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
        time.sleep(0.002)

  else:
    GPIO.output(ledPin, GPIO.LOW)
    for pin in control_pins:
      GPIO.output(pin, GPIO.LOW)

GPIO.cleanup()

