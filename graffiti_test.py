import cv2
import os
from ultralytics import YOLO

# Load your trained model
# model = YOLO('/Users/kaytee/Documents/BroCodes/VandalismDetection/runs/detect/detector 04-23-13-399/weights/best.pt')  # Replace with the path to your trained model, for graffiti
model = YOLO('/Users/kaytee/Documents/BroCodes/VandalismDetection/runs/detect/graffiti_detector3/weights/best.pt')  # Replace with the path to your trained model, for spitting

# Initialize video capture
cap = cv2.VideoCapture(0)

# Create a directory to save screenshots
output_dir = '/Users/kaytee/Documents/BroCodes/VandalismDetection/screenshots'
os.makedirs(output_dir, exist_ok=True)

# Initialize a counter for naming the screenshots
screenshot_counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform object detection
    results = model.predict(rgb_frame, conf=0.5)

    # Initialize a flag to check if any bounding box is detected
    detected = False

    # Start with the original frame
    annotated_frame = frame.copy()

    for result in results:
        if result.boxes:  # Check if bounding boxes are present
            detected = True
            # Draw annotations on the frame
            annotated_frame = result.plot()
            annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)

    cv2.imshow('Graffiti Detection', annotated_frame)

    # If bounding boxes are detected, save the frame
    if detected:
        screenshot_filename = os.path.join(output_dir, f'screenshot_{screenshot_counter}.jpg')
        cv2.imwrite(screenshot_filename, annotated_frame)
        screenshot_counter += 1
        print(f"Saved screenshot: {screenshot_filename}")

    # Break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
