from ultralytics import YOLO
import os

path = input("Input dataset path: ").replace('"', "")
jpgFiles = [file for file in os.listdir(path) if file.endswith(".jpg")]

yolo = YOLO("model.pt")

out = open("submission.csv", "w")
i = 0
for file in jpgFiles:
    i += 1
    if i % 10 == 0:
        print(f"Processing image {i}...")
    imagePath = path + "\\" + file
    results = yolo.predict(imagePath)
    for result in results:
        for box in result.boxes:
            classIndex = int(box.cls[0])
            x, y, w, h = map(int, box.xywh[0])
            height, width = result.orig_shape
            out.write(f"{file};{classIndex};{(x + w / 2) / width};{(y + h  / 2) / height};{w / width};{h / height}\n")
out.close()
