import json
from app.utils.db_functions import check_table_exists, check_open_elements
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

def create_queues_from_json(filename='/Users/rojanex/deveploment/rjxTurns/rjxTurns-back/app/utils/set_queues.json', conn=None):
    queues = []

    with open(filename, 'r') as file:
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