import cv2
import mediapipe as mp
import numpy as np
import os

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

# Open a file to write the body coordinates
output_file = open('body_coordinates.txt', 'w')

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    print("POSES", mp_pose.POSE_CONNECTIONS)
    while cap.isOpened():
        ret, frame = cap.read()
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        results = pose.process(image)
        
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        try:
            # Get landmarks
            landmarks = results.pose_landmarks.landmark
            for landmark in landmarks:
                # Write x, y, z coordinates and visibility to the file
                output_file.write(f"{landmark.x}, {landmark.y}, {landmark.z}, {landmark.visibility}\n")
            
            # Optionally print one of the landmarks (e.g., LEFT_SHOULDER)
            print(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value])

        except:
            pass
        
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        print(results.pose_landmarks)
        cv2.imshow('Mediapipe Feed', image)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    output_file.close()  # Close the file once done
