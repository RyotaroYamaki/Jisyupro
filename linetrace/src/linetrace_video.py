import cv2 as cv

#detect and return the center of whiteline
def whiteline_detector(vec):
    loc_leftside = 0
    width_line = 0
    line_flag = False
    detected = False
    cnt = 0

    for i in range(20, len(vec) - 20):
        if(detected):
            break
        if(vec[i] == 255):
            if(not line_flag):
                loc_leftside = i
                line_flag = True
            cnt += 1
        else:
            if(vec[i+1] == 0 and vec[i+2] == 0):
                line_flag = False
                if(width_line < cnt):
                    width_line = cnt
                cnt = 0
                if(width_line >= 15):
                    detected = True
            else:
                cnt += 1

    center = loc_leftside + width_line / 2
    return center

#load image and trimming
cap = cv.VideoCapture(1)

while(True):
    ret, frame = cap.read()
    if(not ret):
        break
    frame2 = frame[240:]

    #rgb image to threshold image
    frame_gray = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
    threshold = (max(frame_gray[110])/2 + min(frame_gray[110])/2)
    ret, frame_thr = cv.threshold(frame_gray, threshold, 255, cv.THRESH_BINARY)

    #draw circle on the center of whitelines
    for i in range(100, 225, 50):
        center = whiteline_detector(frame_thr[i])
        cv.circle(frame, (center, 240+i), 7, (255, 0, 0), thickness=-1)

    #show image
    cv.imshow("image", frame)
    key = cv.waitKey(1)
    if(key == 27):
        break

cap.release()
cv.destroyAllWindows()
