import socket,imutils
import cv2
import base64
import os

HOST = ''  # socket.gethostbyname(socket.gethostname())

# PC'den Raspberry'ye keyboard tuş verisini almak için gerekli socket bağlantısı.
def get_command_keyboard(frm):
    PORT = 8001
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('waiting client...')
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            try:
                while True:
                    COMMAND = conn.recv(1024).decode('utf-8')
                    frm["command"] = COMMAND
                    if COMMAND:
                        print(f"Recieved Command: {COMMAND}")            
            except:
                print('conn is closed')
                conn.close()


# Raspberry'den PC'ye yayın yapmak için gerekli socket bağlantısı.
def stream_frame(frm):
    PORT = 8000
    BUFF_SIZE = 65536

    server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)

    socket_address = (HOST,PORT)
    server_socket.bind(socket_address)
    print("waiting for client")
    while True:
        
       msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
       print('GOT connection from ',client_addr)

       while(True):
           frame = imutils.resize(frm["data"],width=640)
           encoded,buffer = cv2.imencode('.jpeg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
           message = base64.b64encode(buffer)
           server_socket.sendto(message,client_addr)
       
           key = cv2.waitKey(1) & 0xFF
           if key == ord('q'):
               os._exit(1)
               break



# PC'den Raspberry'ye sesli komut verisini almak için gerekli socket bağlantısı. get_command_keyboard() ile aynı.
def get_command(frm):
    PORT = 8001
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('waiting client...')
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            try:
                while True:
                    COMMAND = conn.recv(1024).decode('utf-8')
                    frm["command"] = COMMAND
                    if COMMAND:
                        print(f"Recieved Command: {COMMAND}")            
            except:
                print('conn is closed')
                conn.close()   
             

                

