
import binascii
import socket as syssock
from socket import AF_INET, SOCK_STREAM
import struct
import sys

import random

# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

sendPort = None
rcvPort = None

##8 version; /* version number */                               0x1
##8 flags; /* for connection set up, tear-down, control */      see below
#8 opt_ptr; /* option type between the header and payload */    0
#8 protocol; /* higher-level protocol */                        0
##16 header_len; /* length of the header */                     320
#16 checksum; /* checksum of the packet */                      calculate this
#32 source_port; /* source port */                              0
#32 dest_port; /* destination port */                           0
##64 sequence_no; /* sequence number */                         start random, ++
##64 ack_no; /* acknowledgement number */                       start x+1, ++
#32 window; /* receiver advertised window in bytes*/            0
##32 payload_len; /* length of the payload */                   up to 64K

#SOCK352_SYN 0x01 Connection initiation
#SOCK352_FIN 0x02 Connection end
#SOCK352_ACK 0x04 Acknowledgement #
#SOCK352_RESET 0x08 Reset the connection
#SOCK352_HAS_OPT 0xA0 Option field is valid

def init(UDPportTx,UDPportRx):   # initialize your UDP socket here
    if(UDPportTx is None or UDPportTx == 0):
        sendPort = 27182
    else:
        sendPort = UDPportTx

    if(UDPportRx is None or UDPportRx == 0):
        rcvPort = 27182
    else:
        rcvPort = UDPportRx

    pass
    
class socket:

    def __init__(self):  # fill in your code here
        self.sPort = sendPort,
        self.rPort = rcvPort,
        self.addr = None,
        self.seq = 0,
        self.ack = 0,
        self.socket = syssock.socket(AF_INET, SOCK_STREAM, 0)
        return

    def bind(self,address):
        return

    def connect(self,address):  # fill in your code here
        self.addr = address
        self.seq = random.randint(0, 1000)
        self.socket.connect(address)
        self.socket.settimeout(0.2)
        sock352PktHdrData = '!BBBBHHLLQQLL'
        udpPkt_hdr_data = struct.Struct(sock352PktHdrData)
        header = udpPkt_header_data.pack(1, 1, 0, 0, 320, 0, 0, 0, self.seq, self.ack, 0, 0)
        #first part
        self.socket.send(header)
        self.seq+=1
        waiting = True
        while(waiting):
            try:
                #second part
                ret = self.socket.recv(320)
                retStruct = struct.unpack('!BBBBHHLLQQLL', ret)
                synCheck = retStruct[1]
                incSeqNum = retStruct[8]
                incAckNum = retStruct[9]
                #invalid
                if(synCheck != 1 or incAckNum != self.seq or (incSeqNum != self.ack and self.ack != 0)):
                    continue
                self.ack = incSeqNum+1
            except timeout:
                #first part failed
                self.socket.settimeout(0.2)
                self.socket.send(header)
                continue
            waiting = False
        #third part
        self.socket.settimeout(0.2)
        udpPkt_header_data2 = struct.Struct(sock352PktHdrData)
        header2 = udpPkt_header_data2.pack(1, 1, 0, 0, 320, 0, 0, self.seq, self.ack, 0, 0)
        self.socket.sendAll(header2)
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

        return bytessent 

    def recv(self,nbytes):
        bytesreceived = 0     # fill in your code here
        return bytesreceived 
