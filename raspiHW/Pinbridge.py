#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 22:51:53 2022

on laptop gpio simulator is used: https://github.com/nosix/raspberry-gpio-emulator

@author: robert
"""



# coding: utf8
class Singleton(type):
    """
    Define an Instance operation that lets clients access its unique
    instance.
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance



import RPi.GPIO as GPIO
#import _fake_GPIO as GPIO
import time
#GPIO numbering
pins = [2, 3, 4, 7, 8, 9, 10, 11, 14, 15, 17, 18, 22, 23, 24, 25, 27]
pinsRpi2 = [0, 1, 4, 7, 8, 9, 10, 11, 14, 15, 17, 18, 21, 22, 23, 24, 25]
pinsRPi3 = [2, 3, 4, 7, 8, 9, 10, 11, 14, 15, 17, 18, 22, 23, 24, 25, 27]
writingPins = list()
readinigPins = list()

maxSpeed = 100


class Pinbridge(metaclass=Singleton):

   # """ Create singleton instance """    
   # Check whether we already have an instance
   # pass

 def printListOfUsedPins(self):
    #forEach writngpins
    #forEach readingpins
    #pins including possible useage (pwm iCb...)
    rpi2 = "GPIO_02=SDA GPIO_03=SCL GPIO_04=FPCLKO GPIO_07=CE1 GPIO_08=CE0 GPIO_09=MSIO GPIO_10=MSOI GPIO_11=SCLK GPIO_14=TXD GPIO_15=RXD GPIO_17=-- GPIO_18=PWM_CLK GPIO_22=-- GPIO_23=-- GPIO_24=-- GPIO_25=-- GPIO_27="
    rpi3 = ""
    pass
     
 def setGpioMode2Bcm(self):
    #use GPIO numbering
    GPIO.setmode(GPIO.BCM)
    
 def cleanUpPins(self):
  # print ("class pinbridge: try to clear memory...")
  GPIO.cleanup()
  # print ("class pinbridge: memory is cleared!")
 
 def setAllPins2Write(self):
    # print ("class pinbridge: try to set all pins to write...")
    # print(" ****TEST**** list of known writing Pins: ", writingPins)
    for pinNbr in pins:
        if pinNbr in readinigPins: 
            print ("Pinbridge: Error Pin Nbr:", pinNbr , " is allready in use in READmode!")
        else:
            self.setPin2Write(pinNbr)
            #writingPins.append(pinNbr)
            #GPIO.setup(pinNbr, GPIO.OUT)
        #state = GPIO.input(pinNbr)
        # print ("State of PinNbr: ", pinNbr, " = ", state)
    # print(" ****TEST****  list of known writing Pins: ", writingPins)

 def setPins2Write(self, ArrayOfPinNbrs):
  # print ("class pinbrigde: set pins ", ArrayOfPinNbrs , " to write...")
  for pinNbr in ArrayOfPinNbrs:
   #GPIO.setup(pinNbr, GPIO.OUT)
   self.setPin2Write(pinNbr)
   # print ("Pin ", pinNbr, "is set to write")
  # print ("class pinbrigde: ", ArrayOfPinNbrs , "pins are set to write...")  
  #pass
 
 def setPin2Write(self, _pinNbr):
    if _pinNbr in readinigPins: 
        print ("Pinbridge: Error Pin is already in use in READmode!")
    else:
        writingPins.append(_pinNbr)
        GPIO.setup(_pinNbr, GPIO.OUT)
 
 def setAllPins2read(self):
    for pinNbr in pins:
        GPIO.setup(pinNbr, GPIO.IN)

 def setPins2read(self, ArrayOfPinNbrs):
  for pinNbr in ArrayOfPinNbrs:
   GPIO.setup(pinNbr, GPIO.IN)
  #pass
 
 def setPin2read(self, _pinNbr):
    if _pinNbr in writingPins: 
        print ("Pinbridge: Error Pin is already in use in WRITEmode!")
    else:
        readinigPins.append(_pinNbr)
        GPIO.setup(_pinNbr, GPIO.IN)
 
 def activatePin(self, pinNbr): 
    #print ("class pinbrigde: activate PinNbr: ", pinNbr)
    GPIO.output(pinNbr, GPIO.HIGH)
    #print ("class pinbrigde: PinNbr: ", pinNbr, " is activated!")
  #pass
 
 def deactivatePin(self, pinNbr):
    # print ("class pinbrigde: deactivate PinNbr: ", pinNbr)
    GPIO.output(pinNbr, GPIO.LOW)
    # print ("class pinbrigde: PinNbr: ", pinNbr, " is deactivated!")
 
 def deactivePins(self):
 #deactivates ALL pins = emergency shutdown
  for pinNbr in pins:
   GPIO.output(pinNbr, GPIO.LOW)
  # print ("class pinbridge: all pins are deactivated")
  
 def cleanup(self):
   GPIO.cleanup()
   
 def sayHello(self):
  print("class Pinbridge: HELLO!")
  
 def getPinNbrs(self):
    # print("class Pinbridge: getPinNbrs() was called. ")
    return pins
 
   
 
