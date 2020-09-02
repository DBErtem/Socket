import imutils
from imutils.video import VideoStream
import argparse
import time
import cv2
import struct
import pickle
import socket
import time
import adafruit_pca9685
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) #anahtarlama
S_GPIO=17
GPIO.setup(S_GPIO, GPIO.OUT)

HOST = '169.254.69.119'
PORT = 20203

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))
#connection = client_socket.makefile('wb')
print("Baglanti saglandi\n",HOST,":",PORT)
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1)
args = vars(ap.parse_args())

vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(0.2)
pwm =adafruit_pca9685.PCA9685()
yanal=0
dikey=0
donme=0
Guc=0
j=0
i=0
gripper_kapali=0
gripper_eksen_sayac=0
kamera_servo_sayac=0

pwm.set_pwm_freq(50)
for i in range(8):
    pwm.set_pwm(i,0,409)

while True:
    frame = vs.read()
    #####frame = imutils.resize(frame, width=600)
    result, frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    data = pickle.dumps(frame, 0)
    size = len(data)
    #print(size)
    
    client_socket.sendall(struct.pack(">L", size) + data)
    axis = struct.unpack("12f", client_socket.recv(1024))
    leftxaxis = round(axis[0],3)+0.039
    leftyaxis = round(axis[1],3)+0.039
    rightyaxis = round(axis[2],3)+0.039
    rightxaxis = round(axis[3],3)+0.039
    hatx = axis[4]
    haty = axis[5]
    yuvarlak=axis[6]
    ucgen = axis[7]
    L1=axis[8]
    R1=axis[9]
    L2=axis[10]
    R2=axis[11]
    print(leftxaxis,"___",-leftyaxis,"___",-rightyaxis,"___",rightxaxis,hatx,haty,yuvarlak,ucgen,L1,R1,L2,R2)
    #client_socket.sendall(b'heyyyoo')
    yanal=75*leftxaxis
    dikey=75*rightyaxis
    donme=75*leftyaxis
    kayma=75*haty
    
    if ucgen==1 && Guc==0:
        GPIO.output(S_GPIO,GPIO.HIGH)
        Guc=1
    if ucgen==-1 && Guc==1:
        pwm.set_pwm(0,0,311)
        pwm.set_pwm(1,0,311)
        pwm.set_pwm(2,0,311)
        pwm.set_pwm(3,0,311)
        pwm.set_pwm(4,0,311)
        pwm.set_pwm(5,0,311)
        pwm.set_pwm(6,0,310)
        pwm.set_pwm(7,0,311)
        GPIO.output(S_GPIO,GPIO.LOW)
        Guc=0
        
    if Guc==1:
        #--------------------------------------------motor yön-------------------------------
        pwm.set_pwm(0,0,311+dikey)
        pwm.set_pwm(1,0,311+dikey)
        pwm.set_pwm(2,0,311+dikey)
        pwm.set_pwm(3,0,311+dikey)
        pwm.set_pwm(4,0,311+yanal+donme+kayma)
        pwm.set_pwm(5,0,311+yanal-kayma)
        pwm.set_pwm(6,0,310+yanal-kayma)
        pwm.set_pwm(7,0,311+yanal-donme+kayma)
        #-------------------------------------------Motor Kodu Biter---------------------------------------------------
        
        '''#----------------------------------------gripper yönlendirme ve aç kapa----------------------------------------
        if yuvarlak==1:    
            if gripper_kapali==0:
                pwm.set_pwm(9,0,500)
                gripper_kapali==1:
            if gripper_kapali==1:
                pwm.set_pwm(9,0,150)
                gripper_kapali==0:
        if R_1==1 && gripper_eksen_sayac<90:
            gripper_eksen_sayac=gripper_eksen_sayac+2
        if L_1==1 && 0<gripper_eksen_sayac:
            gripper_eksen_sayac=gripper_eksen_sayac-2
        pwm.set_pwm(9,0,350+gripper_eksen_sayac)
        #-----------------------------------------------Gripper kodu biter--------------------------------------------------'''
            
        #--------------------------------------------------Kamera Servo-----------------------------------------------------
        if hatx==1 && kamera_servo_sayac<50:
            kamera_servo_sayac=kamera_servo_sayac+1
        if hatx==-1 && 0<kamera_servo_sayac:
            kamera_servo_sayac=kamera_servo_sayac-1
        pwm.set_pwm(9,0,150+kamera_servo_sayac)
        #----------------------------------------------------Kamera servo bitti---------------------------------------------
               
cv2.destroyAllWindows()
vs.stop()               
client_socket.close()
