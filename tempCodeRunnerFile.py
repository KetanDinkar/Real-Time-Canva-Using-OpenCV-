import cv2
import mediapipe as mp

# Mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)

# Drawing canvas and previous point
canvas = None
prev_x, prev_y = 0, 0

# Pen color and thickness
pen_color = (0, 0, 255)  # Red
pen_thickness = 8

# Finger tip landmark indices
finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
finger_mcp = [6, 10, 14, 18]   # Their respective lower joints

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    # Create canvas if not initialized
    if canvas is None:
        canvas = frame.copy()

    # Process the frame
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark

            # Get index fingertip position
            x = int(landmarks[8].x * w)
            y = int(landmarks[8].y * h)

            # Draw dot on finger
            cv2.circle(frame, (x, y), 10, pen_color, -1)

            # Print index finger position
            print(f"Index Finger Position: x={x}, y={y}")

            # Check if only index finger is up
            fingers_up = 0
            for tip, mcp in zip(finger_tips, finger_mcp):
                if landmarks[tip].y < landmarks[mcp].y:
                    fingers_up += 1

            if fingers_up == 1:  # Only index finger is up
                if prev_x != 0 and prev_y != 0:
                    cv2.line(canvas, (prev_x, prev_y), (x, y), pen_color, pen_thickness)
                prev_x, prev_y = x, y
            else:
                prev_x, prev_y = 0, 0  # Stop drawing if index is not the only finger up

    else:
        prev_x, prev_y = 0, 0

    # Merge canvas with frame
    blended = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

    # Show instructions
    cv2.rectangle(blended, (0, 0), (w, 40), (0, 0, 0), -1)
    cv2.putText(blended, "R/G/B: Change Color | C: Clear | Q: Quit | Only index finger = draw",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Display
    cv2.imshow("Air Canvas - Finger Drawing", blended)

    # Key Controls
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        pen_color = (0, 0, 255)
    elif key == ord('g'):
        pen_color = (0, 255, 0)
    elif key == ord('b'):
        pen_color = (255, 0, 0)
    elif key == ord('c'):
        canvas = None

# Release resources
cap.release()
cv2.destroyAllWindows()
