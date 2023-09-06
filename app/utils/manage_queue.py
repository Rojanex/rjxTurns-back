import json
from app.utils.db_functions import check_table_exists, check_open_elements
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime
import locale
class CustomQueue:
    def __init__(self, start_value, format_string, num_elements, elements_to_add=None):
        self.counter = int(start_value[1:])
        self.format_string = format_string
        self.num_elements = num_elements
        self.queue = []

        if elements_to_add is not None and len(elements_to_add) != 0:
            for element in elements_to_add:
                self.enqueue(element) 

        count_values = [item[1] for item in self.queue]
        if len(count_values) != 0:
            new_start_value = max(count_values)
            self.counter = int(new_start_value[1:]) + 1

    def get_next_value(self): 
        next_value = self.format_string.format(self.counter)
        self.counter += 1 
        if self.counter > self.num_elements: 
            self.counter = 1  # Reset the counter if it exceeds num_elements
        return next_value
    
    def enqueue(self, element):
        self.queue.append(element)

    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)
        return None 
    
    def get_elements(self):
        return self.queue

def create_queues_from_json(filename='/Users/rojanex/deveploment/rjxTurns/rjxTurns-back', conn=None):
    queues = []
    print(filename)
    with open(f"{filename}/app/utils/set_queues.json", 'r') as file:
        queue_data = json.load(file)
        for name_queue in queue_data.keys():
            start_value = queue_data.get(name_queue, {}).get("start_value",{})
            format_string = queue_data.get(name_queue, {}).get("format_string",{})
            num_elements = queue_data.get(name_queue, {}).get("num_elements",{})
            
            #Check if table exists and open elements
            if check_table_exists('registro_fila'):
                rows_with_null = check_open_elements(name_queue, conn)
            
            #Create queue class
            obj_queue = CustomQueue(start_value, format_string, num_elements, elements_to_add=rows_with_null)
            queues.append([name_queue, obj_queue])  

        

    return queues

def create_element(element, folder_path):
    img = Image.new('RGB', (800, 500), (255, 255, 255))

    # get a font
    fnt = ImageFont.truetype(f"{folder_path}/app/utils/assets/fonts/Retroica.ttf", 50)
    font2 = ImageFont.truetype(f"{folder_path}/app/utils/assets/fonts/OldSansBlack.ttf", 100)
    im2 = Image.open(f"{folder_path}/app/utils/assets/icons/logo-2-2.png")
    new_image = im2.resize((120, 90))
    #new_im2 = im2.convert('L')
    #get a drawing context
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