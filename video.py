import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe solutions for drawing, pose, and hands
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_holistic = mp.solutions.holistic



# Initialize webcam
cap = cv2.VideoCapture("videos/video.mp4")

# Open a file to write the body coordinates
output_file = open('body_coordinates.txt', 'w')

# Initialize both pose and hands detection modules
with mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8) as pose, \
     mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands, \
     mp_holistic.Holistic(smooth_landmarks=True) as holistic:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)

        # Convert the BGR frame to RGB before processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False  # Minor speedup by passing by reference

        # Detect pose landmarks
        pose_results = pose.process(rgb_frame)

        # Detect hand landmarks
        hand_results = hands.process(rgb_frame)

        rgb_frame.flags.writeable = True
        frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

        # If pose landmarks are detected
        if pose_results.pose_landmarks:
            landmarks = pose_results.pose_landmarks.landmark
            for idx, landmark in enumerate(landmarks):
                output_file.write(f"{idx}: {landmark.x}, {landmark.y}, {landmark.z}, {landmark.visibility}\n")

            # Draw pose landmarks on the frame
            mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # If hand landmarks are detected
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Show the frame in a window
        cv2.imshow('Pose and Hand Landmarks', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    output_file.close()  # Close the file
