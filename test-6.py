import cv2
import easyocr

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Load image (or replace with video frame in a loop)
image = cv2.imread('openalpr_64/samples/us-4.jpg')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use OpenCV's built-in Haar cascade for license plate detection
plate_cascade = cv2.CascadeClassifier('openalpr_64/runtime_data/region/us.xml')


# Detect license plates
plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

for (x, y, w, h) in plates:
    # Draw rectangle around detected plate
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Crop the detected plate
    plate_img = image[y:y + h, x:x + w]

    # OCR the cropped plate image
    result = reader.readtext(plate_img)

    # Show results
    for (_, text, prob) in result:
        print("Detected Plate Number:", text)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (36,255,12), 2)

# Display result
cv2.imshow("License Plate Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(text)
