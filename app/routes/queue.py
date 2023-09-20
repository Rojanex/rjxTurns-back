from flask import Blueprint, jsonify, request, current_app
from app.extensions import socketio
from datetime import datetime
from app.models.models import RegistroFila, FilaMaestra
from app.extensions import db
from app.utils.db_functions import modify_element
from app.utils.manage_queue import create_element
import re, os

queue_bp = Blueprint('queue', __name__)

@socketio.on('elementAdded')
@queue_bp.route('/add_element', methods=['GET'])
def add_element():
    queue_name = request.args.get('queue_name')
    priority = request.args.get('priority', 1)
    nombre = request.args.get('name')
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
    element_letter = re.sub("[^A-Z]", "", target_queue.format_string)
    c400_exists = any(elem[1] == f"{element_letter}{target_queue.num_elements}" for elem in target_queue.get_elements()) #por favor revisa esto y mejora
    priority2_exists = any(elem[0] == '2' for elem in target_queue.get_elements())
    if (c400_exists and priority != '0') or priority2_exists:
        priority = '2'  # Add with priority 2
    
    #Add element to database
    obj_fila_maestra = FilaMaestra.query.filter_by(nombre=name).first()
    if obj_fila_maestra:
        #Check num module
        add_element_db = RegistroFila(turno=element, fila_id=obj_fila_maestra.id, prioridad=priority, user=nombre, fecha_inicio=datetime.now())
        db.session.add(add_element_db)
        db.session.commit()
        #Socket message
        #socketio.emit('elementAdded', {'message': 'Element added to queue', 'addedElement': element})
    else:
        return jsonify({'message': 'Query params incorrect, verify queue'}), 404

    #Create element png for printing
    folder_root = current_app.config['folder_path']
    create_element(element, folder_root)    
    target_queue.enqueue((priority, element, add_element_db.id))  # Add with priority 1
    os.system(f"lp {folder_root}/utils/assets/icons/label.png") #print element
    
    elements = target_queue.get_elements()
    elements.sort(key=lambda x: (int(x[0] != '0'), int(x[0]), x[1]))
    
    print(elements) 
    return jsonify({'message': 'Element added to queue'}), 200



@socketio.on('element_removed')
@queue_bp.route('/call_element', methods=['GET'])
def remove_element():
    queue_name = request.args.get('queue_name')
    queues_info = current_app.config['queues_info']  # Access queues_info from the app context
    module = request.args.get('module', 0)
    total_modules = current_app.config['total_modules']

    target_queue = None
    for name, queue in queues_info:
        if name == queue_name:
            target_queue = queue
            break

    if target_queue is None:
        return jsonify({'message': 'Queue not found'}), 404 

    result = target_queue.dequeue() 
    if result:
        if module != 0 and int(module) in range(int(total_modules)+1):
            print(result)
            modify_element(id=result[2], column_to_modify='modulo', data=module)
            modify_element(id=result[2], column_to_modify='fecha_atendido', data=datetime.now())
            socketio.emit('element_removed', {'message': 'Element removed from queue', 'removedElement': result, 'modulo': module})
            return jsonify({'message': 'Element remove from queue'}), 200
        else:
            return jsonify({'message': 'Query params incorrect, verify queue'}), 404
    else:
        return jsonify({'message': 'No more elements to remove'}), 200


@queue_bp.route('/end_element', methods=['GET'])
def end_element():
    element = request.args.get('id_element')

    if element:
        modify_element(id=element, column_to_modify='fecha_fin', data=datetime.now())
        return jsonify({'message': 'Element end '}), 200
    else:
        return jsonify({'message': 'No element to end'}), 200
 