'''
#-----------------------------------------------------------------------------------------
# File Name         : UDP-Ping-Client.py
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
#-----------------------------------------------------------------------------------------
'''
#import random
import struct
import socket
import sys
import time

# IP address and Port
servIP = 'localhost'
servPORT = 12000

#client socket
csocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#times out after 1 second has passed without anything happening
csocket.settimeout(1)

# IP address and port of server being pinged
print("Pinging:", servIP, ",", servPORT)

#values used for indicating that data has sent or been received successfully
packSent = 0
packRec = 0

#values related to the min/max/total of RTT
min_RTT = 10000
max_RTT = 0 
tot_RTT = 0
#values related to the min/max/total of RTT
min_0TT = 10000
max_0TT = 0 
tot_0TT = 0


#create the 10 consecutive ping requests
for ping in range(1,11):
    #sends the data packet
    sent = time.time();
    #increments the count of the number of data packets sent
    packSent += 1
    dataSent = struct.pack('>i' , ping)
    csocket.sendto(dataSent, (servIP, servPORT))


    #wait to get response back
    try:
        dataRec,clientAdd = csocket.recvfrom(1024)
        seqNum = struct.unpack('>id', dataRec)

        received = time.time() - 1

        #calculates RTT and OTT
        RTT = received - sent
        OTT = seqNum[1] - sent

        #determines the RTT and OTT mins and maxs 
        max_RTT = max(max_RTT,RTT)
        min_RTT = min(min_RTT,RTT)
        max_OTT = max(max_OTT,OTT)
        min_OTT = min(min_OTT,OTT)

        #calculates the total RTT and OTT for all of the data packets sent
        tot_RTT += RTT
        tot_OTT += OTT
        
        #display the output for each data packet sent with its RTT and OTT
        print("Ping message number", seqNum[0], "RTT (OTT):", RTT, "(", OTT, ")")
        #increment packets received count
        packRec += 1
    #if it times out display the packet number and indicate that it timed out
    except socket.timeout:
        print("Ping message number ", ping, " timed out at time:", time.time())
        #continues onto the next ping request



#After all of the ping requests have been ran through
#Calculate the Total number of Packets that were sent,
#packets that were Received, 
print("Total packets sent:", packSent)
print("Total packets received:", packRec)

#calcuate the minimum and maximum RTT and OTT values
print("Max RTT:", max_RTT, "sec")
print("Min RTT:", min_RTT, "sec")
print("Max 0TT:", max_0TT, "sec")
print("Min 0TT:", min_0TT, "sec")

#along with their overall average RTT and OTT
print("Average RTT:", tot_RTT/packRec)
print("Average OTT:", tot_OTT/packRec)

#close the socket

csocket.close()


            
        



















        
        
