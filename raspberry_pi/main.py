import cv2 as cv
import time
import serial
import tflite_runtime.interpreter as tflite
import numpy as np

ser = serial.Serial('/dev/ttyUSB0', 9600)

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M','J','P','G'))
cap.set(cv.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv.CAP_PROP_FPS, 30)

THRESHOLD = 225
interpreter = tflite.Interpreter(model_path='saved_model.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_shape = input_details[0]['shape']

interpreter2 = tflite.Interpreter(model_path='ssd_mobilenet_v1_1_metadata_1.tflite')
interpreter2.allocate_tensors()
input_details2 = interpreter2.get_input_details()
output_details2 = interpreter2.get_output_details()

MAX_ANGLE = 32
angle = 0
LINE_PIXELS = 30
traffic_light = False
traffic_n = 0
traffic_p = 0
traffic_p2 = 0

def update_angle(angle, output_angle):
    if(output_angle - angle > 3):
        keyword = 'f'
        angle += 2
    elif(output_angle - angle > 1):
        keyword = 'd'
        angle += 1
    elif(output_angle - angle < -3):
        keyword = 'a'
        angle -= 2
    elif(output_angle - angle < -1):
        keyword = 's'
        angle -= 1
    else:
        keyword = 'c'

    if(angle > MAX_ANGLE):
        angle = MAX_ANGLE
    if(angle < -MAX_ANGLE):
        angle = -MAX_ANGLE

    return keyword, angle

def no_lines(angle):
    if(angle >= 0):
        keyword = 'f'
        angle += 2
    else:
        keyword = 'a'
        angle -= 2

    if(angle > MAX_ANGLE):
        angle = MAX_ANGLE
    if(angle < -MAX_ANGLE):
        angle = -MAX_ANGLE

    return keyword, angle

while True:
    ret, frame = cap.read()
    if not ret:
        print("no camera connected")
        break

    #detection
    frame2 = cv.resize(frame, (300, 300))
    img = cv.cvtColor(frame2, cv.COLOR_BGR2RGB)
    img = img.reshape(1, img.shape[0], img.shape[1], img.shape[2])
    img = img.astype(np.uint8)

    interpreter2.set_tensor(input_details2[0]['index'], img)

    interpreter2.invoke()

    #boxes = interpreter2.get_tensor(output_details2[0]['index'])
    labels = interpreter2.get_tensor(output_details2[1]['index'])
    scores = interpreter2.get_tensor(output_details2[2]['index'])

    for i in range(labels.shape[1]):
        if int(labels[0, i]) == 9 and scores[0, i] >= 0.25:
            print("traffic light", scores[0, i])
            traffic_n = 1

    print(traffic_n, traffic_p, traffic_p2)
    if traffic_n == 1 and traffic_p == 1:
        traffic_light = True
    if traffic_n == 0 and traffic_p == 0 and traffic_p2 == 0:
        traffic_light = False

    #learning
    if not traffic_light:
        frame_grayscale = frame[120:,:,0]
        frame_resized = np.array(cv.resize(frame_grayscale, (40, 30)))
        input_data = np.where(frame_resized < THRESHOLD, 0, 1).astype(np.float32)
        input_data = input_data.reshape(1, -1)
        print(np.sum(input_data))

        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        #print(np.sum(input_data), output_data)
        output_angle = np.round(output_data)

        if(np.sum(input_data) < LINE_PIXELS):
            keyword, angle = no_lines(angle)
            print("!")
        else:
            keyword, angle = update_angle(angle, output_angle)
        print(angle, output_angle)
    else:
        keyword = 'p'

    ser.write(keyword.encode())

    traffic_p2 = traffic_p
    traffic_p = traffic_n
    traffic_n = 0

ser.close()
cap.release()

