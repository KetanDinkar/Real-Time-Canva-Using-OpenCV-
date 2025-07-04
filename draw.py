import cv2
import mediapipe as mp
import numpy as np

# Mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Drawing canvas and previous point
canvas = None
prev_x, prev_y = 0, 0

# Pen color and thickness
pen_color = (0, 0, 255)
pen_thickness = 8

# Finger tip landmark indices
finger_tips = [8, 12, 16, 20]
finger_mcp = [6, 10, 14, 18]

# Drawing state
is_drawing = False

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    if canvas is None:
        canvas = np.zeros_like(frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    is_drawing = False  # reset each frame

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark

            x = int(landmarks[8].x * w)
            y = int(landmarks[8].y * h)

            cv2.circle(frame, (x, y), 10, pen_color, -1)

            fingers_up = 0
            for tip, mcp in zip(finger_tips, finger_mcp):
                if landmarks[tip].y < landmarks[mcp].y:
                    fingers_up += 1

            if fingers_up == 1:
                is_drawing = True
                print(f"Pen Coordinates: ({x}, {y})")  # <-- Added print statement here
                if prev_x != 0 and prev_y != 0:
                    cv2.line(canvas, (prev_x, prev_y), (x, y), pen_color, pen_thickness)
                prev_x, prev_y = x, y
            else:
                prev_x, prev_y = 0, 0
    else:
        prev_x, prev_y = 0, 0

    # Merge canvas directly
    output = frame.copy()
    mask = np.any(canvas != 0, axis=2)
    output[mask] = canvas[mask]

    # UI Overlay
    overlay = output.copy()
    cv2.rectangle(overlay, (0, 0), (w, 60), (0, 0, 0), -1)
    output = cv2.addWeighted(overlay, 0.6, output, 0.4, 0)

    # Instructions
    draw_state_text = "Pen: Drawing ON" if is_drawing else "Pen: Drawing OFF"
    draw_state_color = (0, 255, 0) if is_drawing else (0, 0, 255)
    cv2.putText(output, draw_state_text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, draw_state_color, 2)

    cv2.putText(output, "R: Red | G: Green | B: Cyan | M: Magenta | C: Clear | Q: Quit",
                (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    # Pen color preview
    cv2.rectangle(output, (w - 70, 10), (w - 20, 40), pen_color, -1)
    cv2.putText(output, "Pen", (w - 120, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    # Show window
    cv2.imshow("Air Canvas - Finger Drawing", output)

    # Controls
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        pen_color = (0, 0, 255)
    elif key == ord('g'):
        pen_color = (0, 255, 0)
    elif key == ord('b'):
        pen_color = (255, 255, 0)
    elif key == ord('m'):
        pen_color = (255, 0, 255)
    elif key == ord('c'):
        canvas = np.zeros_like(frame)

# Cleanup
cap.release()
cv2.destroyAllWindows()
