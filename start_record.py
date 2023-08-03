
import pyrealsense2 as rs
import numpy as np
import cv2
import time

file_path = "record_data.bag"
pipeline = rs.pipeline()
config = rs.config()

width, height = 640, 480
config.enable_record_to_file(file_path)
config.enable_stream(rs.stream.depth, width, height, rs.format.z16, 30)
config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, 30)

pipeline.start(config)

try:
    print(time.time())
    while True:
        frames = pipeline.wait_for_frames()

except Exception as e:
    print(f"An error occurred: {e}")

finally:

    # Stop streaming
    pipeline.stop()

#fps도 저장해볼 것.