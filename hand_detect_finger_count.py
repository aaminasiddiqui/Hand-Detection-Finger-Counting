import cv2
import numpy as np
from sklearn.metrics import pairwise

#GLOBAL VARIABLES
background = None
accumulated_weight = 0.5  # 0-1
# roi for red bounding box 
roi_top = 20
roi_bottom = 600
roi_right = 200
roi_left = 700


#FIND AVG BACKGROUND VALUE
def calc_accum_avg(frame, accumulated_weight):
    global background
    if background is None:
        #copy of the frame being passed in
        background = frame.copy().astype('float')
        return None

    cv2.accumulateWeighted(frame, background, accumulated_weight)


def segment(frame, threshold_min=27):
    diff = cv2.absdiff(background.astype('uint8'), frame)
    ret, thresholded = cv2.threshold(diff, threshold_min, 255, cv2.THRESH_BINARY)
    #CONTOUR
    contours, hierarchy = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return None
    else:
        hand_segment = max(contours, key=cv2.contourArea)

    return (thresholded, hand_segment)


def count_fingers(thresholded, hand_segment):
    conv_hull = cv2.convexHull(hand_segment)

    top = tuple(conv_hull[conv_hull[:, :, 1].argmin()][0])
    bottom = tuple(conv_hull[conv_hull[:, :, 1].argmax()][0])
    left = tuple(conv_hull[conv_hull[:, :, 0].argmin()][0])
    right = tuple(conv_hull[conv_hull[:, :, 0].argmax()][0])

    cX = (left[0] + right[0]) // 2
    cY = (top[1] + bottom[1]) // 2
    distance = pairwise.euclidean_distances([(cX, cY)], Y=[left, right, top, bottom])[0]
    max_distance = distance.max() - 0.4 * distance.max()

    radius = int(0.9 * max_distance)
    circumfrence = (2 * np.pi * radius)
    circular_roi = np.zeros(thresholded.shape[:2], dtype='uint8')  # black rectangle
    cv2.circle(circular_roi, (cX, cY), radius, 255, 10)
    circular_roi = cv2.bitwise_and(thresholded, thresholded, mask=circular_roi)

    contours, hierarchy = cv2.findContours(circular_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    count = 0
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)

        out_of_wrist = (cY + (0.25 * cY)) > (y + h)
        limit_pts = ((circumfrence * 0.25) > cnt.shape[0])

        if out_of_wrist and limit_pts:
            count += 1

    return count


cam = cv2.VideoCapture(0)
num_frames = 0

while True:
    ret, frame = cam.read()
    frame_copy = frame.copy()
    roi = frame[roi_top:roi_bottom, roi_right:roi_left]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    if num_frames < 60:
        calc_accum_avg(gray, accumulated_weight)
        if num_frames <= 59:
            cv2.putText(frame_copy, "DON'T ENTER. GETTING BACKGROUND...", (20, 300), cv2.FONT_HERSHEY_PLAIN, 2,
                        (0, 0, 0), 2)

    else:
        hand = segment(gray)
        if hand is not None:
            thresholded, hand_segment = hand
            cv2.drawContours(frame_copy, [hand_segment+(roi_right,roi_top)], -1, (255, 0, 0), 2)  
            fingers = count_fingers(thresholded, hand_segment)
            cv2.putText(frame_copy, str(fingers), (70, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
            cv2.imshow('Thresholded', thresholded)

    cv2.rectangle(frame_copy, (roi_left, roi_top), (roi_right, roi_bottom), (0, 0, 255), 2)
    num_frames += 1
    cv2.imshow('Finger Count', frame_copy)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cam.release()
cv2.destroyAllWindows()
