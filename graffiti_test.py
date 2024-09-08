import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('/Users/kaytee/Documents/BroCodes/VandalismDetection/runs/detect/graffiti_detector2/weights/best.pt')  # Replace with the path to your trained model

# Initialize the webcam
cap = cv2.VideoCapture(0)  # 0 is the default webcam; change if necessary

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert frame to RGB (YOLOv8 expects RGB images)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform inference
    results = model.predict(rgb_frame, conf=0.5)

    # Handle results
    for result in results:
        # Filter detections to only include "graffiti"
        annotated_frame = result.plot()  # Plot results on the image

        # Convert back to BGR for display with OpenCV
        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)

        # Display the frame with detections
        cv2.imshow('Graffiti Detection', annotated_frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
