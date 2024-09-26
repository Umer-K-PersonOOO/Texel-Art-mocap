import cv2
import mediapipe as mp
import numpy as np
import mediapipe.tasks as py
from mediapipe.tasks.python import vision as vs
import time


mp_drawing = mp.solutions.drawing_utils
hand_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode
def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    print('hand landmarker result: {}'.format(result))

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)
cap = cv2.VideoCapture(0)




with HandLandmarker.create_from_options(options) as landmarker:
    #print("POSES", mp_pose.POSE_CONNECTIONS)
    previous = time.time()
    while cap.isOpened():
        ret, frame = cap.read()
        timem = int(cap.get(cv2.CAP_PROP_POS_MSEC))
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        
        
        
        

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        hand_detection = landmarker.detect_async(mp_image, timem)
        
        
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        try:
            
            handmark = landmarker.result_callback
            #print(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value])
        except:
            pass
            
       
        hand_drawing.draw_landmarks(image, hand_detection, mp_pose.POSE_CONNECTIONS)
        
        cv2.imshow('Mediapipe Feed', image)
            
        #cv2.imshow('Mediapipe Feed', mp_image)
            
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
        
    
        
    cap.release()
    cv2.destroyAllWindows()