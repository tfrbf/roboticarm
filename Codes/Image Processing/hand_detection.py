import cv2
import mediapipe as mp
import math

# Initialize the media pipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.3)

# Initialize the webcam
cap = cv2.VideoCapture(1)  # Use 0 for the default camera

# Define the threshold for what you consider as an extended finger
some_threshold = 0.11  # Adjust this value based on your specific requirements

while True:
    ret, frame = cap.read()

    # Convert the frame to RGB format
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect hands
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Define landmarks for finger tips and knuckles
            finger_tip_ids = [4, 8, 12, 16, 20]
            knuckle_ids = [2, 5, 9, 13, 17]

            # Detect and display finger distances
            for i in range(len(finger_tip_ids)):
                tip_landmark = hand_landmarks.landmark[finger_tip_ids[i]]
                knuckle_landmark = hand_landmarks.landmark[knuckle_ids[i]]

                # Calculate the Euclidean distance between fingertip and knuckle landmarks
                distance = math.dist((tip_landmark.x, tip_landmark.y), (knuckle_landmark.x, knuckle_landmark.y))

                # Determine if the finger is extended or curved based on the threshold
                if distance < some_threshold:
                    finger_status = "Curved"
                    text_color = (0, 255, 0)  # Green color for curved fingers
                else:
                    finger_status = "Extended"
                    text_color = (0, 0, 255)  # Red color for extended fingers

                # Display the distance for each finger with the appropriate color
                cv2.putText(frame, f'Finger {i + 1} Distance: {distance:.2f}', (10, 50 + 30 * i), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

    # Display the frame with hand detection
    cv2.imshow('Hand Detection with Finger Distances', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
