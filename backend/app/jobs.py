from app import db, scheduler
from app.db.models import Pdf
from app.utils.pdf import gen_random_password


def update_password():
    with scheduler.app.app_context():
        pdfs = Pdf.query.all()
        for pdf in pdfs:
            pdf.password = gen_random_password(6)
        db.session().commit()