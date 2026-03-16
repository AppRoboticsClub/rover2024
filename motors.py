import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # use broadcom pin numbering (not board pin numbering)


# Define pins
pinMotorL = 13 # GPIO Pin for motorL # previously motor1
pinMotorR = 12 # GPIO Pin for motorR # previously motor2
pinReverseL = 5 # pin for reverse left
pinReverseR = 6 # pin for reverse right

forwardDC = 8
backwardDC = 4
turnStillDC = 6

class Motor:
    def _setup(self):
        GPIO.setup(self._motor_pin, GPIO.OUT)

        GPIO.setup(self._reverse_pin, GPIO.OUT)

        GPIO.output(self._reverse_pin, self._reverse)

        self._motor_servo = GPIO.PWM(self._motor_pin, self._freq)
        self._motor_servo.start(self._dc)
        self._running = True
        self._motor_servo.ChangeDutyCycle(self._dc)

    def __init__(self, motor_pin, reverse_pin, reverse=False, starting_freq=1000, starting_dc=0, setup=True):
        self._motor_pin = motor_pin
        self._reverse_pin = reverse_pin
        self._freq = starting_freq
        self._dc = starting_dc
        self._reverse = reverse

        if setup:
            self._setup()

    def stop(self):
        self._motor_servo.stop()
        self._running = False

    def start(self):
        self._motor_servo.start(self._dc)
        self._running = True

    @property
    def reverse(self):
        return self._reverse

    @reverse.setter
    def reverse(self, value):
        val = bool(value)

        if val != self._reverse:
            self._reverse = val
            GPIO.output(self._reverse_pin, self._reverse)

    @property
    def dc(self):
        return self._dc

    @dc.setter
    def dc(self, value):
        val = float(value)

        if val < 0 or val > 100:
            raise ValueError("Duty cycle should be between 0.0 and 100.0")

        self._dc = val
        if self._running:
            self._motor_servo.ChangeDutyCycle(val)

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, value):
        val = float(value)

        if val < 50 or val > 20000:
            raise ValueError("Frequency should be between 50Hz and 20kHz")
       
        self._freq = val
        if self._running:
            self._motor_servo.ChangeFrequency(self._freq)

motorL = Motor(pinMotorL, pinReverseL)
motorR = Motor(pinMotorR, pinReverseR)

def move(straight, turn):
    if straight < -1 or straight > 1 or turn < -1 or turn > 1:
        raise ValueError('Invalid value')

    match (straight, turn):
        case (0,0):
            motorL.dc = 0
            motorR.dc = 0
        case (0,_): # Turning while stationary
            motorL.reverse = turn == -1
            motorR.reverse = turn == 1

            motorL.dc = turnStillDC
            motorR.dc = turnStillDC
        case (_,0): # Going straight
            motorL.reverse = straight == -1
            motorR.reverse = straight == -1

            dc = backwardDC if motorL.reverse else forwardDC
            motorL.dc = dc
            motorR.dc = dc
        case _: # Turning while moving
            motorL.reverse = turn == -1
            motorR.reverse = turn == 1

            dc = forwardDC if straight == 1 else backwardDC

            motorL.dc = 0 if motorL.reverse else dc
            motorR.dc = 0 if motorR.reverse else dc

