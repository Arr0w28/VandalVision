from ultralytics import YOLO
import torch

# Check if MPS (Apple Silicon GPU) is available and set the device
device = 'mps' if torch.backends.mps.is_available() else 'cpu'

# Load the YOLOv8 model
model = YOLO('yolov8m.pt')

# Train the model using the MPS (GPU)
model.train(
    data='/Users/kaytee/Documents/BroCodes/VandalismDetection/Combined Dataset -Spitting - Graffiti-/data.yaml',  # Path to your data.yaml file
    epochs=10,
    imgsz=640,
    batch=16,
    name='detect',
    device=device  # Use the MPS device
)

# Optional: Export the trained model to ONNX format
model.export(format='onnx')
