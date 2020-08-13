import json

from app import db, scheduler
from app.db.models import Pdf, PdfLog
from app.utils.pdf import gen_random_password


def update_password():
    with scheduler.app.app_context():
        pdfs = Pdf.query.all()
        for pdf in pdfs:
            log = PdfLog()
            log.pdf_id = pdf.id
            log.action = "update"
            log.who = "local"
            log.old = json.dumps(pdf.to_dict())
            pdf.password = gen_random_password(6)
            log.new = json.dumps(pdf.to_dict())
            db.session().add(log)
        db.session().commit()
