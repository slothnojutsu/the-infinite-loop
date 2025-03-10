import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract

# Set the path for Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image = cv2.imread("images/Cars6.png")            # Loads the image for folder
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    #Converts the image to grayscale

# Smooths the image to remove noise using a small Gaussian blur
blurred = cv2.GaussianBlur(gray, (3, 3), 0)      # Smaller kernel to reduce streaks

# Finds the edges in the image using the Canny edge detector
edges = cv2.Canny(blurred, 100, 200)

# Finds all the shapes (contours) in the edge image
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Draws all contours on a copy of the original image (blue lines)
contour_image = image.copy()
cv2.drawContours(contour_image, contours, -1, (255, 0, 0), 2)

# Displays the image with all detected contours
plt.figure(figsize=(10, 6))
plt.imshow(cv2.cvtColor(contour_image, cv2.COLOR_BGR2RGB))
plt.title("Detected Contours")
plt.axis("off")
plt.show()

# Loop through contours and filter potential license plates
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)        # Makes each contour shape smoother using polygon approximation
    x, y, w, h = cv2.boundingRect(approx)        # Gets the rectangle area (x, y, width, height) around the contour

    # Filters out rectangles that look like license plates (wide shape, not too small).
    aspect_ratio = w / float(h)
    if 1.5 < aspect_ratio < 6.5 and w > 50 and h > 20:  # Ensure it's not too small
        # Draw rectangle around the detected plate
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
        # Cuts out the license plate from the image
        plate = image[y:y+h, x:x+w]

        # Converts the plate image to grayscale
        plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)

        # Makes the text clearer using adaptive thresholding to improve OCR accuracy
        plate_thresh = cv2.adaptiveThreshold(plate_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # Removes small noise using a morphological filter (close gaps in letters)
        kernel = np.ones((2, 2), np.uint8)  # Smaller kernel to reduce artifacts
        plate_thresh = cv2.morphologyEx(plate_thresh, cv2.MORPH_CLOSE, kernel)

        # Uses Tesseract OCR to read text from the license plate image and prints it
        plate_text = pytesseract.image_to_string(plate_thresh, config='--psm 7 --oem 3')
        print(f"Detected License Plate: '{plate_text.strip()}'")

        # Shows the processed image of the license plate
        plt.figure(figsize=(4, 2))
        plt.imshow(plate_thresh, cmap="gray")
        plt.title("Extracted License Plate")
        plt.axis("off")
        plt.show()

        # Shows what words were detected and how confident the OCR was
        data = pytesseract.image_to_data(plate_thresh, output_type=pytesseract.Output.DICT)
        print("Detected Words:", data["text"])
        print("Confidence Levels:", data["conf"])

# Show the final result with rectangles drawn
plt.figure(figsize=(10, 6))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title("Detected License Plate")
plt.axis("off")
plt.show()
