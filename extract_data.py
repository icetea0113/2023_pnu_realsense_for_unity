import cv2
import numpy as np
import pyrealsense2 as rs
import mediapipe as mp
import time
import subprocess

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
            if last_timestamp is None :
                last_timestamp = timestamp
            timestamp = timestamp - last_timestamp
            color_image = np.asanyarray(color_frame.get_data()) # 480, 640 / 720, 1280
            depth_image = np.asanyarray(depth_frame.get_data()) # y, x

            results = pose.process(cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB))
            annotated_image = color_image.copy()
            mp_drawing.draw_landmarks(annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            if results.pose_landmarks:
                #timestamp = color_frame.get_timestamp()
                for i, landmark in enumerate(results.pose_landmarks.landmark):
                    #timestamp = color_frame.get_timestamp()
                    if 0 <= landmark.x < 1 and 0 <= landmark.y < 1:
                        image_point = [int(np.floor(landmark.x * color_image.shape[1])), int(np.floor(landmark.y * color_image.shape[0]))]
                        depth_value = depth_image[image_point[1], image_point[0]]
                    else:
                        depth_value = -1
                    f.write(f"{timestamp}, {i}, {landmark.x}, {landmark.y}, {depth_value}, {landmark.z}\n")
                    #f.write(f"{timestamp}, {i}, {landmark.x}, {landmark.y}, {landmark.z}\n")
                    # timestamp -> mili second
            cv2.imshow('RGB Image', annotated_image)
            cv2.imshow('Depth Image', depth_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # cv2.destroyAllWindows()
        pipeline.stop()

# 다른 파이썬 스크립트를 실행시킵니다.
result = subprocess.run(["python", "knn_depth_data.py"], capture_output=True, text=True)

# 실행 결과를 출력합니다.
print(result.stdout)

with open("updated_skeleton_data.txt", "r") as f:
    lines = f.readlines()
data = []

for line in lines:
    parts = line.strip().split(",")
    timestamp = float(parts[0])
    joint_id = int(parts[1])
    x = float(parts[2])
    y = float(parts[3])
    depth = None if parts[4] == "None" else float(parts[4])
    z = float(parts[5])
    data.append([timestamp, joint_id, x, y, depth, z])

new_data = []
for i in range(0, len(data)-33, 33):  # 33은 관절의 개수
    data1 = data[i:i+33]
    data2 = data[i+33:i+66]

    timestamp1 = data1[0][0]
    timestamp2 = data2[0][0]
    new_timestamp = (timestamp1 + timestamp2) / 2

    new_data.extend(data1)

    for joint1, joint2 in zip(data1, data2):
        joint_id = int(joint1[1])
        x = (joint1[2] + joint2[2]) / 2
        y = (joint1[3] + joint2[3]) / 2
        depth = (joint1[4] + joint2[4]) / 2 if joint1[4] is not None and joint2[4] is not None else None
        z = (joint1[5] + joint2[5]) / 2
        new_data.append([new_timestamp, int(joint_id), x, y, depth,z])

new_data.extend(data[i+66:])

# 새로운 데이터를 파일에 저장
with open("skeleton_data_interpolated.txt", "w") as f:
    for line in new_data:
        f.write(", ".join(map(str, line)) + "\n")
print("end expand interpolated")

## https://1ch0.tistory.com/75