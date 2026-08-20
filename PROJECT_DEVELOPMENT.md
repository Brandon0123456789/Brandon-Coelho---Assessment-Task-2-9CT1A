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

### Test Case Evaluation
#### Buzzer Output:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| Laser beam untouched | Light detector continuously recieves the laser light | System waits and does not trigger the buzzer |
| Intruder enters rooms | Laser beam is broken; light detector is triggered | Buzzer activates instantly to alert intruder. |


The voltage divider worked very well when we used a 10 kΩ resistor. Using it gave us the maximum possible U16 range. In dark conditions the readings averaged around 1500 while shining the laser directly at the LDR produced readings of approximately 60000. Interestingly, the reading stayed around 60000 when the laser was shining on the LDR even in both dark and very bright environments. In normal light conditions the reading dropped to around 50000. Due to this we programmed the system so that when the LDR detects a light level below 55000, it will activate.

During testing, the green buzzer stopped working so we initially used my buzzer but this also stopped working. We were then suggested to use the passive buzzer from Daniel’s engineering kit. We tested different frequencies and found that 440 Hz (A note, octave 4) worked well. We decided to keep this frequency for our final system.


#### Time Logging Process:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| Intruder inside room | Laser beam stays broken while person is inside | System waits and does not log a final time yet |
| Intruder leaves room | Laser beam is restored; light detector recieves light again | System captures the exact current time as the final time. |


When the time was first logged, the system only recorded when the person closed the door. This was because the time was overwritten every minute until the LDR detected the laser again. This meant we could not determine when the person entered the room but only when they left (this is if they even close the door). The system was also limited to one log because if someone entered the room again the previous time would be replaced by the new time.

To fix these issues, instead of overwriting the file with the 'w' tuple in the 'open()' method, we replaced it with the 'a' argument instead. The 'w' argument overwrites the existing file while 'a' adds new information to the end of the file. We also changed the system so that it records the time when the door is opened. Once the door is opened, the laser shines every five seconds. If the buzzer has just been activated it waits two seconds instead, as the buzzer runs for three seconds. The system then waits 0.5 seconds for the LDR to detect the laser. If the LDR detects the laser it remains on and waits for the door to be opened again. The same .txt file also records the time when the door is closed. This gives us a much better indication of when the door was opened and when it was closed again.

When we implemented and tested this system, the laser immediately turned off when it was tripped and a new time was added to the log. After five seconds, the laser turned on for 0.5 seconds before turning off again. However,one problem is if the intruder closes the door when they enter, the LDR will detect the laser, the laser will remain on and the system will record the time that the door was closed. Therefore, this test case was considered unsuccessful. 


#### Memory System Process:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| Intruder inside room | Laser beam stays broken as time passes | System overwrites the previous time; replaces it with the current time in the memory |
| Intruder leaves room | Laser beam is restored | System stops deleting, retains the final exit time and saves it. |


This test was successful. When the laser beam remained broken the system continued overwriting the previous time with the current time, meaning the memory always showed the most recent time. When the intruder left and the laser beam was restored the system stopped overwriting and saved the final time. This meant we could accurately record approximately when the intruder left the room.


#### Data Storing Process:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| System is turned off | Cables and wires are disconnected or switches are turned off | System completely shuts down, but the final time is kept safe in the memory variable |
| System is turned back on | Cables and wires are connected and switches are turned on | System powers up and successfully displays the final time before the shutdown. |


We needed a way to detect if someone sabotaged the system by turning it off. To do this, the system records the current time in a separate .txt file every five seconds then overwrites the previous time using the 'w' argument. If the system is turned off, the last recorded time remains in the file allowing us to see approximately when it was turned off and identify who may have interfered with it. Overall, no changes were made to our original idea.


### Final Product

Film a video of your final product working. Include this in your Github repo if it fits, or submit separately to Google Classroom.

ALREADY SENT IT TO GOOGLE CLASSROOM!!!




## Final Evaluation

### Peer Evaluation: PMI
| Person | Plus | Minus | Implication |
|--------|------|-------|-------------|
| Liam S | Very interesting concept, and I like the logs of when the door is open, closed, and operation statues. | Uhhhh, I don't really have much here, I'm just wondering whether the 5 second time intervals is too slow, also the wires are a little messy, but that's to be expected. | 9/10 project, 5 second interval might be an issue, but it's probably just me. Overall, very good |
| Fayaaz K | The machine works extremely well, and the checking of when the system was operational is a really good idea, as users can check if the door-logger was on or not | Not really any major issues I can note, the 5 second interval might be a bit too long | The overall idea and execution of said idea works extremely well and meets the functional and non-functional requirements well |   


### Final Evaluation Questions

#### Evaluate your Final Test in Relation to Functional Criteria
The system was able to detect when the door was opened and closed with no errors and it could tell the difference because when the door is opened the laser can no longer reach the LDR. The buzzer also worked really well and the data logging for the door worked perfectly. Instead of replacing the time until the door was closed, it would add the time to a .txt file when the door was both opened and closed, doing this quickly and accurately. At the last minute we changed it so that a new doorlog file would be created for each date, meaning there was one file for every day. This stopped the file from becoming too large and making it take forever to look through. The data storing process also worked very well because it could record the time every 5 seconds and overwrite the previous time once another 5 seconds had passed. This meant we could easily check when the system was last turned off and work out who may have interfered with it. It also made the system more secure because people would know that touching it could be detected. The RTC we used, the DS1302, also worked very well with the driver we found on GitHub. It kept the time accurate and the driver made it simple to read and write the time. Overall, the functional parts of the system were very successful and worked how we wanted them to.


#### Evaluate your Final Test in Relation to Non-Functional Criteria
The non-functional criteria was met to a full extent. The laser could easily differentiate between the door being opened and closed because when the door opens it blocks the laser from reaching the LDR. Every five seconds, the laser turns on for half a second to check the LDR. If it detects the laser, the door is closed and if it does not, the door is open. When the laser first turns on we give the LDR 0.5 seconds to detect it so the system does not malfunction by checking too quickly. Once the laser is detected the program checks every 20ms for better efficiency. The program also saves power by only turning the laser on every five seconds and the Pico stayed quite cool while running showing it was not under a high workload. Overall, we met all of our non-functional criteria by making the system fast, reliable, and power efficient.


#### Evaluate your Final Performance in Relation to the Identified Need
Due to the success in meeting all the functional requirements and our non-functional requirements enhancing the device, our needs where absolutely met. The system could successfully log whenever the door was opened or closed, with the added security of the data storing process. Due to it being fast, reliable and having low power requirements, it means it works to a high standard and can be something to depend upon. For example, if my friend comes into my room looking to upset my layout, the device will log when they came in and out, as well as hopefully invoke paranoia since they will realise that they are now getting logged. If they try tampering with the system, it will log when they did it leaving great evidence for me.


#### Evaluate your Project in Relation to Project Management
We managed time with our project well but sometimes fell behind by around half a week at times due to me having to go to the Ski Trip in Week 3. For the main file, we first researched what we needed which was threads and the 'open()' method. We then worked on making sure the laser and the LDR worked somewhat well, then moved on to making the log for the door and the data storing process using the '_thread' library. The whole time, the 'timestamp' variable was set to 'None', until we added the programming for the RTC, then configured the logs to fit the time. We then ran some tests to see the light level when the LDR was shone by the laser (60000), then calibrated the minimum light level required to set off the system (55000). Then we wired it up to a door and tested to see if the whole thing worked (which happened), and filmed it (Attached on the google classroom).

#### Evaluate your Project in Relation to Peer Feedback.

The peer feedback was mostly very positive with both people saying that the system worked extremely well and that the door logs and operation status were useful features. Liam gave the project a 9/10 and said that the main possible issue was the 5 second checking interval, while Fayaaz also mentioned that the 5 seconds could be a little too long. This is something we could improve in the future by making the system check more often, although the 5 second interval was made to save power. Liam also mentioned that the wires were a little messy, which is another area we could improve by organising the wiring better. Overall, the feedback showed that the project worked very well and met both the functional and non-functional requirements with only a few small improvements that could be made.

#### Justify Future Improvements you could make to your Final Product

There are a few improvements we could make to the final product in the future. One improvement would be reducing the 5 second checking interval due to both classmates mentioning that this could be a little too slow. However, this would use more power, meaning we would need to find a good balance between speed and efficiency. Another improvement would be making the wiring less messy and more organised which would make the device look cleaner and easier to work with. We could also make the device more secure so the components are better protected. These improvements would make the final product more reliable, easier to use and better overall.
