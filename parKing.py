import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract

# Set the path for Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load the image
image = cv2.imread("images/Cars6.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian Blur with a smaller kernel size
blurred = cv2.GaussianBlur(gray, (3, 3), 0)  # Smaller kernel to reduce streaks

# Edge detection using Canny with adjusted thresholds
edges = cv2.Canny(blurred, 100, 200)  # Adjusted thresholds for better edge detection

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Draw all contours for debugging
contour_image = image.copy()
cv2.drawContours(contour_image, contours, -1, (255, 0, 0), 2)
plt.figure(figsize=(10, 6))
plt.imshow(cv2.cvtColor(contour_image, cv2.COLOR_BGR2RGB))
plt.title("Detected Contours")
plt.axis("off")
plt.show()

# Loop through contours and filter potential license plates
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
    x, y, w, h = cv2.boundingRect(approx)

    # Adjust aspect ratio filter to be more flexible
    aspect_ratio = w / float(h)
    if 1.5 < aspect_ratio < 6.5 and w > 50 and h > 20:  # Ensure it's not too small
        # Draw rectangle around the detected plate
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
        plate = image[y:y+h, x:x+w]  # Extract license plate

        # Convert extracted plate to grayscale
        plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)

        # Apply adaptive thresholding to improve OCR accuracy
        plate_thresh = cv2.adaptiveThreshold(plate_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # Apply morphological operations to reduce noise (smaller kernel to reduce streaks)
        kernel = np.ones((2, 2), np.uint8)  # Smaller kernel to reduce artifacts
        plate_thresh = cv2.morphologyEx(plate_thresh, cv2.MORPH_CLOSE, kernel)

        # Recognize text from the license plate
        plate_text = pytesseract.image_to_string(plate_thresh, config='--psm 7 --oem 3')
        print(f"Detected License Plate: '{plate_text.strip()}'")

        # Show extracted plate
        plt.figure(figsize=(4, 2))
        plt.imshow(plate_thresh, cmap="gray")
        plt.title("Extracted License Plate")
        plt.axis("off")
        plt.show()

        # Check OCR confidence levels
        data = pytesseract.image_to_data(plate_thresh, output_type=pytesseract.Output.DICT)
        print("Detected Words:", data["text"])
        print("Confidence Levels:", data["conf"])

# Show the final result with rectangles drawn
plt.figure(figsize=(10, 6))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title("Detected License Plate")
plt.axis("off")
plt.show()
