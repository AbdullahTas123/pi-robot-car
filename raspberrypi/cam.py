import math
import cv2
import cv2.aruco as aruco
import numpy as np
import base64


class Aruco:
    def __init__(self, ID, dist2cam, angle) -> None:
        self.arucoID = ID
        self.angle = angle
        self.dist2cam = dist2cam
        self.left_target_angle = 0
        self.right_target_angle = 0
        self.left_distance = 0
        self.right_distance = 0

    def set_instant_phase_angle(self, phase_angle):
        self.instant_phase_angle = self.angle + phase_angle
        #   ## New angle optimization for minimum rotation
        #   # Angle changed to (0, 360) range
        #   self.instant_phase_angle = self.instant_phase_angle % 360
        #   if self.instant_phase_angle // 180 == 1:
        #       self.instant_phase_angle -= 360
        print(f'Phase: {self.instant_phase_angle} for ArUcoID: {self.arucoID}')
        #   print(f'New optimized angle: {self.instant_phase_angle} for ArUcoID: {self.arucoID}')
        print('-----------------------------------')


class Camera:
    def __init__(self, show: bool, captureIndex: int, camRes: tuple) -> None:
        self.show = show
        self.captureIndex = captureIndex
        self.resolution = camRes
        self.target = None
        self.ids = []
        self.isRead = False
        self.out = False

    def set_camera_settings(self, focal_length: float):
        self.cap = cv2.VideoCapture(self.captureIndex)
        self.cap.set(3, self.resolution[0])
        self.cap.set(4, self.resolution[1])
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.focalL = focal_length

    def set_aruco_settings(self, markerSize, totalMarkers, arucoWidth):
        self.aruco_key = aruco.Dictionary_get(
            getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}'))
        self.aruco_params = aruco.DetectorParameters_create()
        self.aruco_params.adaptiveThreshConstant = 10
        self.aruco_real_width = arucoWidth

    def calc_focal_length(self):
        pass

    def distance_to_camera(self, aruco_size_px):
        return (self.aruco_real_width * self.focalL) / aruco_size_px

    def set_frame(self):
        ret, frame = self.cap.read()
        if ret:
            self.frame = frame
            self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.isRead = True

    def detect_aruco(self):
        corners, ids, _ = aruco.detectMarkers(
            self.gray, self.aruco_key, parameters=self.aruco_params)
        if np.all(ids != None):
            self.arucoDetected = True
            #collect_data_obj = CameraData()

            aruco.drawDetectedMarkers(self.frame, corners)
            c = max(corners, key=cv2.contourArea)
            for i in range(len(ids)):
                if c.all() == corners[i].all():
                    self.id = ids.flatten()[i]
                    break
            #collect_data_obj.arucoID = self.id

            marker = cv2.minAreaRect(c)
            dim = sum(marker[1])/2.0

            self.dist2cam_real_cm = self.distance_to_camera(dim)
            #collect_data_obj.dist2camera_dik = self.dist2cam_real_cm
            # Kameranın orta noktasını bulma
            (h, w) = self.frame.shape[:2]  # w:image-width and h:image-height
            self.centerCamera = (w//2, h//2)

            # Aruconun orta noktasını bulma
            self.centerAruco = (int(marker[0][0]), int(marker[0][1]))

            # Orta noktaların arsındaki çizginin; önce pixel sonra cm uzunluğu buldurma, en son olarak derece buldurma
            dist2center_frame_px = self.centerAruco[0] - self.centerCamera[0]
            self.dist2_yaxis_real_cm = (
                self.aruco_real_width / dim) * dist2center_frame_px

            # Hipotenüs
            self.dist2cam_real_cm = math.sqrt(
                self.dist2cam_real_cm**2 + self.dist2_yaxis_real_cm**2)
            #collect_data_obj.dist2camera = self.dist2cam_real_cm

            self.angle = round(math.degrees(
                math.atan(self.dist2_yaxis_real_cm / self.dist2cam_real_cm)))
            #collect_data_obj.angle = self.angle

            if not (self.id in self.ids):
                self.ids.append(self.id)
                self.target = Aruco(ID=self.id,
                                    dist2cam=self.dist2cam_real_cm,
                                    angle=self.angle)
                print(
                    f'New target detected!! \nArUcoID: {self.id} \ndist2cam: {self.dist2cam_real_cm} \nangle: {self.angle}')
            else:
                self.target = None

            x = self.resolution[0]//2
            self.frame = cv2.line(self.frame, (x, 0),(x, self.resolution[1]), (128, 0, 0), 1)
            
            # Kamera ile Aruconun orta noktaları arasına çizgi çektirme
            self.frame = cv2.line(self.frame, self.centerCamera,self.centerAruco, (128, 0, 128), 2)
            
            # izdüşüm
            self.frame = cv2.line(self.frame, (self.centerCamera[0], self.centerAruco[1]), self.centerAruco, (0, 0, 255), 2)
            
            # Ekrana değerleri yazdırma
            strg = str(self.id)+', ' + str(np.round(self.dist2cam_real_cm, 2))+" cm"
            self.frame = cv2.putText(self.frame, "Id: " + strg, (5, 15), self.font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            
            strg = '{:.5f} cm {:.2f} degree'.format(abs(self.dist2_yaxis_real_cm), self.angle)
            self.frame = cv2.putText(self.frame, strg, (5, 30), self.font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        else:
            self.frame = cv2.putText(self.frame, "No Ids", (5, 15), self.font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            self.target = None
            self.arucoDetected = False
        _, jpeg = cv2.imencode('.jpg', self.frame)
        
        self.data = base64.b64encode(jpeg.tobytes())
        
        if self.show:
            cv2.imshow('frame', self.frame)


    def break_and_release(self):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.out = True
            self.cap.release()
            cv2.destroyAllWindows()
