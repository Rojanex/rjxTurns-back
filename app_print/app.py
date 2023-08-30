from flask import Flask, send_file
from flask_socketio import SocketIO, emit
from PIL import Image, ImageFont, ImageDraw
import io
import locale , datetime

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def create_element(element, folder_path):
    img = Image.new('RGB', (800, 500), (255, 255, 255))

    # get a font
    fnt = ImageFont.truetype(f"{folder_path}/app/utils/assets/fonts/Retroica.ttf", 50)
    font2 = ImageFont.truetype(f"{folder_path}/app/utils/assets/fonts/OldSansBlack.ttf", 100)
    im2 = Image.open(f"{folder_path}/app/utils/assets/icons/logo-2-2.png")
    new_image = im2.resize((120, 90))
    d = ImageDraw.Draw(img)

    # draw text, half opacity
    d.text((270, 200), "TU TURNO ES: ", font=fnt, fill=("black"))
    d.text((350, 270), element, font=font2, fill=("black"))
    img.paste(new_image, (250, 50))
    #time
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    now = datetime.now()
    fnt2 = ImageFont.truetype(f"{folder_path}/app/utils/assets/fonts/OldSansBlack.ttf", 30)
    date_string = now.strftime("%a %d de %B")
    hour_string = now.strftime("%H:%M")
    d.text((400, 50), date_string, font=fnt2, fill=("black"))
    d.text((400, 80), hour_string, font=fnt2, fill=("black"))
    final = img.rotate(180)
    final.save(f"{folder_path}/app/utils/assets/icons/label.png")


@socketio.on('image')
def handle_image(data):
    # Assuming data is base64 encoded image
    image = Image.open(io.BytesIO(base64.b64decode(data)))
    image.save('received_image.png')
    print('Image saved')

@app.route('/')
def index():
    return send_file('received_image.png', mimetype='image/png')

if __name__ == '__main__':
    socketio.run(app)