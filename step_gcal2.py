#!/usr/bin/python -OO

"""Script to control an automated cat food dispenser. Stepper motor rotates thru 80 degrees then returns to resting position. This can be triggered by a button press or within 5 minutes of a calendar event."""

__author__ = "Rachael Stentiford"

import time
import datetime
import urllib.request
import re
import sys
import RPi.GPIO as GPIO

iCalUrl = 'https://calendar.google.com/calendar/ical/ohuvledfpis079ab01r97mqpqk%40group.calendar.google.com/private-b9e1cd2325b1b573fda61b57fc4704e4/basic.ics'

control_pins = [7,11,13,15]
ledPin = 12
buttonPin = 16
deg1 = int(90 * 11.3777777777 / 8)
deg2 = int(90 * 11.3777777777 /8)
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

#setup raspberryPi pins
GPIO.setmode(GPIO.BOARD)
for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#function to move stepper motor fowards by angle deg1 and backwards by angle deg2
def feedThatMoo(currenttime):
  print('Feeding the Moo at ', currenttime)
  GPIO.output(ledPin, GPIO.HIGH)
  for step in range(0,deg1):
    for halfstep in range(7,-1,-1):
      for pin in range(4):
        GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
      time.sleep(0.001)

  time.sleep(0.5)

  for step in range(deg2):
    for halfstep in range(8):
      for pin in range(4):
        GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
      time.sleep(0.001)

  GPIO.output(ledPin, GPIO.LOW)
  for pin in control_pins:
      GPIO.output(pin, GPIO.LOW)

def main():
  # initialize current time
  currenttime = datetime.datetime.utcnow()
  nextcheck = datetime.timedelta(minutes=5)
  nextchecktime = currenttime

  # periodicaly check the calendar and find upcoming events
  while True:
    currenttime = datetime.datetime.utcnow()
    try:
      if currenttime>=nextchecktime:
        nextchecktime = currenttime+nextcheck

        print(currenttime, ' Checking the calendar. I will next check at: ', nextchecktime)
        req = urllib.request.Request(iCalUrl)
        response = urllib.request.urlopen(req)

        for line in response.readlines():
          string = line.rstrip().decode('utf-8')

          if bool(re.match("^DTSTART:", string)):
            splt = string.split(':')
            starttime = datetime.datetime.strptime(splt[1], "%Y%m%dT%H%M%SZ")
            if (starttime > currenttime) and (starttime <= currenttime+nextcheck):
              feedThatMoo(currenttime)
    except:
      print("An exception occurred")

    # check for button press
    buttonState = GPIO.input(buttonPin)
    if buttonState == False:
      feedThatMoo(currenttime)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nExiting application\n')
        sys.exit(0)


