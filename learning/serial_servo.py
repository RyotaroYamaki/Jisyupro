from pygame.locals import *
import numpy as np
import pygame
import sys
import time
import serial
import cv2 as cv
import pickle

cap = cv.VideoCapture(1)
cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M','J','P','G'))
cap.set(cv.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv.CAP_PROP_FPS, 30)

image_list = []
angle_list = []
process_num = 0
DATA_NUM = 1500

pygame.init()
screen = pygame.display.set_mode((200, 100))
pygame.display.set_caption("keyboard event")
ser = serial.Serial('/dev/ttyUSB0', 9600)

MAX_ANGLE = 32
angle = 0
isPressed_a = False
isPressed_s = False
isPressed_d = False
isPressed_f = False

time.sleep(1)
start = time.time()
while True:
    ret, frame = cap.read()
    if(not ret):
        print("Error:no camera connected")
        break
    #~12-23
    #frame_trimmed = frame[120:]
    #frame_grayscale = cv.cvtColor(frame_trimmed, cv.COLOR_BGR2GRAY)
    #frame_grayscale = cv.resize(frame_grayscale, (160, 60))

    #frame_grayscale = np.array(frame_grayscale)
    ##frame_grayscale = np.ravel(frame_grayscale)

    #12-24~
    frame_trimmed = frame[120:]
    #frame_bluescale = frame_trimmed[:,:,0]
    frame_bluescale = np.array(cv.resize(frame_trimmed, (160, 60)))

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            ser.close()
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                ser.close()
                pygame.quit()
                sys.exit()
            if event.key == K_a:
                isPressed_a = True
            if event.key == K_s:
                isPressed_s = True
            if event.key == K_d:
                isPressed_d = True
            if event.key == K_f:
                isPressed_f = True
        if event.type == KEYUP:
            if event.key == K_a:
                isPressed_a = False
            if event.key == K_s:
                isPressed_s = False
            if event.key == K_d:
                isPressed_d = False
            if event.key == K_f:
                isPressed_f = False

    if isPressed_a:
        angle -= 2
        if(angle < -MAX_ANGLE):
            angle = -MAX_ANGLE
        ser.write('a')
    elif isPressed_s:
        angle -= 1
        if(angle < -MAX_ANGLE):
            angle = -MAX_ANGLE
        ser.write('s')
    elif isPressed_d:
        angle += 1
        if(angle > MAX_ANGLE):
            angle = MAX_ANGLE
        ser.write('d')
    elif isPressed_f:
        angle += 2
        if(angle > MAX_ANGLE):
            angle = MAX_ANGLE
        ser.write('f')

    print(process_num, angle)
    image_list.append(frame_bluescale)
    angle_list.append(angle)
    
    process_num += 1
    if(process_num >= DATA_NUM):
        break
    #time.sleep(0.02)

ser.close()
cap.release()
cv.destroyAllWindows()
end = time.time()
print("end1", end - start)

image_list = np.array(image_list)
angle_list = np.array(angle_list)

with open('./data/angle_list_4.txt', 'wb') as g:
    pickle.dump(angle_list, g)

print("end2")

start = time.time()

with open('./data/image_list_4.txt', 'wb') as f:
    pickle.dump(image_list, f)

end = time.time()

print("end", end - start)
