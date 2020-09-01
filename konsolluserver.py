import socket
from cv2 import cv2
import pickle
import numpy as np
import struct
import time
import imutils
import random
import pygame

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()

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

leftxaxis = 0
leftyaxis = 0
rightxaxis = 0
rightyaxis = 0
hatx = 0
haty = 0
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                leftxaxis = event.value
            if event.axis == 1:
                leftyaxis = event.value
            if event.axis == 2:
                rightxaxis = event.value
            if event.axis == 3:
                rightyaxis = event.value
        if event.type == pygame.JOYHATMOTION:
            if event.value == (0,1):
                haty = 1
            elif event.value == (0,-1):
                haty = -1
            elif event.value == (1,0):
                hatx = 1
            elif event.value == (-1,0):
                hatx = -1
            if event.value == (0,0):
                hatx = 0
                haty = 0
            

    analogBytes = bytearray(struct.pack("6f", leftxaxis,leftyaxis,rightxaxis,rightyaxis,hatx,haty))

    conn.send(analogBytes)

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
    frame = imutils.resize(frame,width=1600, inter=cv2.INTER_LINEAR)
    #frame = cv2.flip(frame,0)
    cv2.imshow("KAMERA", frame)
    cv2.waitKey(1)
    
s.close()