from ultralytics import YOLO
import os
from pathlib import Path

def ProcessCsv():
    path = input("Input dataset path: ").replace('"', "")
    jpgFiles = [file for file in os.listdir(path) if file.endswith(".jpg")]

    yolo = YOLO("model.pt")

    if (not os.path.exists("./out/")):
        os.makedirs("./out/")
    out = open("out/submission.csv", "w")
    out.write("filename;class_id;rel_x;rel_y;width;height\n")
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
                out.write(f"{file};{classIndex};{x / width};{y / height};{w / width};{h / height}\n")
    out.close()

if __name__ == "__main__":
    ProcessCsv()