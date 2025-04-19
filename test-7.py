import easyocr
import cv2 as cv
import numpy as np
import pandas as pd
import os
from datetime import datetime

reader = easyocr.Reader(['en'], gpu=False)
results = []

for file in os.listdir("assets"):
    if file.lower().endswith('.jpg'):
        path = os.path.join("assets", file)
        image = reader.readtext(path, 
                                allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        if image is None:
            continue

        # Compute areas
        areas = [cv.contourArea(np.array(bbox, dtype=np.int32)) for bbox, _, _ in image]
        max_idx = int(np.argmax(areas))
        biggest_bbox, biggest_text, biggest_conf = image[max_idx]

        print(f"Detected largest text: {biggest_text!r} (conf={biggest_conf:.2f})")
        
        results.append((file, biggest_text, biggest_conf, datetime.now()))


df = pd.DataFrame(results, columns=["Filename", "Text", "Confidence", "Timestamp"])
print(df)


