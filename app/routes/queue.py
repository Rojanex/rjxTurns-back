import queue
import json
from flask import Blueprint, jsonify, request, current_app
from app.utils.manage_queue import CustomQueue, create_queues_from_json


queue_bp = Blueprint('queue', __name__)

@queue_bp.route('/add_element', methods=['GET'])
def add_element():
    queue_name = request.args.get('queue_name')
    priority = request.args.get('priority', 1)
    queues_info = current_app.config['queues_info']  # Access queues_info from the app context
    target_queue = None
    for name, queue in queues_info:
        if name == queue_name:
            target_queue = queue
            break

    if target_queue is None:
        return jsonify({'message': 'Queue not found'}), 404

    element = target_queue.get_next_value()
     # Check if 'C400' exists in the list of elements
    c400_exists = any(elem[1] == 'C400' for elem in target_queue.get_elements())
    priority2_exists = any(elem[0] == '2' for elem in target_queue.get_elements())
    if (c400_exists and priority != '0') or priority2_exists:
        target_queue.enqueue(('2', element))  # Add with priority -1
    else:
        target_queue.enqueue((priority, element))  # Add with priority 1
    

    elements = target_queue.get_elements()
    elements.sort(key=lambda x: (int(x[0] != '0'), int(x[0]), x[1]))
    
    print(elements) 
    return jsonify({'message': 'Element added to queue'}), 200


@queue_bp.route('/remove_element', methods=['GET'])
def remove_element():
    queue_name = request.args.get('queue_name')
    queues_info = current_app.config['queues_info']  # Access queues_info from the app context

    target_queue = None
    for name, queue in queues_info:
        if name == queue_name:
            target_queue = queue
            break

    if target_queue is None:
        return jsonify({'message': 'Queue not found'}), 404

    result = target_queue.dequeue()
    print(result)
    return jsonify({'message': 'Element remove from queue'}), 200

