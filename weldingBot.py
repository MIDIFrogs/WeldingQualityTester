import telebot
from PIL import Image
import io
import os
import yaml
import drawBox
import numpy as np
from ultralytics import YOLO

# YOLO
model  = YOLO('model.pt')

# Resources
config = {}
if (os.path.exists("startup.config")):
    with open("startup.config") as configFile:
        keys = configFile.readlines()
        for line in keys:
            key, value = map(lambda x: x.trim(), line.split("="))
            config[key] = value

localization = yaml.load(open(f'Resources/Localization/{config.get("Locale", "ru")}.yaml', encoding="UTF-8"), Loader=yaml.CFullLoader)
classNames = localization["LabelsInvariant"]
classNamesRu = localization["LabelsLocalized"]

# Image processing
def proccesImage(nparr):
    '''Performs image processing using loaded YOLO model
    
    Args:
        'nparr': Image in format of NumPy array
    
    Returns:
        List of processing results. Each result is a dictionary with following keys:
            'hitbox': List with X, Y, Width and Height of the processed image
            'class': Image class index
            'confidence': Confidence of the box detection
    '''
    results = model.predict(nparr)
    for result in results:
        boxes = result.boxes
        records = []
        for box in boxes:
            x, y, w, h = map(int, (box.xywh)[0])
            records.append({
                'hitbox': [x,y,w,h],
                'class': int(box.cls[0]),
                'confidence': float((box.conf)[0])
            })
    return records

# Bot helper functions

def createAnswer(records):
    '''Builds answer message with defects data
    
    Args:
        'records': list with results of the 'processImage' function
    
    Returns:
        String with results message.
    '''
    if len(records) == 0:
        msg = localization['DefectsNotFound']
    else:
       msg = localization['DefectsFound'] % (len(records))
       classes = [0] * 5
       for k in records:
           classes[k['class']] += 1
       for j in range(len(classes)):
           if classes[j] != 0:
               msg += '\n' + classNamesRu[j] + ':' + str(classes[j])
    return msg

def createBoxedPhoto(image, records):
  return drawBox.plot_bboxes(image, [k['hitbox'] + [k['confidence'], k['class']] for k in records], labels=classNames, colors=[], score=True, conf=None)

# Bot section

TOKEN = open("Resources/token.dat").readline()
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    '''Answers on bot '/start' command
    '''
    sticker = open('Resources/hi.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.chat.id, localization["HelloMessage"])

@bot.message_handler(content_types=['photo'])
def OnPhotoRecieve(message):
    '''Handles photo request from user.

    Args:
        'message': Telegram message with image for the bot. 
    '''
    bot.send_message(message.chat.id, 'чудик обработал')
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image = Image.open(io.BytesIO(downloaded_file))
    nparr = np.array(image)
    records = proccesImage(nparr)
    text = createAnswer(records)
    bot.send_message(message.chat.id, text)
    if len(records) != 0:
        image = createBoxedPhoto(nparr, records)
        image = Image.fromarray(image)
        bytes = io.BytesIO()
        bytes.name = 'image.jpeg'
        image.save(bytes, format="JPEG")
        bytes.seek(0)
        bot.send_photo(message.chat.id, photo=bytes)

@bot.message_handler(content_types=['text', 'sticker', 'video' 'voice'])
def OnWrongContentType(message):
    '''Handles any wrong data types receiving.

    Args:
        'message': Telegram message with any content instead of photos.
    '''
    sticker = open('Resources/wrong.webp', 'rb')
    bot.send_message(message.chat.id, localization["WrongTypeMessage"])
    bot.send_sticker(message.chat.id, sticker)

# Startup the bot
bot.polling(none_stop = True)
