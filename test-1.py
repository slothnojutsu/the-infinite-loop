import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread("assets/car-0.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian Blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Edge detection using Canny
edges = cv2.Canny(blurred, 100, 200)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Loop through contours and filter potential license plates
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
    x, y, w, h = cv2.boundingRect(approx)

    # Filter based on aspect ratio (License plates are usually rectangular)
    aspect_ratio = w / float(h)
    if 2 < aspect_ratio < 6:
        # Draw rectangle around the detected plate
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
        plate = image[y:y+h, x:x+w]
        cv2.imshow("License Plate", plate)

# Show the result
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.show()

