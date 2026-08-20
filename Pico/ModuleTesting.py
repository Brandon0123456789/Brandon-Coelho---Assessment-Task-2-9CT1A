from machine import ADC, Pin, PWM
import time

print("1. Laser")
print("2. Two colour LED")
print("3. Passive buzzer")
print("4. Light dependent resistor")
moduleInput = int(input("Which module would you like to test? "))

if moduleInput == 1:
    laser = Pin(16, Pin.OUT)
    while True:
        laser.value(1)
        time.sleep(3)
        laser.value(0)
        time.sleep(1)        
    
elif moduleInput == 2:
    greenLed = Pin(5, Pin.OUT)
    redLed = Pin(4, Pin.OUT)
    while True:
        redLed.value(1)
        time.sleep(1)
        redLed.value(0)
        greenLed.value(1)
        time.sleep(1)
        greenLed.value(0)
        break
        
elif moduleInput == 3:
    buzzer = PWM(Pin(16))
    while True:
        buzzer.freq(440) # A4
        time.sleep(0.5)
        buzzer.duty_u16(32728)
        time.sleep(0.5)
        buzzer.duty_u16(0)
        buzzer.freq(494) # B4
        time.sleep(0.5)
        buzzer.duty_u16(32728)
        time.sleep(0.5)
        buzzer.duty_u16(0)
        buzzer.freq(523) # C5
        time.sleep(0.5)
        buzzer.duty_u16(32728)
        time.sleep(0.5)
        buzzer.duty_u16(0)

elif moduleInput == 4:
    laser = Pin(16, Pin.OUT)
    laser.value(1) 
    analogPin = ADC(Pin(26))
    while True:
        LDRvalue = analogPin.read_u16()
        print(LDRvalue)
        time.sleep_ms(100)
