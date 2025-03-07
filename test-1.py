import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract

# Set the path for Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load the image
image = cv2.imread("images/Cars0.png")
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
        plate = image[y:y+h, x:x+w]  # Extract license plate **(still in BGR)**

        # **Fix: Convert the extracted plate to grayscale**
        plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)

        # Save the grayscale license plate image
        #cv2.imwrite("plate_gray.png", plate_gray)  # Saves as a file

        # Apply thresholding to improve OCR accuracy
        _, plate_thresh = cv2.threshold(plate_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Recognize text from the license plate
        plate_text = pytesseract.image_to_string(plate_thresh, config='--psm 8')
        print(f"Detected License Plate: {plate_text.strip()}")  # Print detected plate

        # Show extracted plate
        plt.figure(figsize=(4, 2))
        plt.imshow(plate_thresh, cmap="gray")
        plt.title("Extracted License Plate")
        plt.axis("off")
        plt.show()

# Show the final result with rectangles drawn
plt.figure(figsize=(10, 6))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title("Detected License Plate")
plt.axis("off")
plt.show()
