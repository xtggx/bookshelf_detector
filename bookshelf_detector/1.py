from ultralytics import YOLO

# Загрузка предобученной модели YOLOv8
model = YOLO('yolov8s.pt')  # Автоматически загрузит с GitHub