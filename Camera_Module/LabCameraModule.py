# camera_module.py
import cv2
import numpy as np
import requests

class LabCameraModule:
    def __init__(self, source):
        self.is_ip_camera = isinstance(source, str)
        if self.is_ip_camera:
            self.base_url = source
            self.video_url = f"{self.base_url}/video"
            self.image_url = f"{self.base_url}/shot.jpg"
        else:
            self.camera_index = source

    def get_image(self):
        if self.is_ip_camera:
            try:
                response = requests.get(self.image_url, stream=True)
                response.raise_for_status()
                image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
                image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                return image
            except requests.RequestException as e:
                print(f"Error fetching image: {e}")
                return None
        else:
            cap = cv2.VideoCapture(self.camera_index)
            ret, frame = cap.read()
            cap.release()
            return frame if ret else None