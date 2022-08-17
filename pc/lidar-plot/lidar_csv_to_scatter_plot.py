# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 02:14:17 2022

@author: DELL
"""

import matplotlib.pyplot as plt
import numpy as np

def file_read(f):
    with open(f) as data:
        measures = [line.split(",") for line in data]
    angles = []
    distances = []
    for measure in measures:
        angles.append(float(measure[0]))
        distances.append(float(measure[1]))
    
    ## 655 li dataları 0 olarak kaydediyoruz.
    for i,d in enumerate(distances):
        if distances[i] > 25:
            distances[i] = 0

    angles = np.array(angles)
    distances = np.array(distances)
    return angles, distances


def rotate_vector(data, angle):
    # make rotation matrix
    theta = np.radians(angle)
    co = np.cos(theta)
    si = np.sin(theta)
    rotation_matrix = np.array(((co, -si), (si, co)))
    # rotate data vector
    rotated_vector = data.dot(rotation_matrix)
    # return index of elbow
    return rotated_vector


def plot_1_csv():
    
    for i in range(1):
        ang, dist = file_read("lidar"+ str(i) +".csv") 
        # ilk satır x, y değerleri, siliyoruz.
        ang = np.delete(ang,0)
        dist = np.delete(dist,0)
        ang = np.radians(ang)
        ox = np.cos(ang) * dist
        oy = np.sin(ang) * dist

                    
        plt.scatter(ox, oy, c ="blue")
            
        # To show the plot
        plt.show()
        

def plot_all_csv():
    
    for i in range(29):
        ang, dist = file_read("csv/lidar"+ str(i) +".csv")
        # ilk satır x, y değerleri, siliyoruz.
        ang = np.delete(ang,0)
        dist = np.delete(dist,0)
        ang = np.radians(ang)
        ox = np.cos(ang) * dist
        oy = np.sin(ang) * dist
        # ilk csv dışındaki csv lerdeki y değerlerine 1.2(120cm) ekliyoruz. Plotta üst üste eklediğmizde düzgün gözüksün.
        """
        stack_data = np.vstack((ox, oy)).T
        rotated_data = rotate_vector(stack_data, -10) 
        plt.scatter(rotated_data[:, 0], rotated_data[:, 1], c="blue")
        
        """
        if i == 0:
            oy = oy
        else:
            for j in range(181):
                if oy[j] == 0:
                    oy[j] = oy[j]
                else:
                    oy[j] = oy[j] + i*1.2
        ax = plt.gca()
        #ax.set_xlim([0, 1000])
        ax.set_ylim([0, np.max(oy)*1.2])
        plt.scatter(ox, oy, c ="blue")
        
    # To show the plot
    plt.show()
        

if __name__ == "__main__":      
    plot_all_csv()       
        