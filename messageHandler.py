from raspiHW.Pinbridge import Pinbridge
from raspiHW.HC_SR04_SonicSensor import HC_SR04_SonicSensor
from raspiHW.SimulateSensor import SimulateSensor
from raspiHW.Vehicle import Vehicle
from threading import Thread
import time
import asyncio

class messageHandler():

# True and False are keywords and will always be equal to 1 and 0.
 testmode=0
 answer="messagehandler: has nothing done!"

 def __init__ (self, _websocket): #"constructor" -> initiator 
  #variablen mit self.xyz hier initialisieren
   self.bridge = Pinbridge()
   self.sonarF = HC_SR04_SonicSensor(self.bridge, _websocket, "HC_SR04_SonicSensorF", 20, 21)#11, 10)#bridge, websocket,    trigger, echo
   self.sonarL = HC_SR04_SonicSensor(self.bridge, _websocket, "HC_SR04_SonicSensorL", 7, 8)#14
   self.sonarR = HC_SR04_SonicSensor(self.bridge, _websocket, "HC_SR04_SonicSensorR", 17, 22)
   self.SimulateSensor = SimulateSensor(self.bridge, _websocket)
   self.v = Vehicle(self.bridge)
   self.websocket = _websocket
   
   #pass
   
 
 def getmessage(self, _message):
    self.answer="messagehandler: has done nothing!"
    # print("class messsageHandler: message received: ", _message)
    #bridge.sayHello()
    
    identifyer=_message[0:_message.find(".")]
    if self.testmode:
        print("calss MessageHandler identifyer = "+identifyer)
    if ' ' not in _message:
        command = _message[_message.find(".")+1:len(_message)]
    else:
        command = _message[_message.find(".")+1:_message.find(" ")]
    values = self.splitCommand(_message[_message.find(" ")+1:len(_message)])
    if self.testmode:
            print ("class message handler identifyer: ",identifyer)
    if self.testmode:
            print ("class message handler command: ",command)
    if self.testmode:
            print ("class message handler values: ",values)
#help
    if identifyer == "help" or _message == "help":
        answer = self.usage()
        asyncio.ensure_future(self.sendmessage(answer, self.websocket))
        return self.usage()
        
            
#simulation    
    if identifyer == "sim":
        if self.testmode:
            print ("class messageHanlder: SimulateSensor Stuff")
        if command == "getLoop":
             asyncio.ensure_future(self.SimulateSensor.getLoopMeasure())
             return "MessageHandler: simulated getLoop started"
        elif command == "stop":
            self.SimulateSensor.setDoLoop(False)
            asyncio.ensure_future(self.sendmessage("simulate looping stoped!", self.websocket))
            return "MessageHandler: simulated getLoop stopped"
        else:
            return "MessageHandler: unknown command for: "+ identifyer
            
#test             
    elif identifyer == "test":
        if self.testmode:
            print ("class messageHandler: Test Stuff...")
        if command == "mode":
            if self.testmode:
                print ("class messageHandler: Changing Testmode...")
                print (values[0])
            if values[0] == 'on':
                self.testmode=True
                self.v.setTestmode(True)
                self.sonarF.setTestmode(True)
                self.sonarL.setTestmode(True)
                return "MessageHandler: Testmode ON"
            if values[0] == 'off':
                self.testmode=False
                self.v.setTestmode(False)
                self.sonarF.setTestmode(False)
                self.sonarL.setTestmode(False)
                return "MessageHandler: Testmode OFF"
        if command == "activatePin":
            self.bridge.setPin2Write(int(values[0]))
            #print ("MessageHanlder: set PinNbr: "+values[0]+" to writeMode")
            self.bridge.activatePin(int(values[0]))
            return "MessageHanlder: activated PinNbr: "+values[0]
        if command == "deactivatePin":
            self.bridge.setPin2Write(int(values[0]))
            self.bridge.deactivatePin(int(values[0]))
            return "MessageHanlder: deactivated PinNbr: "+values[0]
            
            
        elif command == "ping":
            pong = "pong!"
            asyncio.ensure_future(self.sendmessage(pong, self.websocket))
            return pong
        else:
            return "MessageHandler: unknown command for: "+identifyer
    
#vehicle    
    elif identifyer == "vehicle": 
        if self.testmode:
            print ("class messageHandler: vehicle Stuff...")
        if command == "steer":
            if self.testmode:
                print ("class messageHandler: vehicle steer direction: ", values[0])
            return self.v.steer(int(values[0])) 
        elif command == "move":
            if self.testmode:
                print ("class messageHandler: vehicle move direction: ", values[0])
            return self.v.move(int(values[0]))
        else:
            return "MessageHandler: unknown command for: "+identifyer
            
#sonar
    elif identifyer == "sonar":
        if self.testmode:
            print ("class messageHandler: sonar Stuff...")
        if command == "getDistanceF":
            distance = self.sonarF.getDistance()
            if self.testmode:
                print ("messageHandler: got a distance from sonarF: "+ distance)
            asyncio.ensure_future(self.sendmessage(distance, self.websocket))
            return "MessageHandler from Sonar: " +distance
        if command == "getDistanceL":
            distance = self.sonarL.getDistance()
            if self.testmode:
                print ("messageHandler: got a distance from sonarL: "+ distance)
            asyncio.ensure_future(self.sendmessage(distance, self.websocket))
            return "MessageHandler from SonarL: " +distance
        if command == "getDistanceR":
            distance = self.sonarR.getDistance()
            if self.testmode:
                print ("messageHandler: got a distance from sonarR: "+ distance)
            asyncio.ensure_future(self.sendmessage(distance, self.websocket))
            return "MessageHandler from SonarR: " +distance
        elif command == "getDistanceStreamF":
            asyncio.ensure_future(self.sonarF.getDistanceStream())
            return "MessageHandler: Sonar: DistanceStream started"
        elif command == "getDistanceStreamL":
            asyncio.ensure_future(self.sonarL.getDistanceStream())
            return "MessageHandler: SonarL: DistanceStream started"
        elif command == "getDistanceStreamR":
            asyncio.ensure_future(self.sonarR.getDistanceStream())
            return "MessageHandler: SonarR: DistanceStream started"
        elif command == "stop":
            self.sonarF.setDoStream(False)
            self.sonarL.setDoStream(False)
            self.sonarR.setDoStream(False)
            return "MessageHandler: Sonar: DistanceStream stopped"
        else:
            return "MessageHandler: unknown command for: "+identifyer
#answer if no action was performed   
#    asyncio.ensure_future(self.sendmessage("messagehandler: has nothing done!", self.websocket))
    return self.answer
 
 @asyncio.coroutine
 def sendmessage(self, _message, _websocket):
    if self.testmode:
        print ("handler: method sendmessage was called")
    yield from _websocket.send(_message)
   
 def splitCommand(self, _message):
    return _message.split()
    
 def usage(self):
    usage ="list of known commands. \n pattern: identifyer.command [values] \n test.mode [on,off]\n vehicle.steer [0(ahead), 1(right), 2(left)] \n vehicle.move [-100(rwd)-100(fwd)] \n sonar.getDistance [] \n sonar.getDistanceStream [] \n sonar.stop [] \n sim."
    return usage
