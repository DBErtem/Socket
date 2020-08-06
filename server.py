import socket
from cv2 import cv2
import pickle
import numpy as np
import struct

HOST = '169.254.43.118' #Bağlantının kurulacağı IPV4 adresi
PORT = 20203 #Bağlantının sağlanacağı port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Bağlantının adres ailesi ve türü

#Sunucuyu çalıştırıyoruz
s.bind((HOST,PORT))
s.listen(10)
print("Client bekleniyor...")

conn,addr = s.accept() #Conn = bağlantı sağlanıp sağlanamadığı, addr = bağlananın bilgileri
print(conn)
print(addr)
data = b"" #Verileri byte cinsinden tutmak için string formatting
payload_size = struct.calcsize(">L")
print(payload_size)
print(data)
while True:
    
    print("deurovteam")
    while len(data) < payload_size: #Elimizde gelen veri yoksa
        data += conn.recv(4096)     #veriyi alıyoruz

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]            #Gelen mesaj
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    while len(data) < msg_size:                        
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    
    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes") #Byte cinsinden aldığımız verileri encode edip frame değişkenine attık
    
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR) #Frame'i decode ediyoruz
    cv2.imshow("KAMERA", frame) #Ekranda açılacak olan frame'in özellikleri
    cv2.waitKey(1)

