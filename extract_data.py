import cv2
import numpy as np
import pyrealsense2 as rs
import mediapipe as mp
import time

file_path = "skeleton_data.txt"

pipeline = rs.pipeline()
config = rs.config()

rs.config.enable_device_from_file(config, "record_data.bag")

profile = pipeline.start(config)

depth_sensor = profile.get_device().first_depth_sensor()    # depth sensor에 대한 것들을 얻자
depth_scale = depth_sensor.get_depth_scale()                # 깊이 센서의 깊이 스케일 얻음

print(depth_scale)
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

mp_drawing = mp.solutions.drawing_utils 
last_timestamp = None

with open(file_path, "w") as f:
    try:
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()

            timestamp = frames.get_timestamp()
            if last_timestamp is not None and timestamp < last_timestamp:
                print("End of .bag file reached")
                break
            last_timestamp = timestamp

            color_image = np.asanyarray(color_frame.get_data()) # 480, 640 / 720, 1280
            depth_image = np.asanyarray(depth_frame.get_data()) # y, x

            results = pose.process(cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB))
            annotated_image = color_image.copy()
            mp_drawing.draw_landmarks(annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            if results.pose_landmarks:
                timestamp = color_frame.get_timestamp()
                for i, landmark in enumerate(results.pose_landmarks.landmark):
                    timestamp = color_frame.get_timestamp()

                    if 0 <= landmark.x <= 1 and 0 <= landmark.y <= 1:
                        image_point = [int(round(landmark.x * color_image.shape[1])), int(round(landmark.y * color_image.shape[0]))]
                        depth_value = depth_image[image_point[1], image_point[0]]
                    else:
                        depth_value = None

                    f.write(f"{timestamp}, {i}, {landmark.x}, {landmark.y}, {depth_value}\n")
                    #f.write(f"{timestamp}, {i}, {landmark.x}, {landmark.y}, {landmark.z}\n")
                    # timestamp -> mili second
            print("-----------------------------------------")
            cv2.imshow('RGB Image', annotated_image)
            cv2.imshow('Depth Image', depth_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # cv2.destroyAllWindows()
        pipeline.stop()


## https://1ch0.tistory.com/75