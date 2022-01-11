#https://www.johannespetz.de/l293d-geschwindigkeit-und-richtung-von-dc-motoren-steuern/

import RPi.GPIO as GPIO

#import _fake_GPIO as GPIO
pins = [2, 3, 4, 7, 8, 9, 10, 11, 14, 15, 17, 18, 22, 23, 24, 25, 27] 


fwdPin=24
rwdPin=25
leftPin=23
rightPin=18 
     

class Vehicle:

    # True and False are keywords and will always be equal to 1 and 0.
    testmode=False
    
    # constructor
    def __init__(self, _pinbridge):
        self.pinbridge = _pinbridge
        self.pinbridge.setGpioMode2Bcm()
        self.pinbridge.setPins2Write([fwdPin, rwdPin, leftPin, rightPin])
        #set Pin into PWM Mode 
        self.fwd = GPIO.PWM(fwdPin, 100)
        self.rwd = GPIO.PWM(rwdPin, 100)
        #start pwm pins 
        self.fwd.start(0)
        self.rwd.start(0)
        #set Pins to 0% duty        
        self.fwd.ChangeDutyCycle(0)
        self.rwd.ChangeDutyCycle(0)
        
        
        
        
    def sayHello(self):
        return "vehicle says: hello"
    
    def steer(self, _directionAsInt):
    #0 = stop
    #1 = left
    #2 = right
        if _directionAsInt == 0:
            if self.testmode:
                print ("vehicle: steering to direction: ", _directionAsInt)
            if self.testmode:
                print ("Vehicle: deactivatePin 18")
                print ("Vehicle: activatePin 23")
            self.pinbridge.deactivatePin(leftPin)
            self.pinbridge.deactivatePin(rightPin)
            return "Vehilce: steering direction: straight"
        if _directionAsInt == 1:
            if self.testmode:
                print ("vehicle: steering to direction: ", _directionAsInt)
            self.pinbridge.deactivatePin(leftPin)
            self.pinbridge.activatePin(rightPin)
            return "Vehilce: steering direction: left"
        if _directionAsInt == 2:
            if self.testmode:
                print ("vehicle: steering to direction: ", _directionAsInt)
            self.pinbridge.deactivatePin(rightPin)
            self.pinbridge.activatePin(leftPin)
            return "Vehilce: steering direction: right"
    def move(self, _speed):
        #_speed = 0.0 +int(_speed)
        #print ("Vehicle: function move was called, speed: ", _speed)
        if int(_speed) > 100:
            _speed = 100
        if int(_speed) < -100:
            _speed = -100
        if int(_speed) == 0:
            if self.testmode:
                print ("Vehicle: function move was called -> Stop", _speed)
            self.fwd.ChangeDutyCycle(0)
            self.rwd.ChangeDutyCycle(0)
            return "Vehilce: stop moving!"
        if int(_speed) < 0:
            if self.testmode:
                print ("Vehicle: function move was called -> RWD", _speed)
            self.fwd.ChangeDutyCycle(0)
            speedrwd = int(_speed) *(-1)
            self.rwd.ChangeDutyCycle(speedrwd)
            return "Vehilce: moving backward, speed: "+str( _speed)
        if int(_speed) > 0:
            if self.testmode:
                print ("Vehicle: function move was called -> FWD", _speed)
            self.rwd.ChangeDutyCycle(0)
            self.fwd.ChangeDutyCycle(_speed)
            return "Vehilce: moving forward, speed: "+ str(_speed)
        pass
        
    def setTestmode(self, _boolean):
        self.testmode=_boolean
        
    
    
    

        