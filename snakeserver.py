#! /usr/bin/env python

import socket
import sys

HOST = ''   
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'
scores={}
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    data=conn.recv(1024)
    scores[addr[0]]=data
    print("Received Score: " + data)
    #print scores
    maximum_score = max(scores, key=scores.get)
    print(maximum_score, scores[maximum_score])
    conn.send(str(maximum_score))
    conn.send(",")
    conn.send(str(scores[maximum_score]))
    print "send"
s.close()
