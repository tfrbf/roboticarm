import serial
import cv2
import math
import mediapipe as mp

try:
    serialcomm = serial.Serial('COM1', 9600)
    serialcomm.timeout = 1
except serial.SerialException as e:
    print(f"Error initializing serial communication: {e}")
    exit()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(1)
calibrating = False
calibrated = False
min_distance = float('inf')
max_distance = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Extracting landmarks for thumb and index finger
            thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Converting landmarks to pixel coordinates
            thumb_x, thumb_y = int(thumb.x * frame.shape[1]), int(thumb.y * frame.shape[0])
            index_x, index_y = int(index.x * frame.shape[1]), int(index.y * frame.shape[0])

            # Calculating the difference between vertical and horizontal coordinates
            diff_x = index_x - thumb_x
            diff_y = index_y - thumb_y

            # Calculating the angle using atan2
            angle = math.atan2(diff_y, diff_x)
            angle_degrees = math.degrees(angle)

            # Printing the coordinates, differences, and angle
            print(f"Thumb Tip: ({thumb_x}, {thumb_y}), Index Finger Tip: ({index_x}, {index_y}), "
                  f"Diff X: {diff_x}, Diff Y: {diff_y}, Angle: {angle_degrees:.2f} degrees")

            # Drawing points and lines on the frame
            cv2.circle(frame, (thumb_x, thumb_y), 7, (0, 255, 255), 1)
            cv2.circle(frame, (index_x, index_y), 7, (0, 255, 255), 1)
            cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), (0, 255, 0), 2)

            # Calculating distance between thumb and index finger
            distance = int(math.sqrt(diff_x ** 2 + diff_y ** 2) * 1.0)
            distance = int((distance / 110) * 255)

            if calibrating:
                min_distance = min(min_distance, distance)
                max_distance = max(max_distance, distance)
                cv2.putText(frame, f"Min: {min_distance} Max: {max_distance}", (20, 50), cv2.FONT_HERSHEY_COMPLEX, .7, (255, 255, 255), 1)
                cv2.putText(frame, "Calibrating... Move your hand to set min and max distances", (20, 30), cv2.FONT_HERSHEY_COMPLEX, .7, (255, 255, 255), 1)
            elif calibrated:
                if max_distance > min_distance:
                    distance = max(min_distance, min(distance, max_distance))  # Clamping distance between min and max
                    distance = int((distance - min_distance) / (max_distance - min_distance) * 255)

                cv2.putText(frame, str(distance), (20, 30), cv2.FONT_HERSHEY_COMPLEX, .7, (255, 255, 255), 1)
                e = '\n'
                try:
                    serialcomm.write(f"{distance}{e}".encode())
                except serial.SerialException as e:
                    print("Serial communication error:", e)
            else:
                cv2.putText(frame, "Press 'c' to calibrate", (20, 30), cv2.FONT_HERSHEY_COMPLEX, .7, (255, 255, 255), 1)

    cv2.imshow('Image', frame)
    key = cv2.waitKey(20)
    if key & 0xFF == ord('c'):
        if not calibrating and not calibrated:
            calibrating = True
        elif calibrating:
            calibrating = False
            calibrated = True

    if key & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
