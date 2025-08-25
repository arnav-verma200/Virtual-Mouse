import mediapipe as mp
import cv2
import math as m
import time
import string
from pynput.keyboard import Controller, Key

cap = cv2.VideoCapture(1)
keyboard = Controller()
mphands = mp.solutions.hands
hands = mphands.Hands(max_num_hands=1)
mpdraw = mp.solutions.drawing_utils

letters = list(string.ascii_uppercase) + ["Space", "Backspace", "Enter"]

selected_letter = None
enter_time = None
typed = False
typed_txt = ""


while True:
    suc, frame = cap.read()
    if not suc:
        break
    
    coords = []
    frame = cv2.flip(frame, 1)
    sf = 0.6
    h, w = frame.shape[:2]
    h2, w2 = int(h * sf), int(w * sf)
    frame = cv2.resize(frame, (w2, h2))
    #======================================================================================================================
    # Fixed layout: two rows for alphabet, third row for Space and Backspace
    box_w = int(70 * sf)
    box_h = int(70 * sf)
    margin = int(15 * sf)
    start_x = margin
    start_y = int(130 * sf)
    letters_per_row = 13
    # First row: A-M
    for idx, letter in enumerate(letters[:letters_per_row]):
        x1 = start_x + idx * (box_w + margin)
        y1 = start_y
        x2 = x1 + box_w
        y2 = y1 + box_h
        cv2.rectangle(frame, (x1, y1), (x2, y2), (128,128,128), 2)  # grey border
        text_size = cv2.getTextSize(letter, cv2.FONT_HERSHEY_SIMPLEX, 1.3 * sf, 2)[0]
        text_x = x1 + (box_w - text_size[0]) // 2
        text_y = y1 + (box_h + text_size[1]) // 2
        cv2.putText(frame, letter, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.3 * sf, (0,0,0), 2)  # black text
        coords.append([letter, x1, y1, x2, y2])
    # Second row: N-Z
    for idx, letter in enumerate(letters[letters_per_row:letters_per_row*2]):
        x1 = start_x + idx * (box_w + margin)
        y1 = start_y + box_h + margin
        x2 = x1 + box_w
        y2 = y1 + box_h
        cv2.rectangle(frame, (x1, y1), (x2, y2), (128,128,128), 2)
        text_size = cv2.getTextSize(letter, cv2.FONT_HERSHEY_SIMPLEX, 1.3 * sf, 2)[0]
        text_x = x1 + (box_w - text_size[0]) // 2
        text_y = y1 + (box_h + text_size[1]) // 2
        cv2.putText(frame, letter, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.3 * sf, (0,0,0), 2)
        coords.append([letter, x1, y1, x2, y2])
    # Third row: Space, Backspace, Enter
    special_w = int(2.5 * box_w)
    space_x1 = start_x
    space_y1 = start_y + 2 * (box_h + margin)
    space_x2 = space_x1 + special_w
    space_y2 = space_y1 + box_h
    cv2.rectangle(frame, (space_x1, space_y1), (space_x2, space_y2), (128,128,128), 2)
    text_size = cv2.getTextSize("Space", cv2.FONT_HERSHEY_SIMPLEX, 1.3 * sf, 2)[0]
    text_x = space_x1 + (special_w - text_size[0]) // 2
    text_y = space_y1 + (box_h + text_size[1]) // 2
    cv2.putText(frame, "Space", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.3 * sf, (0,0,0), 2)
    coords.append(["Space", space_x1, space_y1, space_x2, space_y2])
    backspace_x1 = space_x2 + margin
    backspace_y1 = space_y1
    backspace_x2 = backspace_x1 + special_w
    backspace_y2 = backspace_y1 + box_h
    cv2.rectangle(frame, (backspace_x1, backspace_y1), (backspace_x2, backspace_y2), (128,128,128), 2)
    text_size = cv2.getTextSize("Backspace", cv2.FONT_HERSHEY_SIMPLEX, 1.3 * sf, 2)[0]
    text_x = backspace_x1 + (special_w - text_size[0]) // 2
    text_y = backspace_y1 + (box_h + text_size[1]) // 2
    cv2.putText(frame, "Backspace", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.3 * sf, (0,0,0), 2)
    coords.append(["Backspace", backspace_x1, backspace_y1, backspace_x2, backspace_y2])
    enter_x1 = backspace_x2 + margin
    enter_y1 = space_y1
    enter_x2 = enter_x1 + special_w
    enter_y2 = enter_y1 + box_h
    cv2.rectangle(frame, (enter_x1, enter_y1), (enter_x2, enter_y2), (128,128,128), 2)
    text_size = cv2.getTextSize("Enter", cv2.FONT_HERSHEY_SIMPLEX, 1.3 * sf, 2)[0]
    text_x = enter_x1 + (special_w - text_size[0]) // 2
    text_y = enter_y1 + (box_h + text_size[1]) // 2
    cv2.putText(frame, "Enter", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.3 * sf, (0,0,0), 2)
    coords.append(["Enter", enter_x1, enter_y1, enter_x2, enter_y2])

    #===============================================================================================================================
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            mpdraw.draw_landmarks(frame, handlms, mphands.HAND_CONNECTIONS)

            llm = []
            for id, lm in enumerate(handlms.landmark):
                cx, cy = int(lm.x * w2), int(lm.y * h2)
                llm.append([id, cx, cy])

            if len(llm) > 8:  # Ensure landmarks exist
                cv2.circle(frame, (llm[8][1], llm[8][2]), 8, (0, 0, 255), -1)
                #cv2.line(frame, (llm[4][1], llm[4][2]), (llm[8][1], llm[8][2]), (255, 0, 0), 2)
                #dist = m.hypot(llm[4][1] - llm[8][1], llm[4][2] - llm[8][2])
                #min_dist = 25

                inside_any = False
                
                for letter, x1, y1, x2, y2 in coords:
                    if x1 <= llm[8][1] <= x2 and y1 <= llm[8][2] <= y2:
                        inside_any = True
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
                        if selected_letter != letter:
                            selected_letter = letter
                            enter_time = time.time()
                            typed = False
                        elif not typed and time.time() - enter_time >= 1:
                            if letter == "Space":
                                typed_txt += " "
                                keyboard.press(Key.space)
                                keyboard.release(Key.space)
                            elif letter == "Backspace":
                                typed_txt = typed_txt[:-1]
                                keyboard.press(Key.backspace)
                                keyboard.release(Key.backspace)
                            elif letter == "Enter":
                                typed_txt += "\n"
                                keyboard.press(Key.enter)
                                keyboard.release(Key.enter)
                            else:
                                typed_txt += letter
                                keyboard.press(letter.lower())
                                keyboard.release(letter.lower())
                            typed = True

                if not inside_any:
                    selected_letter = None
                    enter_time = None
                    typed = False

    # Always display typed text at the top
    cv2.putText(frame, f"Typed txt is : {typed_txt}", (30,60), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0),2)

    cv2.imshow("V", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(typed_txt)
        break

cap.release()
cv2.destroyAllWindows()