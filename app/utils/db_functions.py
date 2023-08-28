import psycopg2
from flask import current_app
from sqlalchemy import inspect
from app.extensions import db
from app.models.models import FilaMaestra, RegistroFila

def connection_db():
    db_name = current_app.config['DB_NAME']
    db_user = current_app.config['DB_USER']
    db_pass = current_app.config['DB_PASS']
    db_port = current_app.config['DB_PORT']
    db_host = current_app.config['DB_HOST']
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)
    return conn

def check_table_exists(table_name):
    inspector = inspect(db.engine)
    return inspector.has_table(table_name)

def check_open_elements(name_queue, conn):
    obj_fila_maestra = FilaMaestra.query.filter_by(nombre=name_queue).first()
    cursor = conn.cursor()
    query = f"SELECT prioridad, turno, id FROM registro_fila WHERE fecha_fin IS NULL AND fecha_atendido IS NULL AND fila_id = {obj_fila_maestra.id}"
    cursor.execute(query)
    rows_with_null = cursor.fetchall()
    return rows_with_null

def modify_element(id, column_to_modify, data):
    item = RegistroFila.query.filter_by(id=id).first() 
    if item:
        setattr(item, column_to_modify, data)
        db.session.commit()
    else:
        print("Item not found") 

def get_attend_elements():
    items = RegistroFila.query\
        .filter(RegistroFila.fecha_fin.is_(None))\
        .filter(RegistroFila.fecha_atendido.isnot(None))\
        .order_by(RegistroFila.fecha_atendido.desc())
    filtered_items = items.all()
    return filtered_items



        