import psycopg2, logging
from flask import current_app
from sqlalchemy import inspect, update, and_
from datetime import datetime
from app.extensions import db, logger
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
    try:
        fila_id = obj_fila_maestra.id
        cursor = conn.cursor()
        query = f"SELECT prioridad, turno, id FROM registro_fila WHERE fecha_fin IS NULL AND \
                    fecha_atendido IS NULL AND fila_id = {fila_id}"
        cursor.execute(query)
        rows_with_null = cursor.fetchall()
        return rows_with_null
    except AttributeError:
        logger.critical(f"'{name_queue}' does not exits in database, therefore NoneType has no attribute 'id'")
        return False
   
    


def check_unfinished_elements(conn):
    cursor = conn.cursor()
    registro_fila = RegistroFila.__table__
    query = "UPDATE registro_fila SET fecha_fin = %s WHERE fecha_fin IS NULL AND fecha_atendido IS NOT NULL"
    values = (datetime.now(),)
    cursor.execute(query, values)
    conn.commit()

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
    filtered_items = items.limit(6).all()
    return filtered_items

def get_all_queues():
    items = FilaMaestra.query.order_by()
    filtered_items = items.all()
    print(filtered_items)
    return filtered_items


def get_in_list_elements():
    items = RegistroFila.query\
        .filter(RegistroFila.fecha_fin.is_(None))\
        .filter(RegistroFila.fecha_atendido.is_(None))\
        .order_by(RegistroFila.fecha_inicio.asc())
    filtered_items = items.limit(6).all()
    return filtered_items



        