import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

# Initialize Video Capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)  # Set frame rate to 60 fps (adjust as needed)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image with MediaPipe Hands model
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Extract hand landmarks
            landmarks = np.array([[landmark.x, landmark.y, landmark.z] for landmark in hand_landmarks.landmark])

            # Calculate the centroid of the hand landmarks
            centroid = np.mean(landmarks, axis=0)

            # Calculate the center of twist (average x, y, z)
            center_of_twist = centroid

            # Calculate the roll, pitch, and yaw angles
            # Assuming the wrist is at landmarks[0], we can calculate angles relative to it
            wrist = landmarks[0]
            vector = centroid - wrist
            roll = np.arctan2(vector[2], vector[1]) * 180 / np.pi
            pitch = np.arctan2(vector[0], vector[1]) * 180 / np.pi
            yaw = np.arctan2(vector[0], vector[2]) * 180 / np.pi

            # Display roll, pitch, and yaw angles and center of twist
            cv2.putText(frame, f"Roll: {roll:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Pitch: {pitch:.1f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Yaw: {yaw:.2f}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.circle(frame, (int(center_of_twist[0] * frame.shape[1]), int(center_of_twist[1] * frame.shape[0])),
                       5, (0, 255, 0), -1)

    # Display the annotated image
    cv2.imshow('Hand Pose Estimation', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close all windows
cap.release()
cv2.destroyAllWindows()
