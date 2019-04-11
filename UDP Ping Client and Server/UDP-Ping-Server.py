'''
#-----------------------------------------------------------------------------------------
# File Name         : UDP-Ping-Server.py
# Program Assignment: 2
# Author            : Kevin Rana
# Description       : Using UDP sockets, you will write a client and server program
# that enables the client to determine the one-way trip time (OTT) and round-trip time
# (RTT) to the server. To determine the delays, the client records the time when sending
# and receiving the packet to/from the server, and the server records the time when the
# packet is received. In the ping request the client sends to the server, it should
# include the (binary-encoded) 4-byte sequence number of the message sent. In the ping
# response, the server should echo back the client’s sequence number, and also include
# the 8-byte server’s reception time . On receiving the ping response,
# the client has all the information it needs to determine the OTT and RTT for that packet.
#------------------------------------------------------------------------------------------
'''

import sys
import struct
import socket
import random
import time

servIP = 'localhost'
servPORT = 12000

print("The server is ready to receive on port: ", servPORT)
#create server socket
ssocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ssocket.bind(('',servPORT))

 #continues as long as there are requests coming in 
while True:
    #data packet received from the client
    dataRec, clientAdd = ssocket.recvfrom(1024)
    seqNum = struct.unpack('>i', dataRec)
    #generate random number
    rand = random.randint(0,10)
    #use the random number to implement random loss 
    #wait for another ping to be sent
    if(rand < 4):
        print("packet loss on ping ", seqNum[0], " at time: ", time.time())
    else:
        sent = time.time()
        dataSent = struct.pack('>id', seqNum[0], sent)
        #send the data packet back to client along with its sequence number and the time it was sent
        print("Sent back ping number ", seqNum[0], "at current time:", sent)

    
