from machine import Pin, ADC, PWM
import ds1302
import _thread
import time

def getTime(timeFormat): # Quickly takes the date or time from the DS1302 RTC
    if timeFormat == "date":
        eventDate = "-".join([str(rtc.day()), str(rtc.month()), str(rtc.year())[-2:]]) # DD-MM-YY
        return eventDate
    elif timeFormat == "time":
        eventTime = ":".join([str(rtc.hour()), "0" + str(rtc.minute()) if rtc.minute() < 10 else str(rtc.minute())]) # Add a 0 before the number if it is before 10 (less than 2 digits)
        return eventTime

def logTime(logType): # Takes the type of time log and logs it
    if logType == "laserBlocked":
        with open(f'LogFiles/DoorLog{getTime("date")}.txt', 'a') as DoorLog: # Appends
            DoorLog.write(f'Door OPENED at {getTime("time")}\n')
    elif logType == "laserClear":
        with open(f'LogFiles/DoorLog{getTime("date")}.txt', 'a') as DoorLog: # Appends
            DoorLog.write(f'Door CLOSED at {getTime("time")}\n')
    elif logType == "status":
        with open('LogFiles/StatusLog.txt', 'w') as StatusLog: # Writes
            StatusLog.write(f'{getTime("time")} OPERATIONAL')

def turnOn(device, tone=None): # Turns on either laser or buzzer. The 'tone' positional parameter is not required to be satisfied, as its default is 'None'
    if device == "laserPin":
        laserPin.value(1)
    elif device == "buzzer":
        buzzer.freq(tone)
        buzzer.duty_u16(32728) # A 50% duty cycle makes the buzzer produce sound symmetrically, making it as loud, clear, and efficent as possible

def buzz(action): # Different buzzer noises for different scenarios
    if action == "doorAlarm":
        for i in range(3):
            turnOn("buzzer", 440) # A4
            time.sleep(0.5)
            buzzer.duty_u16(0)
            time.sleep(0.5)

def statusLogThread(): # Every 5 seconds it logs the status of the device, so I know when my device was last on
    while True:
        with logLock:
            logTime("status")
        time.sleep(5)

laserPin = Pin(16, Pin.OUT)
lightDetector = ADC(Pin(26))
buzzer = PWM(Pin(17))
rtc = ds1302.DS1302(Pin(13), Pin(12), Pin(11))
isLaserClear = True
doorAlarm = False # Whether the door alarm was just played. Since it takes 3 seconds to play, the program will check if the laser is clear 3 seconds earlier on the first attempt
logLock = _thread.allocate_lock()
buzzLock = _thread.allocate_lock()
_thread.start_new_thread(statusLogThread, ())

try:
    laserPin.value(1)
    time.sleep(0.5) # Time for the LDR to detect the laser
    while True:
        while isLaserClear: # Technically I don't need to use isLaserClear as a condition, but it makes it easier to identify the loops
            if lightDetector.read_u16() < 55000:
                laserPin.value(0)
                with logLock: # Log before buzzing because buzzing takes time and I need logging to be done at detection
                    logTime("laserBlocked")
                with buzzLock:
                    buzz("doorAlarm")
                    doorAlarm = True
                isLaserClear = False
            time.sleep_ms(20)
                
        while not isLaserClear:
            if doorAlarm:
                time.sleep(2) # Checks if the laser is clear every 5 seconds
                doorAlarm = False
            else:
                time.sleep(5)
            turnOn("laserPin")
            time.sleep(0.5)
            if lightDetector.read_u16() < 55000:
                laserPin.value(0)
            else: # The laser will be kept on
                with logLock:
                    logTime("laserClear")
                isLaserClear = True
finally:
    laserPin.value(0)
    buzzer.duty_u16(0)
'''
This finally clause turns off the laser and buzzer when the system is turned off normally.
If I don't do this the GPIO or PWM pins will stay on.
If the power is just ripped out instead then the pins will just automatically be set to off when it turns on again.
'''
