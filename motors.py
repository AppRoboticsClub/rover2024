import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # use broadcom pin numbering (not board pin numbering)

# Define pins
pinMotorL = 13 # GPIO Pin for motorL # previously motor1
pinMotorR = 12 # GPIO Pin for motorR # previously motor2
pinReverseL = 5 # pin for reverse left
pinReverseR = 6 # pin for reverse right


# setup
# motor control pins
GPIO.setup(pinMotorL, GPIO.OUT) # set pin motorL to output
GPIO.setup(pinMotorR, GPIO.OUT) # set pin motorR to output

# reverse control pins
GPIO.setup(pinReverseL, GPIO.OUT) # set pin reverseL to output
GPIO.setup(pinReverseR, GPIO.OUT) # set pin reverseR to output
GPIO.output(pinReverseL, False) # set so no pin output, aka go forwards
GPIO.output(pinReverseR, False) # set so no pin output, aka go forwards

motorLServo = GPIO.PWM(pinMotorL, 1000) # set Motors to PWM. Change this depeneding on how your motor controller works
motorLServo.start(8)
motorRServo = GPIO.PWM(pinMotorR, 1000) # set Motors to PWM. Change this depeneding on how your motor controller works
motorRServo.start(8)
motorLServo.ChangeDutyCycle(0) # 
motorRServo.ChangeDutyCycle(0) # RPI can encounter a bug that might require this to be applied twice
dutyL = 5
dutyR = 5

isReversed = False

def turn(value):
    if value < 0:
        GPIO.output(pinReverseL, True)
        GPIO.output(pinReverseR, True)
    elif value > 0:
        GPIO.output(pinReverseL, False)
        GPIO.output(pinReverseR, False)

    l_speed = speed * (1 + value)
    r_speed = speed * (1 - value)

    motorLServo.ChangeDutyCycle(speed) # 50 Right, 0 Neutral, -50 Left
    motorRServo.ChangeDutyCycle(speed)

    print(f"Turning: {l_speed} -- {r_speed} (speed={speed})(value={value})")

    dutyL = 50 + value
    dutyR = 50 - value

    if speed < 0:
        setReverse(True)
    else:
        setReverse(False)

def acc(value):
    global isReversed
    value = value / 5
    if value < 0:
        setReverse(True)
    else:
        setReverse(False)
    # check for is reversed

    # reduce reverse speed
    if isReversed:
        value = value * -1
        value = value / 5

    # update pwm duty cycle to new value
    print(f"Changing acc() duty cycle: {value}")
    motorLServo.ChangeDutyCycle(value)
    motorRServo.ChangeDutyCycle(value)
    dutyL = value
    dutyR = value

    # update the speed
    global speed
    speed = value

def stop():
    motorLServo.stop()
    motorRServo.stop()

def start():
    motorLServo.start(dutyL)
    motorRServo.start(dutyR)

def Left(value: int):
    motorLServo.ChangeFrequence(value)
    # motorLServo.ChangeFrequency(value)

def Right(value: int):
    # motorRServo.ChangeFrequence(value)
    motorRServo.ChangeFrequency(value)

def setReverse(isRev: bool):
    '''
    - Takes a boolean value as a parameter as to whether the rover should be reversed, then updates
    the reverse pins to be on if reverse is true, and off if false
    - @param isRev: bool - The current state of the reverse button
    '''
    global isReversed
#    if isReversed == isRev:
#        return
    isReversed = isRev
    GPIO.output(pinReverseL, isRev)
    GPIO.output(pinReverseR, not isRev)

