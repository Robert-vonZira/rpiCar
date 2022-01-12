#!/usr/bin/env python3
"""
Created 2016



@author: robert-vonZira
"""

LISTEN_ADDRESS = ('0.0.0.0', 8080)

import websockets
from server import client_handler
import asyncio

# to prevent the Error "RuntimeError: This event loop is already running" when using IDE Spyder use those 2 lines: 
import nest_asyncio
nest_asyncio.apply()

#from raspiHW.configHandler import ConfigHandler as conf
#config = conf.readConfig2Dict(conf, "GPIOconfig.conf")

start_server = websockets.serve(client_handler, *LISTEN_ADDRESS)
print ('WebSocket Server version 5_x up and running!')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

