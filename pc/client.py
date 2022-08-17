import warnings
warnings.simplefilter("ignore", DeprecationWarning)
import socket
import threading
import speechrecog
import numpy as np
import os
import cv2
import base64
import time
from keyboardlistener import KeyboardListener
import multiprocessing
import sys

# Raspberry'e verilen ip
HOST = '192.168.1.49'  # socket.gethostbyname(socket.gethostname())

# Klavye ile hareket için mode = 1
# Sesli komut ile hareket için mode = 2
# Klavye ile hareket ve Aynı anda Raspberryden PC'ye frame aktarma için mode = 3
# Sesli komut ile hareket ve Aynı anda Raspberryden PC'ye frame aktarma için mode = 4
# default mode = 1
mode = 1 # server daki mode ile aynı seçin


def keyListener(frm):
    kl = KeyboardListener("dur") # keyboard listener object kl
    kl.key_pynput(frm)

def send_command_keyboard(frm):  
    PORT = 8001
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            time.sleep(0.1)
            my_data = frm["command"]
            print("mydata ",my_data)
            x_encoded_data = my_data.encode('utf-8')
            s.sendall(x_encoded_data)

def get_frame():
    PORT = 8000
    BUFF_SIZE = 65536
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
    message = b'HELLO'
    client_socket.sendto(message,(HOST,PORT))
    cv2.namedWindow('RECEIVING VIDEO')        
    cv2.moveWindow('RECEIVING VIDEO', 10,360) 
    
    while True:
        # FRAME
        packet,_ = client_socket.recvfrom(BUFF_SIZE)
        data = base64.b64decode(packet,' /')
        npdata = np.fromstring(data,dtype=np.uint8)
        frame = cv2.imdecode(npdata,1)
        
        cv2.imshow("RECEIVING VIDEO",frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            client_socket.close()
            os._exit(1)
            break 
    client_socket.close()
    cv2.destroyAllWindows() 

def send_command_speech():
    PORT = 8001
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            time.sleep(2)
            my_data = speechrecog.speech_recog()
            x_encoded_data = my_data.encode('utf-8')
            s.sendall(x_encoded_data)


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    frm = manager.dict()
    frm["command"] = "dur"
    
    # PC'den raspberry'yi klavye ile kontrol etmek istiyorsanız mode = 1 yapın.
    if mode == 1:
        t1 = threading.Thread(target=keyListener, args=(frm,))
        t2 = threading.Thread(target=send_command_keyboard, args=(frm,))
        try:
            t1.start()
            t2.start()
        except (KeyboardInterrupt, SystemExit):
            sys.exit()

    # PC'den raspberry'yi sesli komut ile kontrol etmek istiyorsanız mode = 2 yapın.
    elif mode == 2:
        t1 = threading.Thread(target=send_command_speech, args=(frm,))
        try:
            t1.start()
        except (KeyboardInterrupt, SystemExit):
            sys.exit()
             
    # Klavye ile hareket ve Aynı anda Raspberry'den PC'ye frame aktarma için mode = 3
    elif mode == 3: 
        t1 = threading.Thread(target=keyListener, args=(frm,))
        t2 = threading.Thread(target=send_command_keyboard, args=(frm,))
        t3 = threading.Thread(target=get_frame, args=())
        try:
            t1.start()
            t2.start()
            t3.start()
        except (KeyboardInterrupt, SystemExit):
            sys.exit()
             
    # Sesli komut ile hareket ve Aynı anda Raspberry'den PC'ye frame aktarma için mode = 4
    elif mode == 4:
        t1 = threading.Thread(target=send_command_speech, args=(frm,))
        t2 = threading.Thread(target=get_frame, args=())
        try:
            t1.start()
            t2.start()
        except (KeyboardInterrupt, SystemExit):
            sys.exit()

    
    
    
    








    
    
    
    