"""
Created 2016



@author: robert-vonZira
"""
from raspiHW.Pinbridge import Pinbridge
from raspiHW.HC_SR04_SonicSensor import HC_SR04_SonicSensor
from raspiHW.SimulateSensor import SimulateSensor
from raspiHW.Vehicle import Vehicle
import asyncio

class messageHandler():
 
# True and False are keywords and will always be equal to 1 and 0.
 testmode=0
 #answer="messagehandler: has nothing done!"

 def __init__ (self, _websocket): #"constructor" -> initiator 
  #variablen mit self.xyz hier initialisieren
   self.bridge = Pinbridge()
   self.sonarF = HC_SR04_SonicSensor(self.bridge, _websocket, "HC_SR04_SonicSensorF", 20, 21)#bridge, websocket,    trigger, echo
   self.sonarL = HC_SR04_SonicSensor(self.bridge, _websocket, "HC_SR04_SonicSensorL", 16, 12)
   self.sonarR = HC_SR04_SonicSensor(self.bridge, _websocket, "HC_SR04_SonicSensorR", 19, 13)
   self.SimulateSensor = SimulateSensor(self.bridge, _websocket)
   self.v = Vehicle(self.bridge)
   self.websocket = _websocket
   
   #pass
   
 
 def getmessage(self, _message):
    answer="messagehandler: has done nothing!"
    # print("class messsageHandler: message received: ", _message)
    #bridge.sayHello()
    try:
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
    except:
        answer = "messageHanlder on rpi: ERROR - unkonwn / not suitable command was sent."
        asyncio.ensure_future(self.sendmessage(answer, self.websocket))
        

        

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
            answer="MessageHandler: unknown command for: "+identifyer
            asyncio.ensure_future(self.sendmessage(answer, self.websocket))
            return answer
            
            
#test             
    elif identifyer == "test":
        if self.testmode:
            print ("class messageHandler: Test Stuff...")
        if command == "mode":
            if self.testmode:
                print ("class messageHandler: Changing to Testmode...")
                print (values[0])
            if values[0] == 'on':
                self.testmode=True
                self.v.setTestmode(True)
                self.sonarF.setTestmode(True)
                self.sonarL.setTestmode(True)
                answer = "MessageHandler: Testmode ON"
                asyncio.ensure_future(self.sendmessage(answer, self.websocket))
                return answer
            if values[0] == 'off':
                self.testmode=False
                self.v.setTestmode(False)
                self.sonarF.setTestmode(False)
                self.sonarL.setTestmode(False)
                answer = "MessageHandler: Testmode OFF"
                asyncio.ensure_future(self.sendmessage(answer, self.websocket))
                return answer
        if command == "activatePin":
            self.bridge.setPin2Write(int(values[0]))
            #print ("MessageHanlder: set PinNbr: "+values[0]+" to writeMode")
            self.bridge.activatePin(int(values[0]))
            answer = "MessageHanlder: activated PinNbr: "+values[0]
            asyncio.ensure_future(self.sendmessage(answer, self.websocket))
            return answer
        if command == "deactivatePin":
            self.bridge.setPin2Write(int(values[0]))
            self.bridge.deactivatePin(int(values[0]))
            answer = "MessageHanlder: deactivated PinNbr: "+values[0]
            asyncio.ensure_future(self.sendmessage(answer, self.websocket))
            return answer           
            
        elif command == "ping":
            pong = "pong!"
            asyncio.ensure_future(self.sendmessage(pong, self.websocket))
            return pong
        else:
            answer="MessageHandler: unknown command for: "+identifyer
            asyncio.ensure_future(self.sendmessage(answer, self.websocket))
            return answer

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
            answer="MessageHandler: unknown command for: "+identifyer
            asyncio.ensure_future(self.sendmessage(answer, self.websocket))
            return answer
            
            
#sonar
    elif identifyer == "sonar":
        if self.testmode:
            if command == "stop":
                answer = ("TESTMODE all Sonars have stopped")
                asyncio.ensure_future(self.sendmessage(answer, self.websocket))
                return "class messageHandler: all Sonars have stopped"
            else: 
                answer = ("TESTMODE sonar "+values[0] + " does some Measurements...")
                asyncio.ensure_future(self.sendmessage(answer, self.websocket))
                return "class messageHandler: sonar "+values[0] + " does some Measurements..."
        elif command == "getDistance":
            if values[0] == 'F':
                distance = self.sonarF.getDistance()
                if self.testmode:
                    print ("messageHandler: got a distance from sonar Front: "+ distance)
                asyncio.ensure_future(self.sendmessage(distance, self.websocket))
                return "MessageHandler from Sonar: " +distance
            elif values[0] == 'L':
                distance = self.sonarL.getDistance()
                if self.testmode:
                    print ("messageHandler: got a distance from sonar Left: "+ distance)
                asyncio.ensure_future(self.sendmessage(distance, self.websocket))
                return "MessageHandler from Sonar: " +distance
            elif values[0] == 'R':
                distance = self.sonarR.getDistance()
                if self.testmode:
                    print ("messageHandler: got a distance from sonar Right: "+ distance)
                asyncio.ensure_future(self.sendmessage(distance, self.websocket))
                return "MessageHandler from Sonar: " +distance
            else:
                answer="MessageHandler: unknown value for: "+identifyer+"."+command
                asyncio.ensure_future(self.sendmessage(answer, self.websocket))
                return answer
        
        elif command == "getDistanceStream":
            if values[0] == 'F':
                asyncio.ensure_future(self.sonarF.getDistanceStream())
                return "MessageHandler: Sonar: DistanceStream Front started"
            elif values[0] == 'L':
                asyncio.ensure_future(self.sonarL.getDistanceStream())
                return "MessageHandler: Sonar: DistanceStream Left started"
            elif values[0] == 'R':
                asyncio.ensure_future(self.sonarR.getDistanceStream())
                return "MessageHandler: Sonar: DistanceStream Right started"
            else:
                answer="MessageHandler: unknown value for: "+identifyer+"."+command
                asyncio.ensure_future(self.sendmessage(answer, self.websocket))
                return answer
        
            
        elif command == "stop":
            self.sonarF.setDoStream(False)
            self.sonarL.setDoStream(False)
            self.sonarR.setDoStream(False)
            return "MessageHandler: Sonar: all DistanceStreams stopped"
        else:
            answer="MessageHandler: unknown command for: "+identifyer
            asyncio.ensure_future(self.sendmessage(answer, self.websocket))
            return answer
    #response if no suitable command was found: 
    asyncio.ensure_future(self.sendmessage(answer, self.websocket))
    return answer
 
 
 @asyncio.coroutine
 def sendmessage(self, _message, _websocket):
    if self.testmode:
        print ("handler: method sendmessage() was called")
    yield from _websocket.send(_message)
   
 def splitCommand(self, _message):
    return _message.split()
    
 def usage(self):
     usage ="list of known commands: \n pattern: identifyer.command [values] \n test.mode [on,off]\n test.activatePin [int] \n test.deactivatePin [int]\n test.ping [] \n vehicle.steer [0(ahead), 1(right), 2(left)] \n vehicle.move [-100(rwd)-100(fwd)] \n sonar.getDistance [F, L, R] \n sonar.getDistanceStream [F, L, R] \n sonar.stop [] \n sim.getLoop [] \n sim.stop [] \n "
     return usage
