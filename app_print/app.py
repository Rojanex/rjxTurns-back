from flask import Flask, send_file
from PIL import Image, ImageFont, ImageDraw
import locale , datetime, base64, os
from dotenv import load_dotenv
from time import time, sleep
import socketio
# from geventwebsocket.handler import WebSocketHandler
# from gevent.pywsgi import WSGIServer

load_dotenv()

sio = socketio.Client()

server_socket = os.environ.get('SERVER_SOCKET')

def create_element(element, folder_path):
    img = Image.new('RGB', (800, 500), (255, 255, 255))

    # get a font
    fnt = ImageFont.truetype(f"{folder_path}/assets/fonts/Retroica.ttf", 50)
    font2 = ImageFont.truetype(f"{folder_path}/assets/fonts/OldSansBlack.ttf", 100)
    im2 = Image.open(f"{folder_path}/assets/icons/logo-2-2.png")
    new_image = im2.resize((120, 90))
    d = ImageDraw.Draw(img)

    # draw text, half opacity
    d.text((270, 200), "TU TURNO ES: ", font=fnt, fill=("black"))
    d.text((350, 270), element, font=font2, fill=("black"))
    img.paste(new_image, (250, 50))
    #time
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    now = datetime.now()
    fnt2 = ImageFont.truetype(f"{folder_path}/assets/fonts/OldSansBlack.ttf", 30)
    date_string = now.strftime("%a %d de %B")
    hour_string = now.strftime("%H:%M")
    d.text((400, 50), date_string, font=fnt2, fill=("black"))
    d.text((400, 80), hour_string, font=fnt2, fill=("black"))
    final = img.rotate(180)
    final.save(f"{folder_path}/assets/icons/label.png")


@sio.event
def connect():
    print("connected")



@sio.on('elementAdded')
def handle_elementAdded(data):
    folder_path = os.getcwd()
    create_element(element=data.addedElement, folder_path=folder_path)
    os.system(f"lp {folder_path}/assets/icons/label.png")
    print(data)

@sio.event
def disconnect():
    print("disconnect")


# sio.connect('http://'+server_socket+':5000')


connected = False
while not connected:
    try:
        sio.connect('http://'+ server_socket +':5000')
        sio.wait()
    except socketio.exceptions.ConnectionError as err:
        print("ConnectionError: Connection Refused")
        sleep(5)
    else:
        print("Connected!")
        connected = True

