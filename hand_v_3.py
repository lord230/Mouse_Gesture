import cv2
import mediapipe as mp
import math
import time
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

pyautogui.FAILSAFE = False
screen_width, screen_height = pyautogui.size()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

prev_time = 0
click_active = False
scroll_cooldown = 0

def fingers_up(landmarks, image_h):
   
    tips = [8, 12, 16, 20]
    states = []
    for tip_id in tips:
        tip_y = landmarks.landmark[tip_id].y * image_h
        pip_y = landmarks.landmark[tip_id - 2].y * image_h
        states.append(tip_y < pip_y)
    return states  

def detect_click(index_x, index_y, thumb_x, thumb_y):
    global click_active
    distance = math.hypot(index_x - thumb_x, index_y - thumb_y)
    if distance < 30:
        if not click_active:
            print("Click")
            pyautogui.click()
            click_active = True
    else:
        click_active = False

def detect_scroll(finger_states):
    global scroll_cooldown
    if scroll_cooldown > 0:
        scroll_cooldown -= 1
        return

    fingers_up_count = sum(finger_states)

    if fingers_up_count == 4:
        print("Scroll Up ")
        pyautogui.scroll(50)
        scroll_cooldown = 10

    elif fingers_up_count == 0:
        print("Scroll Down ")
        pyautogui.scroll(-50)
        scroll_cooldown = 10

with mp_hands.Hands(
    model_complexity=0,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        image = cv2.resize(image, (640, 480))
        image_h, image_w, _ = image.shape

        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time
        cv2.putText(image, f"FPS: {int(fps)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = hands.process(image_rgb)
        image_rgb.flags.writeable = True
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

                def pos(id):
                    lm = hand_landmarks.landmark[id]
                    return int(lm.x * screen_width), int(lm.y * screen_height)

                index_x, index_y = pos(mp_hands.HandLandmark.INDEX_FINGER_TIP)
                thumb_x, thumb_y = pos(mp_hands.HandLandmark.THUMB_TIP)

      
                pyautogui.moveTo(index_x, index_y)

                detect_click(index_x, index_y, thumb_x, thumb_y)

                finger_states = fingers_up(hand_landmarks, image_h)
                detect_scroll(finger_states)

        cv2.imshow('Hand Mouse & Scroll', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
