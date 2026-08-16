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


Add your first attempt as a code window in your markdown documentation:
eg: 

 ```Python 

#Enter code here

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

Include all final Thonny / VS Code files and folder structure in your Github, all test cases in your documentation, and include all commits. 
