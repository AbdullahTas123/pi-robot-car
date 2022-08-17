import RPi.GPIO as GPIO
import serial
import time
import csv

#import cv2
#cap = cv2.VideoCapture(-1)
#cap.set(3, 640)
#cap.set(4, 480)

ser = serial.Serial("/dev/serial0", 115200,timeout=0) # mini UART serial device

#Set function to calculate percent from angle
def angle_to_percent (angle) :
    if angle > 180 or angle < 0 :
        return False
    start = 4
    end = 12.5
    ratio = (end - start)/180 #Calcul ratio from angle to percent

    angle_as_percent = angle * ratio

    return start + angle_as_percent

GPIO.setwarnings(False) #Disable warnings

servoPIN = 2
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)


if ser.isOpen() == False:
    ser.open() # open serial port if not open

save_count = 0

def main(x: int, y: int):
    i = 0
    global save_count
    global ser
    p = GPIO.PWM(servoPIN, 50) # GPIO 2 for PWM with 50Hz
    p.start(angle_to_percent(i)) # Initialization
    #time.sleep(0.3)
    try:
        with open("csv/lidar"+str(save_count)+".csv", "w") as f:
            # create the csv writer
            writer = csv.writer(f)
            writer.writerow([x, y])
     
            while True:
                if i >= 181:
                    #p.ChangeDutyCycle(angle_to_percent(0))
                    #time.sleep(1)
                    break
                
                p.ChangeDutyCycle(angle_to_percent(i))
                time.sleep(0.01)
                while True:
                    try:
                        counter = ser.in_waiting # count the number of bytes of the serial port
                        if counter > 8:
                            bytes_serial = ser.read(9) # read 9 bytes
                            ser.reset_input_buffer() # reset buffer
                            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: # check first two bytes
                                distance = bytes_serial[2] + bytes_serial[3]*256 # distance in next two bytes
                                distance= round(distance/100.0, 2)
                                #print('While {} , Distance: {0:2.2f} m'.format(j, distance)) # print sample data
                                writer.writerow([i, distance])
                                #print('Distance: {0:2.2f} m'.format(distance))      
                                print("Distance: {} m ".format(distance))
                                print("--------------------------------------")
                                break
                        else:
                            print("counter Error")
                            ser = serial.Serial("/dev/serial0", 115200,timeout=0) # mini UART serial device
                            if ser.isOpen() == False:
                                ser.open() # open serial port if not open
                    except OSError:
                        print("OS Error")
                        ser = serial.Serial("/dev/serial0", 115200,timeout=0) # mini UART serial device
                        if ser.isOpen() == False:
                            ser.open() # open serial port if not open
                    except IndexError:
                        print("Index Error")
                        ser = serial.Serial("/dev/serial0", 115200,timeout=0) # mini UART serial device
                        if ser.isOpen() == False:
                            ser.open() # open serial port if not open
                

                i = i + 1
                   
    
    
    except KeyboardInterrupt:
        #p.stop()
        #df.to_csv("distances.csv", index=False)
        #ser.close() # close serial port
        pass


#def camera_save(save_count):
    #ret, frame = cap.read()
    #cv2.imwrite("images/frame"+str(save_count)+".jpg", frame)
    

while True:
    try:
        ex = str(input("Exit?: "))
        if ex == "exit":
            break
        x = int(input("Enter X: "))
        y = int(input("Enter Y: "))
        #camera_save(save_count)
        main(x, y)
        save_count += 1
    except KeyboardInterrupt:
        ser.close()
        #Close GPIO & cleanup
        GPIO.cleanup()
