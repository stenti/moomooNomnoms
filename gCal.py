#!/usr/bin/python -OO

from time import gmtime, strftime
import datetime
import urllib.request
import re
import sys

iCalUrl = 'https://calendar.google.com/calendar/ical/ohuvledfpis079ab01r97mqpqk%40group.calendar.google.com/private-b9e1cd2325b1b573fda61b57fc4704e4/basic.ics'

def feedThatMoo():
 print('Feeding the Moo')

def main():
  # initialize current time
  currenttime = datetime.datetime.utcnow()
  nextcheck = datetime.timedelta(minutes=5)
  nextchecktime = currenttime

  # periodicaly check the calendar and find upcoming events
  while True:

    currenttime = datetime.datetime.utcnow()

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
            feedThatMoo()
            print(starttime)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nExiting application\n')
        sys.exit(0)
