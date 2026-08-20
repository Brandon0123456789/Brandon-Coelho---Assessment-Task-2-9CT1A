# Assessment Task 2: MECHATRONICS DOCUMENTATION
## Requirements Outline

### Defining the Purpose
-------- The Need --------

Living in a multiple story home means I spend a lot of time downstairs, leaving my upstairs bedroom unattended. Family members, guests and friends regularly go upstairs and enter my room without warning. Because I am on a different floor, I cannot see or hear when someone enters my space leaving me unaware. This has caused a big issue with privacy as people often disturb my room layout and touch valuable items without me knowing.

-------- Proposed Solution --------

An open loop security system shines a laser into a light detector triggering a buzzing noise when the beam is blocked to alert the intruder that their being logged. To stop someone from unplugging the device, the memory overwrites the time every minute while the room is occupied but locks the time when they exit. This means if the system is turned off the memory still retains the very last time it was active, letting you know exactly when it stopped working.

### Key Actions
 - Laser shines into a light detector triggering a buzzing noise.
 - While room is occupied, the memory overwrites the time every minute but saves the final time the moment they exit. 
 - If switched off the memory retains the very last time it was active


### Functional Requirements
The functional requirements for my security system list the key actions the mechanism needs to follow to detect intrusions and record important information:
 
Buzzer Output - The system needs to activate a buzzer the exact moment the laser beam is broken and the light detector is triggered to alert the intruder that the logging has started. This will hopefully add extreme paranoia onto the suspect.

Memory System Process - Every minute the system should delete the last time that was stored and replace it with a new one so the memory always stays updated. 

Time Logging Process - It must record and log the time the person leaves the room so the user knows exactly when the intruder left.

Data Storing Process -  If system is switched off it must retain the very last time it was active so the user can be notified.


### Test Cases
#### Buzzer Output:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| Laser beam untouched | Light detector continuously recieves the laser light | System waits and does not trigger the buzzer |
| Intruder enters rooms | Laser beam is broken; light detector is triggered | Buzzer activates instantly to alert intruder. |

#### Time Logging Process:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| Intruder inside room | Laser beam stays broken while person is inside | System waits and does not log a final time yet |
| Intruder leaves room | Laser beam is restored; light detector recieves light again | System captures the exact current time as the final time. |

#### Memory System Process:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| Intruder inside room | Laser beam stays broken as time passes | System overwrites the previous time; replaces it with the current time in the memory |
| Intruder leaves room | Laser beam is restored | System stops deleting, retains the final exit time and saves it. |

#### Data Storing Process:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| System is turned off | Cables and wires are disconnected or switches are turned off | System completely shuts down, but the final time is kept safe in the memory variable |
| System is turned back on | Cables and wires are connected and switches are turned on | System powers up and successfully displays the final time before the shutdown. |


### Non-Functional Requirements
The non-functional requirements for my security system list the performance expectations, speed, and accuracy the mechanism must sustain to achieve it's goal of running effectively and being reliable:

Efficiency - The system must run smoothly so that updating the memory every minute doesnt slow down/freeze the device.

Response Time - The buzzer must work within 0.5 seconds of the laser beam being broken so the intruder is alerted instantly.

Accuracy - The light detector must have 100% accuracy in distinguishing between the laser light and a normal bedroom light so it never starts a false alarm.




## Algorithms

### Flowchart (Two Subroutines and Mainline Routine)
![alt text](Flowchart.png)


### Psuedocode
START

    --- System Setup ---
    Set up system and memory variables
    Turn system ON
    Set alarm state to ON
    Turn laser ON
    Run Minute_logging()

    --- Main Monitoring ---
    LOOP forever
        Check light detector
        IF laser is NOT blocked THEN
            INPUT 'Continue monitoring?'
                IF answer == NO THEN
                    Turn system OFF
                    EXIT LOOP
                ELSE
                    Go back to checking light detector
                ENDIF

        ELSE IF laser is blocked THEN
            Run Intrusion_Logging()
            INPUT 'Continue monitoring?'
                IF answer == NO THEN
                    Turn system OFF
                    EXIT LOOP
                ELSE
                    Go back to checking light detector
                ENDIF
        ENDIF
    ENDLOOP

END


START Minute_logging()
    
    LOOP forever
        INPUT 'Is system ON?'
            IF answer == YES THEN
                Record current time
                Save time to memory variable
                Wait 1 minute

            ELSE
                Wait 1 minute
                END MinuteLogging
            ENDIF
    ENDLOOP

END Minute_logging


Start Intrusion_logging()
    
    Record intrusion time
    Activate buzzer
    Save intrusion time to memory
    END IntrusionLogging

END Intrusion_logging




## Development and Integration

```Python

from machine import Pin, ADC, PWM
import _thread
import time

def logTime(logType): # Takes the type of time log and logs it
    if logType == "laserBlocked":
        with open('LogFiles/DoorLog.txt', 'a') as DoorLog:
            DoorLog.write(f"Door OPENED at {timestamp}\n")
    elif logType == "laserClear":
        with open('LogFiles/DoorLog.txt', 'a') as DoorLog:
            DoorLog.write(f"Door CLOSED at {timestamp}\n")
    elif logType == "status":
        with open('LogFiles/StatusLog.txt', 'w') as StatusLog:
            StatusLog.write(f"{timestamp} OPERATIONAL")
    elif logType == "shutdown":
        with open('LogFiles/StatusLog.txt', 'w') as StatusLog:
            StatusLog.write(f"{timestamp} AUTHORISED SHUTDOWN")

def statusLogThread(): # Every 5 seconds it logs the status of the device, so I know when it was last on
    with logLock:
        logTime("status")
    time.sleep(5)

def turnOn(device, tone=None): # Turns on a device but first checks whether or not stopSystem is True. If it is, it will not turn anything on
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
    elif action == "incorrectPassword":
        turnOn("buzzer", 156) # Eb3
        time.sleep(0.3)
        buzzer.duty_u16(0)
        turnOn("buzzer", 98) # G2
        time.sleep(0.5)
        buzzer.duty_u16(0)


laserPin = Pin(16, Pin.OUT)
lightDetector = ADC(Pin(26))
buzzer = PWM(Pin(17))
timestamp = None
isLaserClear = True
logLock = _thread.allocate_lock()
buzzLock = _thread.allocate_lock()
_thread.start_new_thread(statusLogThread, ())

laserPin.value(1)
time.sleep(0.5) # Time for the LDR to detect the laser
while isLaserClear: # Technically I don't need to use isLaserClear as a condition, but it makes it easier to identify the loops
    if lightDetector.read_u16() < 40000:
        laserPin.value(0)
        with logLock: # Log before buzzing because buzzing takes time and I need logging to be done at detection
            logTime("laserBlocked")
        with buzzLock:
            buzz("doorAlarm")
        isLaserClear = False
    time.sleep_ms(20)
       
while not isLaserClear:
    time.sleep(5)
    turnOn("laserPin")
    time.sleep(0.5)
    if lightDetector.read_u16() < 40000:
        laserPin.value(0)
    else: # The laser will be kept on
        with logLock:
            logTime("laserClear")
        isLaserClear = True

```




## Testing and Debugging

### Test Cases
#### Buzzer Output:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| Laser beam untouched | Light detector continuously recieves the laser light | System waits and does not trigger the buzzer |
| Intruder enters rooms | Laser beam is broken; light detector is triggered | Buzzer activates instantly to alert intruder. |


WRITE A PARAGRAPH EVALUATING


#### Time Logging Process:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| Intruder inside room | Laser beam stays broken while person is inside | System waits and does not log a final time yet |
| Intruder leaves room | Laser beam is restored; light detector recieves light again | System captures the exact current time as the final time. |


WRITE A PARAGRAPH EVALUATING


#### Memory System Process:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| Intruder inside room | Laser beam stays broken as time passes | System overwrites the previous time; replaces it with the current time in the memory |
| Intruder leaves room | Laser beam is restored | System stops deleting, retains the final exit time and saves it. |


WRITE A PARAGRAPH EVALUATING


#### Data Storing Process:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| System is turned off | Cables and wires are disconnected or switches are turned off | System completely shuts down, but the final time is kept safe in the memory variable |
| System is turned back on | Cables and wires are connected and switches are turned on | System powers up and successfully displays the final time before the shutdown. |


WRITE A PARAGRAPH EVALUATING


### Final Product

Film a video of your final product working. Include this in your Github repo if it fits, or submit separately to Google Classroom.

ALREADY SENT IT TO GOOGLE CLASSROOM!!!




## Evaluation

### Peer Evaluation: PMI
| Person | Plus | Minus | Implication |
|--------|------|-------|-------------|
| Liam S | Very interesting concept, and I like the logs of when the door is open, closed, and operation statues. | Uhhhh, I don't really have much here, I'm just wondering whether the 5 second time intervals is too slow, also the wires are a little messy, but that's to be expected. | 9/10 project, 5 second interval might be an issue, but it's probably just me. Overall, very good |
| Fayaaz K | The machine works extremely well, and the checking of when the system was operational is a really good idea, as users can check if the door-logger was on or not | Not really any major issues I can note, the 5 second interval might be a bit too long | The overall idea and execution of said idea works extremely well and meets the functional and non-functional requirements well |   
