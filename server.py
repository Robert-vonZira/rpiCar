import asyncio
#from messageHandler import *
from messageHandler import messageHandler 
import websockets

# from raspi import *
# based on: 
# https://stackoverflow.com/questions/32054066/python-how-to-run-multiple-coroutines-concurrently-using-asyncio
# https://stackoverflow.com/questions/42830828/how-can-i-send-a-message-down-a-websocket-running-in-a-thread-from-tkinter

# The set of clients connected to this server. It is used to distribute
# messages.
clients = {} #: {websocket: name}
# vehicle = raspi() 
#pins = [2, 3, 4, 7, 8, 9, 10, 11, 14, 15, 17, 18, 22, 23, 24, 25, 27] 
#handler = messageHandler()
   
@asyncio.coroutine
def client_handler(websocket, path):
    
#    print(' ({} existing clients)'.format(len(clients)))

    # The first line from the client is the name
    name = yield from websocket.recv()
    handler = messageHandler(websocket)


    print('New client:', name)
    yield from websocket.send('Welcome to websocket-server, {}'.format(name))
    yield from websocket.send('There are {} other users connected: {}'.format(len(clients), list(clients.values())))
    clients[websocket] = name
    print(' ({} clients connected)'.format(len(clients)))
    for client, _ in clients.items():
        yield from client.send(name + ' has joined the server')


    # Handle messages from client
    try: 
        while True:
            message = yield from websocket.recv()
    #        if message is None:
    #            their_name = clients[websocket]
    #            del clients[websocket]
    #            print('Client closed connection', websocket)
    #            for client, _ in clients.items():
    #                yield from client.send(their_name + ' has left the server')
    #            break
    
           
            print('<',message)
            #answer = handler.getmessage(message, websocket)
            answer = handler.getmessage(message)
            #because every identifyer performs his own return action, no direct return possible..
            #yield from websocket.send(answer)
            print ('>',answer)   
    except websockets.exceptions.ConnectionClosed as c:
        print("One client has lost the connection - ", c)
        del clients[websocket]
    finally: 
        pass
    

         # Send message to all clients
        #for client, _ in clients.items():
        #    yield from client.send('{}: {}'.format(name, message))
