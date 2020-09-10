import os
import numpy as np
from math import *
from PIL import Image
import cv2

def coord_find(num,acc):
    return acc if num > acc else 0 if (num < 0 or num > acc) else num

def min_max_x(a, b, angle, x, y, width):

    ang = np.arctan(-(b/a)*np.tan(angle))
    x1 = x + (a*np.cos(ang)*np.cos(angle) - b*np.sin(ang)*np.sin(angle))
    x2 = x + (a*np.cos(ang + np.pi)*np.cos(angle) - b*np.sin(ang+np.pi)*np.sin(angle))

    return coord_find(min(x1,x2),width), coord_find(max(x1,x2),width)


def min_max_y(a,b,angle,x,y, height):
    epsi = 0.0001
    ang = (b/a)*(1/np.tan(angle))if np.tan(angle) != 0 else (b/a)*(1/(np.tan(angle)+epsi))
    term1 = y + (b*np.sin(np.arctan(ang))*np.cos(angle) + a*np.cos(np.arctan(ang))*np.sin(angle))
    term2 = y + (b*np.sin(np.arctan(ang) + np.pi)*np.cos(angle) + a*np.cos(np.arctan(ang) + np.pi)*np.sin(angle))

    return coord_find(min(term1,term2),height), coord_find(max(term1,term2),height)



def face_out(filename):
    
    with open(filename) as f:
        lines = list()
        for el in f:
            lines.append(el.rstrip('\n'))
    
    images = list()
    i = 0
    while i < len(lines):

        img_filename = lines[i] + '.jpg'
        width, height = Image.open(img_filename).size
        
        num_faces = int(lines[i+1])

        for j in range(num_faces):
        
            a, b, angle, x, y = lines[i+j+2].split()[0:5]
            
            x_min, x_max = min_max_x(float(a), float(b), float(angle), float(x), float(y), width)
            y_min, y_max = min_max_y(float(a), float(b), float(angle), float(x), float(y), height)
            
            if (abs(y_max-y_min) > 4 and abs(x_max-x_min) > 4):
                img_load = cv2.imread(img_filename)
                gry_img = cv2.cvtColor(img_load, cv2.COLOR_BGR2GRAY)
                face = gry_img[int(y_min): int(y_min + abs(y_max-y_min)), int(x_min):int(x_min+abs(x_max-x_min))]
                face = cv2.resize(face, (24,24))
                images.append(face)
                print(j)
            
        i = i + num_faces + 2
    return images


def face():
    
    final_faces = list()

    for i in range(1,11):

        filename = "FDDB-fold-%02d-ellipseList.txt" %i
        file_open = 'FDDB-folds/' + filename
        
        final_faces.extend(face_out(file_open))
    print(np.shape(final_faces))
    np.savez("face_images.npz", images=final_faces)
    
def non_face(folder):

    non_face = list()
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        gry_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        non_face_patch = cv2.resize(gry_img, (24,24))
        non_face.append(non_face_patch)
    print(np.shape(non_face))
    np.savez("non_face_images.npz", images=non_face)

if __name__=='__main__':
    face()

    folder = "non-faces"
    non_face(folder)