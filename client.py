import imutils
from imutils.video import VideoStream
import argparse
import time
import cv2
import struct
import pickle
import socket

HOST = '169.254.69.15'
PORT = 20203

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))
#connection = client_socket.makefile('wb') 

ap = argparse.ArgumentParser() 
ap.add_argument("-p", "--picamera", type=int, default=-1)
args = vars(ap.parse_args())

vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(0.2)

while True:
    frame = vs.read()
    

    result, frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    data = pickle.dumps(frame, 0)
    size = len(data)
    client_socket.sendall(struct.pack(">L", size) + data)
    print(client_socket.recv(1024))
    
cv2.destroyAllWindows()
vs.stop()               
client_socket.close()

