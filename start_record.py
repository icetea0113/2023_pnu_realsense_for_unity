
import pyrealsense2 as rs
import numpy as np
import cv2

file_path = "record_data.bag"
pipeline = rs.pipeline()
config = rs.config()

config.enable_record_to_file(file_path)
config.enable_all_streams()

pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()

finally:

    # Stop streaming
    pipeline.stop()