from app.db import db
from app.db.models import Pdf


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
    return items,count


def get_pdf(uuid):
    item = Pdf.query.filter(Pdf.uuid == uuid).first()
    if item is None:
        return None
    return item.to_dict()
