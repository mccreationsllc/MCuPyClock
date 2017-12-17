# main.py

import ntptime
import utime
import time

months = ['Jan',
          'Feb',
          'Mar',
          'Apr',
          'May',
          'June',
          'July',
          'Aug',
          'Sept',
          'Oct',
          'Nov',
          'Dec']

days = ['Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday']


def cleartime():
    for x in range(128):
        for y in range(12):
            oled.pixel(x, y, 0)
    oled.show()


def clearday():
    for x in range(128):
        for y in range(12):
            oled.pixel(x, y + 12, 0)
    oled.show()


def cleardate():
    for x in range(128):
        for y in range(12):
            oled.pixel(x, y + 24, 0)
    oled.show()


def clock():
    oledclear()
    global starttime
    starttime = utime.localtime()
    while True:
        try:
            h = utime.localtime()[3]  # Sets Hour output
            if h > 5:  # Sets EST Time from GMT
                h -= 5
            if h <= 5:  # Sets EST Time from GMT
                h = 24 - (5 - h)
            if h >= 12:
                meridian = 'pm'
            else:
                meridian = 'am'
            if h > 12:  # adjusts for 12hr time
                h -= 12
            if h == 0:
                h = 12

            m = utime.localtime()[4]  # Sets Minute output
            if m < 10:  # Pads the minute with a zero when in single digits
                m = '%02d' % m
            s = utime.localtime()[5]  # Sets seconds output
            if s < 10:  # Pads the seconds with a zero when in single digits
                s = '%02d' % s
            d = utime.localtime()[2]  # Sets day output
            M = utime.localtime()[1]  # Sets month output
            y = utime.localtime()[0]  # Sets year output
            w = utime.localtime()[6]  # Sets the day of the week
            clocktime = '%s:%s:%s' % (h, m, s) + meridian
            date = months[M - 1] + ' ' + str(d) + ',' + str(y)
            if(s == 30):
                print('Updating Time')
                ntptime.settime()
                gc.collect()
                clocktime = clocktime + '*'
            cleartime()
            oledtext(clocktime, 30, 1)
            oledtext(days[w], 42, 12)
            oledtext(date, 18, 24)
            if w != starttime[6]:
                clearday()
                oledtext(days[w], 42, 13)
            if d != starttime[2]:
                cleardate()
                oledtext(date, 18, 25)
            time.sleep(1)
        except OSError:
            clock()


if __name__ == '__main__':
    clock()
