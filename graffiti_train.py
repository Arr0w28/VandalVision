from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')  # 'n' stands for the nano model; you can choose 's', 'm', 'l', or 'x' for larger models

# Train the model
# model.train(
#     data='/Users/kaytee/Documents/BroCodes/VandalismDetection/data.yaml',  # Path to your data.yaml file
#     epochs=100,
#     imgsz=640,
#     batch=16,
#     name='graffiti_detector'
# )

# Evaluate the model on the validation set
metrics = model.val()
print("Validation metrics:", metrics)

# Optional: Test the model on the test set using predict
results = model.predict(source='/Users/kaytee/Documents/BroCodes/VandalismDetection/test/images', conf=0.5)
print("Prediction results:", results)

# Save the model weights
model.export(format='onnx')  # You can choose 'torchscript', 'tflite', 'coreml' if needed
