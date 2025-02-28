from ultralytics import YOLO

model = YOLO('yolo11x-cls.pt')

results = model.train(data='/home/bektemir/Desktop/office/AI/YOLO11/car_brand_dataset', epochs=20)