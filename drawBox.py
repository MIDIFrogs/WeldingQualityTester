import cv2
#from google.colab.patches import cv2_imshow

def box_label(image, box, label='', color=(128, 128, 128), txt_color=(255, 255, 255)):
  '''Adds a label to the provided box.

  Args:
    'image' (NumPy array): An image to outline with the box.
    'box' (list): Info about the hitbox in format [x1, y1, x2, y2, confidence, class].
    'color' (tuple(int, int, int)): Color of the outline
    'txt_color' (tuple(int, int, int)): Color of the label
  '''
  lw = max(round(sum(image.shape) / 2 * 0.003), 2)
  p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
  cv2.rectangle(image, p1, p2, color, lw, cv2.LINE_AA)
  if label:
    tf = max(lw - 1, 1)  # font thickness
    w, h = cv2.getTextSize(label, 0, fontScale=lw / 3, thickness=tf)[0]  # text width, height
    outside = p1[1] - h >= 3
    p2 = p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3
    cv2.rectangle(image, p1, p2, color, -1, cv2.LINE_AA)  # filled
    cv2.putText(image,
                label, (p1[0], p1[1] - 2 if outside else p1[1] + h + 2),
                0,
                lw / 3,
                txt_color,
                thickness=tf,
                lineType=cv2.LINE_AA)
    
def plot_bboxes(image, boxes, labels=[], colors=[], score=True, conf=None):
  '''Adds labels to all the boxes in the list.
  
  Args:
    'image' (NumPy array): An image to process.
    'boxes' (list): List of the boxes definition in format [x1, y1, x2, y2, confidence, class].
    'labels' (list): List of the label names according to class indices.
    'colors' (list): List of the box colors to outline different classes with different colors.
    'score' (bool): Indicates whether to score confidence in percent.
    'conf' (bool): Indicates whether to print confidence on labels.
  '''
  #Define Labels
  if labels == []:
    labels = {0: u'adj', 1: u'int', 2: u'geo',3: u'pro', 4: u'non'}
  #Define colors
  if colors == []:
    colors = [(89, 161, 197),(67, 161, 255),(19, 222, 24),(186, 55, 2),(167, 146, 11)]
  
  #plot each boxes
  for box in boxes:
    #add score in label if score=True
    if score :
      label = labels[int(box[-1])] + " " + str(round(100 * float(box[-2]),1)) + "%"
    else :
      label = labels[int(box[-1])]
    #filter every box under conf threshold if conf threshold setted
    if conf :
      if box[-2] > conf:
        color = colors[int(box[-1])]
        box_label(image, box, label, color)
    else:
      color = colors[int(box[-1])]
      box_label(image, box, label, color)

  return image

#path=r'1.jpg'
#image=cv2.imread(path) 

