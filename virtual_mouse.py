import mediapipe as mp
import cv2

cap = cv2.VideoCapture(0)
mphands = mp.solutions.hands
hands = mphands.Hands(4)
mpdraw = mp.solutions.drawing_utils

while True:
  suc, frame = cap.read()
  frame = cv2.flip(frame,1)
  frame = cv2.GaussianBlur(frame, (5, 5), 0)

  frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  results = hands.process(frame_rgb)
  #print(results.multi_hand_landmarks)

  if results.multi_hand_landmarks:
      for handlms in results.multi_hand_landmarks: # handlms has the coordinates of each pt
          mpdraw.draw_landmarks(frame, handlms, mphands.HAND_CONNECTIONS)
          for id, lm in enumerate(handlms.landmark):
              #print(id, lm)
              h,w,_ = frame.shape
              cx, cy = int(lm.x*w), int(lm.y * h)
              print(id, cx, cy)



  cv2.imshow("V", frame)
  if cv2.waitKey(1) & 0xFF == ord('q'):
        break