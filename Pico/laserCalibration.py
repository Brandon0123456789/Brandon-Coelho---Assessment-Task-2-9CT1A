from machine import Pin, ADC
import time
laserPin = Pin(16, Pin.OUT)
lightDetectorPin = ADC(26)
laserPin.value(1)
try:
    while True:
        print(lightDetectorPin.read_u16())
        time.sleep_ms(250)
finally:
    laserPin.value(0)