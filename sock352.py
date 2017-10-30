
import binascii
import socket as syssock
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
import struct
import sys
import pdb


import random

# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

sendPort = 0
rcvPort = 0

##8 version; /* version number */                               0x1
##8 flags; /* for connection set up, tear-down, control */      see below
#8 opt_ptr; /* option type between the header and payload */    0
#8 protocol; /* higher-level protocol */                        0
##16 header_len; /* length of the header */                     40
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
#SOCK352_HAS_OPT 0x10 Option field is valid

# this init function is global to the class and
# defines the UDP ports all messages are sent
# and received from.
def init(UDPportTx,UDPportRx): # initialize your UDP socket here
    # create a UDP/datagram socket 
    # bind the port to the Rx (receive) port number
    global sendPort
    global rcvPort

    if(UDPportTx is None or UDPportTx == 0):
        sendPort = 27182
    else:
        sendPort = int(UDPportTx)

    if(UDPportRx is None or UDPportRx == 0):
        rcvPort = 27182
    else:
        rcvPort = int(UDPportRx)
    
class socket:

    def __init__(self):  # fill in your code here
        # create any lists/arrays/hashes you need
        self.sPort = sendPort
        self.rPort = rcvPort
        self.addr = None
        self.seq = 0
        self.ack = 0
        self.socket = syssock.socket(AF_INET, SOCK_DGRAM)

        self.packetList = []    # for part 1 we dont need a buffer to be stored,
        # so we're only using this list to store the current packet
        self.PLindex = 0
        return

    def bind(self,address):
        # null function for part 1
        return

    def connect(self,address): # fill in your code here
        #  create a new sequence number 
        #  create a new packet header with the SYN bit set in the flags (use the Struct.pack method)
        #  also set the other fields (e.g sequence #)
        #   add the packet to the send buffer
        #   set the timeout
        #      wait for the return SYN
        #        if there was a timeout, retransmit the SYN packet
        #   set the send and recv packets sequence numbers

        self.addr = (syssock.gethostbyname(syssock.getfqdn(address[0])), (int)(self.rPort))
        self.seq = random.randint(0, 1000)
        self.socket.bind(("", sendPort))
        
        #self.socket.connect((syssock.gethostbyname(syssock.getfqdn(address[0])), int(address[1])))
        #self.socket.settimeout(0.2)
        self.sock352PktHdrData = '!BBBBHHLLQQLL'
        udpPkt_hdr_data = struct.Struct(self.sock352PktHdrData)
        header = udpPkt_hdr_data.pack(1, 1, 0, 0, 40, 0, 0, 0, self.seq, self.ack, 0, 0)
        #first part
        print (self.addr)
        self.socket.sendto(header, self.addr)

        waiting = True
        while(waiting):
            try:
                #second part
                #pdb.set_trace()
                self.socket.settimeout(0.2)
                ret, ad = self.socket.recvfrom(40)
                retStruct = struct.unpack('!BBBBHHLLQQLL', ret)
                synCheck = retStruct[1]
                incSeqNum = retStruct[8]
                incAckNum = retStruct[9]
                #invalid
                if(synCheck != 5 or incAckNum != self.seq+1 or (incSeqNum != self.ack and self.ack != 0)):
                    continue
                self.ack = incSeqNum+1
            except:
                #first part failed
                print ("receive timed out")
                self.socket.sendto(header, self.addr)
                continue
            waiting = False
        #third part
        self.seq+=1
        self.socket.settimeout(0.2)
        udpPkt_header_data2 = struct.Struct(self.sock352PktHdrData)
        header2 = udpPkt_header_data2.pack(1, 5, 0, 0, 40, 0, 0, self.seq, self.ack, 0, 0)
        self.socket.sendto(header2, self.addr)
        self.seq+=1
        return
    
    def listen(self,backlog):
        return

    def accept(self):
        #pdb.set_trace()

        self.socket.bind(("", rcvPort))
        #self.socket.listen(5)
        #self.clsocket = self.socket.accept()

        #rcv syn info from client
        self.clsocket = socket()
        #set the data correctly

        # call  __sock352_get_packet() until we get a new conection
        # check the the incoming packet - did we see a new SYN packet?
        self.socket.settimeout(None)
        packetList[0], ad = self.socket.recvfrom(40)
        self.addr = (syssock.gethostbyname(syssock.getfqdn(ad[1])), (int)(self.sPort))
        print ("got the packet")
        __sock352_get_packet()
        packetList[0] = None
        self.socket.settimeout(0.2)
        return self.clsocket
    
    def close(self):   # fill in your code here
        # send a FIN packet (flags with FIN bit set)
        self.socket.settimeout(0.2)
        udpPkt_hdr_data = struct.Struct(self.sock352PktHdrData)
        header = udpPkt_header_data.pack(1, 2, 0, 0, 40, 0, 0, 0, self.seq, self.ack, 0, 0)
        self.socket.sendto(header, self.addr)

        waiting = True
        while(waiting):
            try:
                #second part
                ret, ad = self.socket.recvfrom(40)
                retStruct = struct.unpack(self.sock352PktHdrData, ret)
                ackCheck = retStruct[1]
                incSeqNum = retStruct[8]
                incAckNum = retStruct[9]
                #invalid
                if(ackCheck != 6 or incAckNum != self.seq+1 or incSeqNum != self.ack):
                    continue
                self.ack = incSeqNum+1
            except:
                #first part failed
                self.socket.settimeout(0.2)
                self.socket.sendto(header, self.addr)
                continue
            waiting = False

        self.seq+=1;

        self.socket.close()
        return

    def send(self,buffer):
        bytessent = 0     # fill in your code here
        # make sure the correct fields are set in the flags
        # make sure the sequence and acknowlegement numbers are correct
        # create a new sock352 header using the struct.pack
        # create a new UDP packet with the header and buffer 
        # send the UDP packet to the destination and transmit port
        # set the timeout
        # wait or check for the ACK or a timeout

        udpPkt_hdr_data = struct.Struct(self.sock352PktHdrData)
        header = udpPkt_header_data.pack(1, 0, 0, 0, 40, 0, 0, 0, self.seq, self.ack, 0, len(buffer))
        packet = header + buffer

        bytessent = self.socket.sendto(packet, self.addr)

        waiting = True
        self.socket.settimeout(0.2)
        while(waiting):
            try:
                #second part

                ret, ad = self.socket.recvfrom(40)
                retStruct = struct.unpack(self.sock352PktHdrData, ret)
                ackCheck = retStruct[1]
                incSeqNum = retStruct[8]
                incAckNum = retStruct[9]
                #invalid
                if(ackCheck != 4 or incAckNum != self.seq+1 or incSeqNum != self.ack):
                    continue
                self.ack = incSeqNum+1
            except:
                #first part failed
                bytessent = self.sendto(packet, self.addr)
                continue
            waiting = False
        self.seq += 1

        return bytessent

    def recv(self,nbytes):
        # fill in your code here
        packetList[0], ad = self.socket.recvfrom(nbytes+40)
        __sock352_get_packet()
        bytesreceived = packetList[0][40:]
        packetList[0] = None

        # call __sock352_get_packet() to get packets (polling)
        # check the list of received fragements
        # copy up to bytes_to_receive into a buffer
        # return the buffer if there is some data
        return bytesreceived

    # this is an internal function that demultiplexes all incomming packets
    # it update lists and data structures used by other methods
    def __sock352_get_packet(self):
        # There is a differenct action for each packet type, based on the flags:
        #  First check if it's a connection set up (SYN bit set in flags)
        #    Create a new fragment list
        #    Send a SYN packet back with the correct sequence number
        #    Wake up any readers wating for a connection via accept() or return
        #  else
        #      if it is a connection tear down (FIN) 
        #        send a FIN packet, remove fragment list
        #      else if it is a data packet
        #           check the sequence numbers, add to the list of received fragments
        #           send an ACK packet back with the correct sequence number
        #          else if it's nothing it's a malformed packet.
        #              send a reset (RST) packet with the sequence number
        header = packetList[PLindex][:40]
        msg = packetList[PLindex][40:]
        headerData = struct.unpack(self.sock352PktHdrData, header)
        if (headerData[1] == 1):            #syn
            udpPkt_hdr_data = struct.Struct(self.sock352PktHdrData)
            self.seq = self.seq = random.randint(0, 1000)
            self.ack = headerData[8]+1
            syn = udpPkt_header_data.pack(1, 5, 0, 0, 40, 0, 0, self.seq, self.ack, 0, 0)
            self.socket.sendto(syn, self.addr)
            self.socket.settimeout(0.2)

            waiting = True
            while(waiting):
                try:
                    #wait for third part
                    ret, ad = self.socket.recvfrom(40)
                    retStruct = struct.unpack(self.sock352PktHdrData, ret)
                    ackCheck = retStruct[1]
                    incSeqNum = retStruct[8]
                    incAckNum = retStruct[9]
                    #invalid
                    if(ackCheck != 5 or incAckNum != self.seq+1 or incSeqNum != self.ack):
                        continue
                    self.ack+=1;
                except:
                    #our ack failed; resend
                    self.socket.settimeout(0.2)
                    self.socket.sendto(syn, self.addr)
                    continue
                waiting = False

            self.seq+=1

        elif (headerData[1] == 2):       #fin
            udpPkt_hdr_data = struct.Struct(self.sock352PktHdrData)
            fin = udpPkt_header_data.pack(1, 6, 0, 0, 40, 0, 0, self.seq, self.ack, 0, 0)
            self.socket.sendto(fin, self.addr)

        elif (headerData[1] == 0):
            udpPkt_hdr_data = struct.Struct(sock352PktHdrData)
            ack = udpPkt_header_data.pack(1, 4, 0, 0, 40, 0, 0, self.seq, self.ack, 0, 0)
            self.socket.sendto(ack, self.addr)
            self.seq+=1
            self.ack+=1

        else:       #malformed packet
            udpPkt_hdr_data = struct.Struct(self.sock352PktHdrData)
            res = udpPkt_header_data.pack(1, 8, 0, 0, 40, 0, 0, self.seq, self.ack, 0, 0)
            self.socket.sendto(res, self.addr)

        return
