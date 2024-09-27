import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8) as pose:
    print("POSES", mp_pose.POSE_CONNECTIONS)
    while cap.isOpened():
        ret, frame = cap.read()
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        results = pose.process(image)
        
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        try:
            landmarks = results.pose_landmarks.landmark
            print(landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
        except:
            pass
        
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        cv2.imshow('Mediapipe Feed', image)
        
        #leftH_left = np.min(landmarks[16].x, landmarks[18].x,landmarks[20].x,landmarks[22].x)
        #leftH_right = np.max(landmarks[16].x, landmarks[18].x,landmarks[20].x,landmarks[22].x)
        #leftH_top = 
        #rightH_left = np.min(landmarks[15].x, landmarks[17].x,landmarks[19].x,landmarks[21].x)
        #rightH_right = np.max(landmarks[15].x, landmarks[17].x,landmarks[19].x,landmarks[21].x)

        
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()