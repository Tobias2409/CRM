import cv2, face_recognition, time, os, threading, PIL, sys
import tkinter as tk
import numpy as np
import shutil
import struct
import uuid
from msilib.schema import Binary
from genericpath import exists
from asyncio.windows_events import NULL
from turtle import hideturtle, up, width
from mtcnn.mtcnn import MTCNN
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input, decode_predictions
from PIL import ImageTk, Image
from icrawler.builtin import GoogleImageCrawler
from os import walk
from os import path
import struct

def rawbytes(s):
    """Convert a string to raw bytes without encoding"""
    outlist = []
    for cp in s:
        num = ord(cp)
        if num < 255:
            outlist.append(struct.pack('B', num))
        elif num < 65535:
            outlist.append(struct.pack('>H', num))
        else:
            b = (num & 0xFF0000) >> 16
            H = num & 0xFFFF
            outlist.append(struct.pack('>bH', b, H))
    return b''.join(outlist)




def resize_image(image, scale):
    width, height = image.size

    if height < width:
        width = int(500 * (width/height))
        height = 500
    else:
        height = int (500 * (height/width))
        width = 500

    image = image.resize((width,height),Image.ANTIALIAS)
    
    #image = np.asarray(image)
    
    #crop =  []
    #for x in range(wOffset,500 + wOffset):
    #    crop.append([])
    #    for y in range(hOffset,500 + hOffset):
    #        crop[x-wOffset].append(image[x-wOffset][y])

    #image = Image.fromarray(np.asarray(crop))
    
    return image

def download_image(name):
    uuidOne = uuid.uuid1()
    google_Crawler = GoogleImageCrawler(storage = {'root_dir': r'./download/' + str(uuidOne) + '/'})
    google_Crawler.crawl(keyword = name.replace("_", " ") + ' Portrait', max_num = 1)
    filenames = next(walk('./download/' + str(uuidOne) + '/'), (None, None, []))[2] 
    shutil.move('./download/' + str(uuidOne) + '/'+filenames[0], "./img/"+name)

loading = Image.open("Loading.jpg")
loading = resize_image(loading,500)

def getImage(name):
    if not path.exists("./img/"+name):
        thread = threading.Thread(target=download_image, args=(name,))
        thread.daemon = True
        thread.start()
        return loading

    return resize_image(Image.open("./img/"+name),500)


SIZE = 4
MARGIN_HOR = 60
MARGIN_VER = 80
IMAGE_SIZE = 448

detector = MTCNN()
model = VGGFace(model= 'resnet50')

window = tk.Tk()
window.minsize(1000,550)
window.title("Celeb Dedection")
window.config(bg="white")

youText = tk.Label(window, text="You",font=("Arial", 23))
youText.pack(ipadx=10, ipady=10)
youText.place(x=2,y=10)
youText.config(bg="white")

actorText = tk.Label(window, text="",font=("Arial", 23))
actorText.pack(ipadx=10, ipady=10)
actorText.place(x=502,y=10)
actorText.config(bg="white")

vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
imageLabel = tk.Label()
imageLabel.place(x=0,y=50)
actorLabel = tk.Label()
actorLabel.place(x=500,y=50)
noFace = Image.open("NoFaceDetected.jpg")
noFace = resize_image(noFace, 500)
noFace = ImageTk.PhotoImage(noFace)
image = noFace

white = Image.open("White.jpg")
white = resize_image(white, 500)
white = ImageTk.PhotoImage(white)


run = True
def updateImage():
    while(run):
        ret, frame = vid.read()
        blue,green,red = cv2.split(frame)
        frame = cv2.merge((red,green,blue)) 
        image = Image.fromarray(frame)
        image = resize_image(image, 0)
        image = ImageTk.PhotoImage(image)      

        face_locations = face_recognition.face_locations(frame) 
        celeb_info = ""
        for (top, right, bottom, left) in face_locations:
            face = frame[top-MARGIN_VER:bottom+MARGIN_VER, left-MARGIN_HOR:right+MARGIN_HOR]
            if (face.size > 0):
                results = decode_predictions(model.predict(preprocess_input(np.expand_dims(np.asarray(PIL.Image.fromarray(face).resize((224, 224))).astype('float32'), axis = 0), version = 2)))
                nameB =results[0][0][0]
                print(results[0])
                nameB = rawbytes(nameB).decode("utf-8")
                print(nameB)
                celeb_info = f"{results[0][0][0]} [{results[0][0][1]*100}]"
                print(celeb_info)
                image = ImageTk.PhotoImage(Image.fromarray(face).resize((500,500),Image.BOX))

        actor = NULL

        if len(celeb_info) == 0:
            image = noFace
            actorLabel.configure(image=white)
            actorLabel.image = white
            actorText.configure(text="") 
        else:
            celeb_name = celeb_info.split("'")[1].strip()
            actor = getImage(celeb_name)
            actor = ImageTk.PhotoImage(actor)
            actorLabel.configure(image=actor)
            actorLabel.image = actor
            actorText.configure(text=celeb_name.replace("_", " ")) 
            

        

        imageLabel.configure(image=image)
        imageLabel.image = image  
                    
        



thread = threading.Thread(target=updateImage)
thread.daemon = True
thread.start()


window.mainloop()


print("END")
sys.exit()