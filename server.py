import socket
from cv2 import cv2
import pickle
import numpy as np
import struct
import time
import imutils
import random

HOST = '169.254.69.119'
PORT = 20203

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST,PORT))
s.listen(10)
print("Client bekleniyor...")

conn,addr = s.accept()
print(conn)
print(addr)
data = b""
payload_size = struct.calcsize(">L")


while True:
    xaxis = 11.571
    yaxis = 234.567
    zaxis = -345.678
    xbytes = bytearray(struct.pack("3f", xaxis,yaxis,zaxis))

    conn.send(xbytes)
    #conn.send(bytes([xaxis,yaxis,zaxis]))

    #print(conn.recv(1024))
    
    while len(data) < payload_size:
        data += conn.recv(4096)
        
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg:", msg_size)
    
    while len(data) <= msg_size:
        data += conn.recv(4096)
    
    frame_data = data[:msg_size]
    data = data[msg_size:]
    
    
    
    #print(data)
    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    frame = imutils.resize(frame,width=1600)
    cv2.imshow("KAMERA", frame)
    
    cv2.waitKey(1)
    
s.close()