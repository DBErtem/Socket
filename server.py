import socket
from cv2 import cv2
import pickle
import numpy as np
import struct

HOST = '169.254.43.118'
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
    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg: ", msg_size)

    while len(data) < msg_size:
        data += conn.recv(4096)
    print(data[-4:])
    frame_data = data[:msg_size]
    data = data[msg_size:-4]

    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow("KAMERA", frame)
    cv2.waitKey(1)