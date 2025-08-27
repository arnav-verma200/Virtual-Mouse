import mediapipe as mp
import cv2
from pynput.mouse import Button, Controller
import pyautogui
import math

# Initialize mouse and screen
mouse = Controller()
screen_w, screen_h = pyautogui.size()

# Capture webcam
cap = cv2.VideoCapture(1)

# Mediapipe hands
mphands = mp.solutions.hands
hands = mphands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mpdraw = mp.solutions.drawing_utils

# Smoothing
last_x, last_y = 0, 0
smooth_factor = 0.2

# Click states
left_clicking = False
right_clicking = False
scrolling_up = False
scrolling_down = False

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)  # mirror view
    h, w = frame.shape[:2]

    # Process with mediapipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            mpdraw.draw_landmarks(frame, handlms, mphands.HAND_CONNECTIONS)

            # Landmarks (for gestures)
            tx, ty = int(handlms.landmark[4].x * w), int(handlms.landmark[4].y * h)    # thumb tip
            ix, iy = int(handlms.landmark[8].x * w), int(handlms.landmark[8].y * h)    # index tip
            mx, my = int(handlms.landmark[12].x * w), int(handlms.landmark[12].y * h)  # middle tip
            rx, ry = int(handlms.landmark[16].x * w), int(handlms.landmark[16].y * h)  # ring tip
            px, py = int(handlms.landmark[20].x * w), int(handlms.landmark[20].y * h)  # pinky tip

            # Palm center in normalized coordinates
            cx_n = (handlms.landmark[0].x + handlms.landmark[5].x + handlms.landmark[9].x) / 3
            cy_n = (handlms.landmark[0].y + handlms.landmark[5].y + handlms.landmark[9].y) / 3

            # Map palm center to full screen
            target_x = int(cx_n * screen_w)
            target_y = int(cy_n * screen_h)

            # Apply smoothing
            mx_s = int(last_x + (target_x - last_x) * smooth_factor)
            my_s = int(last_y + (target_y - last_y) * smooth_factor)
            mouse.position = (mx_s, my_s)
            last_x, last_y = mx_s, my_s

            # Distances for gestures
            index_thumb_dist = math.hypot(tx - ix, ty - iy)    # thumb + index
            middle_thumb_dist = math.hypot(tx - mx, ty - my)   # thumb + middle
            ring_thumb_dist = math.hypot(tx - rx, ty - ry)     # thumb + ring
            pinky_thumb_dist = math.hypot(tx - px, ty - py)    # thumb + pinky
            pinch_threshold = 30

            # Left click (thumb + index pinch)
            if index_thumb_dist < pinch_threshold:
                if not left_clicking:
                    mouse.click(Button.left, 1)
                    left_clicking = True
            else:
                left_clicking = False

            # Right click (thumb + middle pinch)
            if middle_thumb_dist < pinch_threshold:
                if not right_clicking:
                    mouse.click(Button.right, 1)
                    right_clicking = True
            else:
                right_clicking = False

            # Scroll Up (thumb + ring pinch)
            if ring_thumb_dist < pinch_threshold:
                if not scrolling_up:
                    pyautogui.scroll(50)  # positive value → scroll up
                    scrolling_up = True
            else:
                scrolling_up = False

            # Scroll Down (thumb + pinky pinch)
            if pinky_thumb_dist < pinch_threshold:
                if not scrolling_down:
                    pyautogui.scroll(-50)  # negative value → scroll down
                    scrolling_down = True
            else:
                scrolling_down = False

    resize_factor = 0.67  # Change this value for desired window size
    frame = cv2.resize(frame, (int(w * resize_factor), int(h * resize_factor)))
    cv2.imshow("Hand Mouse Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
