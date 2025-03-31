import easyocr
import cv2

# Create EasyOCR reader
reader = easyocr.Reader(['en'])  # 'en' = English

# Load image
image_path = 'assets/car-0.jpg'
image = cv2.imread(image_path)

# Run OCR
results = reader.readtext(image)

# Loop through results
for (bbox, text, confidence) in results:
    print(f"Detected Text: {text} (Confidence: {confidence:.2f})")

    # Draw bounding box
    (top_left, top_right, bottom_right, bottom_left) = bbox
    top_left = tuple(map(int, top_left))
    bottom_right = tuple(map(int, bottom_right))

    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
    cv2.putText(image, text, (top_left[0], top_left[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

# Show result
cv2.imshow("EasyOCR Result", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
