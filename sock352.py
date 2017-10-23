
import binascii
import socket as syssock
import struct
import sys

# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

sendPort = None
rcvPort = None

def init(UDPportTx,UDPportRx):   # initialize your UDP socket here
    if(UDPportTx == None or UDPportTx == 0):
        sendPort = 27182
    else:
        sendPort = UDPportTx

    if(UDPportRx == None or UDPportRx == 0):
        rcvPort = 27182
    else:
        rcvPort = UDPportRx

    pass
    
class socket:

    def __init__(self):  # fill in your code here
        return {
            "sPort": sendPort,
            "rPort": rcvPort,
            "addr": None
        }

    def bind(self,address):
        return

    def connect(self,address):  # fill in your code here
        self.addr = address;
        return
    
    def listen(self,backlog):
        return

    def accept(self):
        (clientsocket, address) = (1,1)  # change this to your code
        return (clientsocket,address)
    
    def close(self):   # fill in your code here
        return

    def send(self,buffer):
        bytessent = 0     # fill in your code here
        return bytesent 

    def recv(self,nbytes):
        bytesreceived = 0     # fill in your code here
        return bytesreceived 
