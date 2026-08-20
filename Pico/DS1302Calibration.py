from machine import RTC, Pin
import time
import ds1302

picoRTC = RTC()
timestamp = picoRTC.datetime()

dsRTC = ds1302.DS1302(Pin(13), Pin(12), Pin(11))
dsRTC.start()
dsRTC.date_time(timestamp[:7])


print(timestamp)
print(dsRTC.date_time())
time.sleep(1)
print(dsRTC.date_time())

eventDate = "-".join([str(dsRTC.day()), str(dsRTC.month()), str(dsRTC.year())[-2:]])
eventTime = ":".join([str(dsRTC.hour()), "0" + str(dsRTC.minute()) if dsRTC.minute() < 10 else str(dsRTC.minute())])
print(eventDate, eventTime)
