#https://www.journaldev.com/14628/python-class-definition-variables-constructor-method-object  hier nicht verwendet aber schönes bespiel

# coding: utf8

import RPi.GPIO as GPIO
#import _fake_GPIO as GPIO
import time
import random
#GPIO numbering
pinsOnPinBridge = [2, 3, 4, 7, 8, 9, 10, 11, 14, 15, 17, 18, 22, 23, 24, 25, 27] 
doloop = True
n=0 

# trigger_pin = 24
# echo_pin = 25

import asyncio



class SimulateSensor:
    # constructor: 
    def __init__(self, _pinbridge, _websocket):
        self.pinbridge = _pinbridge
        self.websocket = _websocket
        
        
        pass
        
    @asyncio.coroutine
    def getLoopMeasure(self):
        print ("SimulateSensor: getLoopMeasure activated")
        global n
        global doloop
        doloop = True
        while (doloop):
            yield from asyncio.sleep(1)
            yield from self.websocket.send("simulated measurement: " + str(n))
            print ("simulateSensor counting: ",n)
            time.sleep(0.05) #time in seconds
            n = n+1
        
    def getMeasure(self):
        measure = random.random()        # Random float x, 0.0 <= x < 1.0 
        return measure
        
    def getMeasureTest(self):
        measure = random.random()        # Random float x, 0.0 <= x < 1.0 
        return measure
    def setDoLoop (self, _boolean):
        global doloop
        doloop = _boolean
        global n
        n = 0 
        
    def activatePin(self, _pinNbr):
        self.pinbridge.setGpioMode2Bcm()
        self.pinbridge.setAllPins2Write()
        self.pinbridge.activatePin(_pinNbr)
        
    def deactivatePin(self, _pinNbr):
        self.pinbridge.deactivatePin(_pinNbr)
        
    def doBlink(self, _pinArray, _ontime, _offtime, _loops):
        print ("class SimulateSensor: method doBlink was called.")
        self.pinbridge.setGpioMode2Bcm()
        # print ("handler: trying to set all Pins into write mode....")
        self.pinbridge.setAllPins2Write()
        maxLoops = _loops
        while _loops>0:
            print ("class SimulateSensor: loopnbr: ", maxLoops-_loops+1,"/",_loops)
            for pin in _pinArray:
                print("class SimulateSensor: PinNbr: ", pin)
                GPIO.output(pin, GPIO.HIGH)
                time.sleep(_ontime)
                GPIO.output(pin, GPIO.LOW)
                time.sleep(_offtime)
            _loops=_loops-1
        # # print ("handler: trying to set PIN 15 into write mode....")
        # self.pinbridge.setPins2Write([11, 15, 17])
        # # print ("handler: trying to activate Pin 15....")
        # self.pinbridge.activatePin(23)
        # # print ("handler: trying to sleep for 2 seconds....")
        # time.sleep(2)
        # # print ("handler: trying to deactivate pin 15....")
        # self.pinbridge.deactivatePin(15)
        pass
        
    def sayHello(self):
        return "class SimulateSensor: Hello!"