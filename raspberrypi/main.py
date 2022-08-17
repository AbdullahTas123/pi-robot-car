import sys
import multiprocessing
from controls import ManualControl
from cam import Camera
from server import get_command_keyboard, stream_frame, get_command
import threading

# Klavye ile hareket için mode = 1
# Sesli komut ile hareket için mode = 2
# Klavye ile hareket ve Aynı anda Raspberryden PC'ye frame aktarma için mode = 3
# Sesli komut ile hareket ve Aynı anda Raspberryden PC'ye frame aktarma için mode = 4
# default mode = 1
mode = 1

def cam(targets, isRead, phase, frm):
    # set camera object with Camera class
    camera = Camera(show=False, captureIndex=-1, camRes=(640, 480))
    camera.set_camera_settings(966.9541358947754)
    camera.set_aruco_settings(markerSize=4, totalMarkers=50, arucoWidth=6)
    
    while True:
        camera.set_frame()
        isRead.value = camera.isRead
        camera.detect_aruco()
        if camera.target is not None:
            camera.target.set_instant_phase_angle(phase.value)
            targets.append(camera.target)
        frm["data"] = camera.frame
        camera.break_and_release()
        if camera.out:
            break           


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    targets = manager.list()
    isRead = multiprocessing.Value('i', 0)
    phase = multiprocessing.Value('i', 0)
    frm = manager.dict()
    frm["command"] = "dur"
           
    
    # PC'den raspberry'yi klavye ile kontrol etmek istiyorsanız mode = 1 yapın.
    if mode == 1:
        t1 = threading.Thread(target=get_command_keyboard, args=(frm,))
        t2 = threading.Thread(target=ManualControl.get_command_keyboard_from_pc, args=(frm,))
        try:
            t1.start()
            t2.start()
        except (KeyboardInterrupt, SystemExit):
            sys.exit()
                 
    # PC'den raspberry'yi sesli komut ile kontrol etmek istiyorsanız mode = 2 yapın.
    elif mode == 2: 
        t1 = threading.Thread(target=get_command, args=(frm,))
        t2 = threading.Thread(target=ManualControl.speech_move, args=(frm,))
        try:
            t1.start()
            t2.start()
        except (KeyboardInterrupt, SystemExit):
            sys.exit()
            
    # Klavye ile hareket ve Aynı anda Raspberry'den PC'ye frame aktarma için mode = 3
    elif mode == 3: 
        p1 = multiprocessing.Process(target=cam, args=(targets, isRead, phase, frm))
        t1 = threading.Thread(target=stream_frame, args=(frm,))
        t2 = threading.Thread(target=get_command_keyboard, args=(frm,))
        t3 = threading.Thread(target=ManualControl.get_command_keyboard_from_pc, args=(frm,))
        try:
            p1.start()
            t1.start()
            t2.start()
            t3.start()
        except (KeyboardInterrupt, SystemExit):
            sys.exit()
                  
    # Sesli komut ile hareket ve Aynı anda Raspberry'den PC'ye frame aktarma için mode = 4
    elif mode == 4: 
        p1 = multiprocessing.Process(target=cam, args=(targets, isRead, phase, frm))
        t1 = threading.Thread(target=stream_frame, args=(frm,))
        t2 = threading.Thread(target=get_command, args=(frm,))
        t3 = threading.Thread(target=ManualControl.speech_move, args=(frm,))
        try:
            p1.start()
            t1.start()
            t2.start()
            t3.start()
        except (KeyboardInterrupt, SystemExit):
            p1.kill()
            sys.exit()
        

