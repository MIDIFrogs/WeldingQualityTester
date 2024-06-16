import drawBox
from PIL import Image
import numpy as np

path = input("Input project path: ")
labels = ["Adjacency", "Intergity", "Geometry", "Postprocessing", "Incompletion"]
while True:
    file = input("Input filename: ")
    lines = open(path + "\\" + file + ".txt").readlines()
    img = Image.open(path + "\\" + file + ".jpg")
    nparr = np.array(img)
    boxes = []
    for line in lines:
        cl, centerX, centerY, width, height = map(float, line.split())
        x1 = (centerX - width / 2) * img.width
        x2 = (centerX + width / 2) * img.width
        y1 = (centerY - height / 2) * img.height
        y2 = (centerY + height / 2) * img.height
        boxes.append([x1, y1, x2, y2, 1, cl])
    res = drawBox.plot_bboxes(nparr, boxes, labels, score=False)
    resImg = Image.fromarray(res)
    resImg.save(file, "JPEG")
