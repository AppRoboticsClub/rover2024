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
speed = 0

def turn(value):
    global dutyL, dutyR
    if value < 0:  # Stationary turn
        # Both wheels spin in opposite directions
        if value == 1:        # Rotate right
            GPIO.output(pinReverseL, False)
            GPIO.output(pinReverseR, True)
        else:                 # Rotate left
            GPIO.output(pinReverseL, True)
            GPIO.output(pinReverseR, False)
        motorLServo.ChangeDutyCycle(speed)
        motorRServo.ChangeDutyCycle(speed)
        dutyL = dutyR = speed
    elif value > 0:  # Moving turn
        if not isReversed:  # Forward turn
            # The wheel on the side of the turn stops; the opposite wheel drives forward
            GPIO.output(pinReverseL, False)
            GPIO.output(pinReverseR, False)
            if value == 1:  # Turn right
                motorLServo.ChangeDutyCycle(speed)
                motorRServo.ChangeDutyCycle(0)
                dutyL, dutyR = speed, 0
            else:           # Turn left
                motorLServo.ChangeDutyCycle(0)
                motorRServo.ChangeDutyCycle(speed)
                dutyL, dutyR = 0, speed
        else:               # Backwards turn
            # The wheel on the side of the turn stops; the opposite wheel drives backward
            if value == 1:    # Turn right
                GPIO.output(pinReverseL, True)
                GPIO.output(pinReverseR, False)
                motorLServo.ChangeDutyCycle(speed)
                motorRServo.ChangeDutyCycle(0)
                dutyL, dutyR = speed, 0
            else:             # Turn left
                GPIO.output(pinReverseL, False)
                GPIO.output(pinReverseR, True)
                motorLServo.ChangeDutyCycle(0)
                motorRServo.ChangeDutyCycle(speed)
                dutyL, dutyR = 0, speed
            
    else:  # No turn
        motorLServo.ChangeDutyCycle(speed)
        motorRServo.ChangeDutyCycle(speed)
        dutyL = dutyR = speed

    print(f"Turning: {l_speed} -- {r_speed} (speed={speed})(value={value})")

def acc(value):
    global isReversed, speed, dutyL, dutyR
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

