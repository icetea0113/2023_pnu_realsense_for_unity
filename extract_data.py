import cv2
import numpy as np
import pyrealsense2 as rs
import mediapipe as mp
import time

file_path = "skeleton_data.txt"

pipeline = rs.pipeline()
config = rs.config()

rs.config.enable_device_from_file(config, "record_data.bag")

pipeline.start(config)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

mp_drawing = mp.solutions.drawing_utils 

with open(file_path, "w") as f:
    try:
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()

            color_image = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())

            results = pose.process(cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB))

            annotated_image = color_image.copy()
            mp_drawing.draw_landmarks(annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            if results.pose_landmarks:
                for i, landmark in enumerate(results.pose_landmarks.landmark):
                    timestamp = color_frame.get_timestamp()

                    image_point = [int(landmark.x * depth_image.shape[1]), int(landmark.y * depth_image.shape[0])]

                    depth_value = depth_image[image_point[1], image_point[0]]

                    f.write(f"{timestamp}, {i}, {landmark.x}, {landmark.y}, {depth_value}\n")
                    # timestamp -> mili second

            # cv2.imshow('RGB Image', annotated_image)
            # cv2.imshow('Depth Image', depth_image)

    except RuntimeError as err:
        if err.domain == rs.error_domain.camera_disconnected and err.code == rs.camera_disconnected_error.value:
            print("Reached end of the .bag file!")
        else:
            raise err

    finally:
        # cv2.destroyAllWindows()
        pipeline.stop()
