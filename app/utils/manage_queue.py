import json

class CustomQueue:
    def __init__(self, start_value, format_string, num_elements):
        self.counter = int(start_value[1:])
        self.format_string = format_string
        self.num_elements = num_elements
        self.queue = []

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

def create_queues_from_json(filename='/Users/rojanex/deveploment/rjxTurns/app/utils/set_queues.json'):
    queues = []

    with open(filename, 'r') as file:
        queue_data = json.load(file)
        for name_queue in queue_data.keys():
            start_value = queue_data.get(name_queue, {}).get("start_value",{})
            format_string = queue_data.get(name_queue, {}).get("format_string",{})
            num_elements = queue_data.get(name_queue, {}).get("num_elements",{})
            
            obj_queue = CustomQueue(start_value, format_string, num_elements)
            queues.append([name_queue, obj_queue])
            
            #object_queue = queue.Queue()
            #queues.append({name_queue, object_queue})
        

    return queues