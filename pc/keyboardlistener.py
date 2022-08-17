# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 02:37:45 2022

@author: DELL
"""
from pynput import keyboard

class KeyboardListener:
    def __init__(self, text):
        self.command_text = text   
    
    def key_pynput(self, frm):
        
        def on_press(key):
            try:
                #print('Key {0} pressed'.format(key.char))
                #Add your code to drive motor
                if key.char == "w":
                    self.command_text = "ileri"
                    frm["command"] = self.command_text
                    print("ileri")
                    
                elif key.char == "a":
                    self.command_text = "sol"
                    frm["command"] = self.command_text
                    print("sol")
                    
                elif key.char == "d":
                    self.command_text = "sag"
                    frm["command"] = self.command_text
                    print("sag")
                    
                elif key.char == "s":
                    self.command_text = "geri"
                    frm["command"] = self.command_text
                    print("geri")
                    
                else:
                    self.command_text = "dur"
                    frm["command"] = self.command_text
                    print("dur")
                    
            except AttributeError:
                self.command_text = "dur"
                frm["command"] = self.command_text
                print("dur")
                #print('Key {0} pressed'.format(key))
                #Add Code
                
        def on_release(key):
            #print('{0} released'.format(key))
            #Add your code to stop motor
            self.command_text = "dur"
            frm["command"] = self.command_text
            print("dur")
            
            if key == keyboard.Key.esc:
                # Stop listener
                self.command_text = "dur"
                frm["command"] = self.command_text
                print("dur")
                # Stop the Robot Code
                return False
            
        # Collect events until released
        with keyboard.Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()
   

    