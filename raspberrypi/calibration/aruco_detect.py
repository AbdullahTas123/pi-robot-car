import numpy as np
import cv2
import cv2.aruco as aruco

marker_size = 100

with open('camera_cal.npy','rb') as f:
    camera_matrix = np.load(f)
    camera_distortion = np.load(f)
    
print(camera_matrix)
print(camera_distortion)
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)

cap = cv2.VideoCapture(0)

camera_width = 640
camera_height = 480
camera_frame_rate = 40

cap.set(2, camera_width)
cap.set(4, camera_height)
cap.set(5, camera_frame_rate)

while True:
    ret, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    corners, ids, rejected = aruco.detectMarkers(gray_frame,aruco_dict,camera_matrix,camera_distortion)
    
    if ids is not None:
        
        aruco.drawDetectedMarkers(frame, corners)
        
        rvec_list_all, tvec_list_all, _objPoints = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix,camera_distortion)
        
        rvec = rvec_list_all[0][0]
        tvec = tvec_list_all[0][0]
        
        aruco.drawAxis(frame,camera_matrix,camera_distortion,rvec,tvec,100)
        
        tvec_str = "x=%4.0f y=%4.0f z=%4.0f"%(tvec[0],tvec[1], tvec[2])
        cv2.putText(frame, tvec_str,(20,460),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2,cv2.LINE_AA)
    
    cv2.imshow('frame',frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"): break
        

cap.release()
cv2.destroyAllWindows()