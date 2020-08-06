from imutils.video import VideoStream
import argparse
import time
import cv2
import struct
import pickle
import socket

HOST = '169.254.69.15' #Bağlantının kurulacağı IPV4 adresi
PORT = 20203 #Bağlantının sağlanacağı port

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Bağlantının adres ailesi ve türü
client_socket.connect((HOST,PORT)) #Uzaktaki sunucuya bağlanıp SSL ile şifreleyen komut
connection = client_socket.makefile('wb') 

ap = argparse.ArgumentParser() 
ap.add_argument("-p", "--picamera", type=int, default=-1, help="Picamera modülünü terminal koduna dönüştürdük")
args = vars(ap.parse_args())

vs = VideoStream(usePiCamera=args["picamera"] > 0).start() #Kamera kaydını başlatıyoruz
time.sleep(0.2)

while True:
    frame = vs.read() #Kameradan gelen verileri frame değişkenine atıyoruz
    frame = imutils.resize(frame, width=800) #Görüntünün genişliğini 800px yapıyoruz

    result, frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])  #Her bir frame'in kalitesini %90 olacak şekilde ayarladık.
    data = pickle.dumps(frame, 0)
    size = len(data)
    client_socket.sendall(struct.pack(">L", size) + data) #Frame verilerini sunucuya yolluyoruz
    
cv2.destroyAllWindows() #İşimiz bittikten sonra pencereleri kapatıyoruz
vs.stop()               #Kamerayı durduruyoruz

