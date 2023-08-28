from flask import Blueprint, jsonify, request, current_app
from datetime import datetime
from app.models.models import RegistroFila, FilaMaestra
from app.extensions import db
from app.utils.db_functions import get_attend_elements

data_bp = Blueprint('data', __name__)

@data_bp.route('/attend_elements', methods=['GET'])
def attended_elements_view():
    elements = get_attend_elements()
    json_elements = []
    for e in elements:
        row = {
            'id': e.id,
            'turno': e.turno,
            'modulo':  e.modulo,
            'nombre': e.user
        }
        json_elements.append(row)
    return jsonify({'message': 'Got all elements',
                    'data': json_elements}), 200 
