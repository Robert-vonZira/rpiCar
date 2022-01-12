#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created in 2016

@author: robert
"""
import sys

class ConfigHandler:
    def __init__(self):
        self.readInDic = {}
        
    
# =============================================================================
#     def wrtiteDict2Config(self, dictionary, configfile):
#         try:
#             with open (configfile, 'a') as out:
#                 for key in dictionary:
#                     line =  (key+ " = "+ dictionary[key])
#                     print (line, file = out)
#         except: 
#             print ("ERROR: configHandler could not write to config.txt")      
#             
# =============================================================================
    def readConfig2Dict(self, configFile):
        print (configFile)
        self.readInDic = {}
        #try:
        with open (configFile, "r") as file:
            for line in file:
                line = line.strip(" ")    
                if line.startswith("#") or len(line)<=1 or line.startswith("\n"):
                    pass
                else:
                    line = line.split("=")
                    self.readInDic[str(line[0]).strip(" ")] = str(line[1].rstrip("\n").strip(" "))
        return (self.readInDic)
       # except: 
       #     e = sys.exc_info()[0]
       #     print ("ERROR: configHandler could not read form file: "+ str(configFile))        
        #    print(e)
         #   print(sys.exc_info()[1])
    
    def getValue(self, key):
        return self.readInDic.get(key)

# =============================================================================
#handler = ConfigHandler()
#handler.wrtiteDict2Config()
# 

#dict = handler.readConfig2Dict("raspiHW/GPIOconfig.conf")
#dict = handler.readConfig2Dict("GPIOconfig.conf")

#print (dict)

#print(handler.getValue("leftPin"))
# 
# =============================================================================

