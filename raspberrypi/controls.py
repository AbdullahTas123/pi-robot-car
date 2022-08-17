import math
import multiprocessing
from motormodule import Motor
#from pynput import keyboard

# (ena,in1,in2,enb,in3,in4)
motor = Motor(25, 24, 23, 17, 27, 22)
#############

class ManualControl:

    def get_command_keyboard_from_pc(frm):
        while True:
            if frm["command"] == "ileri":
                print(frm["command"])
                motor.forward_with_time() # time.sleep default 0.01
            elif frm["command"]== "geri":
                print(frm["command"])
                motor.backward_with_time() # time.sleep default 0.01
            elif frm["command"] == "sol":
                print(frm["command"])
                motor.left()
            elif frm["command"] == "sag":
                print(frm["command"])
                motor.right()
            else:
                motor.stop()
                frm["command"] = "dur"


    def speech_move(frm):
        while True:
            if frm["command"] == "ileri":
                print(frm["command"])
                motor.forward(dist=10)
                motor.stop()
                frm["command"] = "NO"
            elif frm["command"]== "geri":
                print(frm["command"])
                motor.backward(dist=10)
                motor.stop()
                frm["command"] = "NO"
            elif frm["command"]== "calis":
                print(frm["command"])
                motor.forward(dist=10)
                motor.stop()
                frm["command"] = "NO"
            elif frm["command"] == "sol":
                print(frm["command"])
                motor.left()
                motor.stop()
                frm["command"] = "NO"
            elif frm["command"] == "sag":
                print(frm["command"])
                motor.right()
                motor.stop()
                frm["command"] = "NO"
            elif frm["command"] == "dur":
                print(frm["command"])
                motor.stop()
                frm["command"] = "NO"
            else:
                motor.stop()
    

       
class ProcessPool:
    def __init__(self) -> None:
        self.processDict = {'2': self.__process_2,
                            '3': self.__process_3,
                            '5': self.__process_5,
                            '7': self.__process_7,
                            '4': self.__process_4,
                            '1': self.__process_1}

    def execute_process(self, arucoID: str):
        self.processDict[arucoID]()

    def __process_2(self):
        print('executed process of id 2')

    def __process_3(self):
        print('executed process of id 3')

    def __process_5(self):
        print('executed process of id 5')

    def __process_4(self):
        print('executed process of id 4')

    def __process_7(self):
        print('executed process of id 7')

    def __process_1(self):
        print('executed process of id 1')


class AutonomousControl:
    def __init__(self, targets) -> None:
        self.targets = targets
        self.processPool = ProcessPool()
        self.offtrack_angel_Threshold = 5
    def run(self, phase: multiprocessing.Value):
        self.rotate360degree(phase)
        self.targets = sorted(
            self.targets, key=lambda target: target.instant_phase_angle)
        for t_indx in range(len(self.targets)):
            left_target = self.targets[t_indx]
            if (t_indx+1) == len(self.targets):
                right_target = self.targets[0]
            else:
                right_target = self.targets[t_indx+1]
            between_angle = abs(
                left_target.instant_phase_angle - right_target.instant_phase_angle)
            if between_angle > 180:
                between_angle = 360 - between_angle
            between_distance = math.sqrt(left_target.dist2cam**2+right_target.dist2cam**2 - 2 *
                                         left_target.dist2cam*right_target.dist2cam*math.cos(math.radians(between_angle)))
            left_target.right_distance = between_distance
            right_target.left_distance = between_distance

            left_angle = round(math.degrees(math.acos((left_target.dist2cam**2+between_distance **
                               2-right_target.dist2cam**2)/(2*left_target.dist2cam*between_distance))))
            right_angle = round(math.degrees(math.acos((right_target.dist2cam**2+between_distance **
                                2-left_target.dist2cam**2)/(2*between_distance*right_target.dist2cam))))

            left_target.left_target_angle += left_angle
            right_target.right_target_angle += right_angle
            print(
                f'left arucoid {left_target.arucoID} / right arucoid {right_target.arucoID}')
            print(
                f'left arucoid dist2cam {left_target.dist2cam} / right arucoid dist2cam {right_target.dist2cam}')
            print(f'between dist: {between_distance}')
            print(f'left angle {left_angle} / right angle {right_angle}')
            print('---------------------------------------------------')
        i = 0
        first = self.targets[0]
        # Motor module turn code angle(first.instant_phase_angle) sağa doğru
        while i < first.instant_phase_angle:
            motor.right()
            motor.stop(0.1)
            i += 1
        # Motor module forward code dist(first.dist2cam)
        motor.forward(dist=first.dist2cam)
        self.processPool.execute_process(arucoID=str(first.arucoID))
        # Motor module turn code angle(180-first.right_target_angle) sağa doğru
        i = 0
        while i < (180-first.right_target_angle):
            motor.right()
            motor.stop(0.1)
            i += 1
        # Motor module forward code dist(first.right_distance)
        motor.forward(dist=first.right_distance)
        for i in range(1, len(self.targets)-1):
            tg = self.targets[i]
            # Motor module turn code angle(tg.left_target_angle) sola doğru
            i = 0
            while i < tg.left_target_angle:
                motor.left()
                motor.stop(0.1)
                i += 1
            self.processPool.execute_process(arucoID=str(tg.arucoID))
            # Motor module turn code angle(180-tg.right_target_angle) sağa doğru
            i = 0
            while i < (180-tg.right_target_angle):
                motor.right()
                motor.stop(0.1)
                i += 1
            # Motor module forward code dist(tg.right_distance)
            motor.forward(dist=tg.right_distance)
        last = self.targets[-1]
        # Motor module turn code angle(last.left_target_angle) sola doğru
        i = 0
        while i < last.left_target_angle:
            motor.left()
            motor.stop(0.1)
            i += 1
        self.processPool.execute_process(arucoID=str(last.arucoID))
        motor.backward(dist=last.dist2cam)
        motor.stop()
    def rotate360degree(self, phase: multiprocessing.Value):
        while phase.value < 360:
            # motor.forward(120)
            motor.right()
            motor.stop(0.1)
            phase.value += 1



            

