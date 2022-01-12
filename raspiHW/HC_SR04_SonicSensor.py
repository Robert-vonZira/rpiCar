# coding: utf8
"""
Created 2016
                  10µS TTL every 20 mS possible
                  ____
triggerInput ____|    \_________________________________________________________________________________________________
                       250µS Delay
                                      8 Cycles Sonic Burst 200µS
sonic Burst                          _   _   _   _   _   _   _   _
from module_________________________| \_| \_| \_| \_| \_| \_| \_| \_____________________________________________________________________
                                                                        Input Echo Signal
Echo Pulse                                                                __________ 
Output    _______________________________________________________________|          \______________



@author: robert-vonZira
"""

import RPi.GPIO as GPIO
#import _fake_GPIO as GPIO
import time
import asyncio
#GPIO numbering
pins = [2, 3, 4, 7, 8, 9, 10, 11, 14, 15, 17, 18, 22, 23, 24, 25, 27] 
doloop = True
n=0 

#trigger_pin = 11 #7
#echo_pin = 10 # 14
name = ""
timeout= 0.039 #0.039

class HC_SR04_SonicSensor:
    
    testmode=False
    # True and False are keywords and will always be equal to 1 and 0.
    testmode=False
        # constructor
    def __init__(self, _pinbridge, _websocket, _name, _triggerPinNbr, _echoPinNbr):
        self.pinbridge = _pinbridge
        self.websocket = _websocket
        self.pinbridge.setGpioMode2Bcm()
        self.testmode=False
        self.doloop=False
        self.name= _name
        self.echo_pin=_echoPinNbr
        self.trigger_pin=_triggerPinNbr
        self.pinbridge.setPin2Write(self.trigger_pin)
        self.pinbridge.setPin2read(self.echo_pin)
        
        
    def getMeasurement(self):
        #deactivate trigger pin        
        GPIO.output(self.trigger_pin, False)
        if self.testmode:
            print ("Waiting to settle")
        time.sleep(0.0001 )
        #activate trigger pin for a short ping
        GPIO.output(self.trigger_pin,True)
        time.sleep(0.00001) 
        # a couple of 8 pulses is triggered by the sensor. If  the signal comes back, the ECHO output of the module will be HIGH for a duration of time taken for sending and receiving ultrasonic signals.The pulse width ranges from 150μS to 25mS depending upon the distance of the obstacle from the sensor and it will be about 38ms (0.038sec)if there is no obstacle.
        ##deactivate trigger pin
        
        
        init = time.time()
        start = time.time()
        
        GPIO.output(self.trigger_pin,False)
        
        #waiting for an echo
        while GPIO.input(self.echo_pin)==0 and start-init<timeout :
         #start = time.time()
         end = 0
        
         if self.testmode:
            print("WHILE echo = 0")
            print ("Sonar: start time  ",start)
            print ("Sonar: init  time  ",init)
            print ("Sonar: delta time ",start-init)
        
         if start-init>=timeout:
            if self.testmode:
                print (self.name," ERROR - Timeout!")
            return self.name,".Err TimeOut failure while measuring distance!"
        
        if GPIO.input(self.echo_pin)==1:
            end = time.time()        
            while GPIO.input(self.echo_pin)==1 and end-init<timeout:
             end = time.time()
             if self.testmode:
                print("WHILE echo = 1")
                print ("Sonar: start time  ",start)
                print ("Sonar: init  time  ",init)
                #print ("Sonar: current time ",time.time())
                print ("Sonar: delta time ",start-init)

             if start-end>=timeout:
                if self.testmode:
                    print (self.name," ERROR - Timeout!")
                return self.name,".Err TimeOut failure while measuring distance!"
        else:
            return self.name,".Err TimeOut failure while measuring distance!"
        duration = end - start
        distance = duration * 17150
        distance = round(distance, 1)
        if self.testmode:
            print (self.name," got a Distance:",distance,"cm")
        return distance
        
    def getDistance(self):
        self.getMeasurement()
        return self.name+".distance "+str(self.getMeasurement())+" cm"
 
     
    @asyncio.coroutine
    def getDistanceStream(self):
        self.doloop = True
        while (self.doloop):
            yield from asyncio.sleep(0.2)
            yield from self.websocket.send(self.getDistance())
            
        pass
    
    def setDoStream(self, _boolean):
        self.doloop=_boolean
        pass
        
    def setTestmode(self, _boolean):
        self.testmode=_boolean
        pass
