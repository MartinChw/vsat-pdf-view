import json

from app.db import db
from app.db.models import Pdf, PdfLog


def open_and_close_db(func):
    def wrapper(*args, **kwargs):
        try:
            conn = db.session()
            result = func(conn=conn, *args, **kwargs)
            conn.commit()
            conn.close()
            return result
        except BaseException as e:
            conn.rollback()
            conn.close()
            raise Exception(str(e))

    return wrapper


@open_and_close_db
def create_pdf(pdf, conn):
    conn.add(pdf)
    conn.flush()
    log = PdfLog()
    log.pdf_id = pdf.id
    log.action = "create"
    log.who = "web"
    log.old = json.dumps(pdf.to_dict())
    log.new = json.dumps(pdf.to_dict())
    conn.add(log)


def has_pdf_by_title(title):
    return Pdf.query.filter(Pdf.title == title).first()


def list_pdf(page, limit):
    query = Pdf.query
    count = query.count()
    if limit != -1:
        query = query.limit(int(limit)).offset((page - 1) * limit)
    data = query.all()
    items = []
    if data:
        for item in data:
            items.append(item.to_dict())
    return items, count


def list_pdf_log(page, limit):
    query = PdfLog.query
    count = query.count()
    if limit != -1:
        query = query.limit(int(limit)).offset((page - 1) * limit)
    data = query.all()
    items = []
    if data:
        for item in data:
            items.append(item.to_dict())
    return items, count


def get_pdf(uuid):
    item = Pdf.query.filter(Pdf.uuid == uuid).first()
    if item is None:
        return None
    return item.to_dict()


def get_pdf_by_id(uuid, id):
    item = Pdf.query.filter(Pdf.uuid == uuid, Pdf.id != id).first()
    if item is None:
        return None
    return item.to_dict()


def update_pdf(update_dict):
    log = PdfLog()
    log.action = "update"
    log.who = "web"
    item = Pdf.query.filter(Pdf.id == update_dict['id']).first()
    log.pdf_id = item.id
    log.old = json.dumps(item.to_dict())
    if item is None:
        raise Exception("记录不存在")
    for key in update_dict:
        if key == 'id':
            continue
        setattr(item, key, update_dict[key])
    log.new = json.dumps(item.to_dict())
    db.session().add(log)
    db.session().commit()
    return item.to_dict()
