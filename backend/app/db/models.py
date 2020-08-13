import datetime

from app.db import db


class Common(object):
    def to_dict(self):
        """
        将查询的结果转化为字典类型
        获取其值剔除 "_sa_instance_state 即可。
        :return:
        """
        __dict = {}
        for k, v in self.__dict__.items():
            if k == "_sa_instance_state":
                continue
            else:
                if isinstance(v, datetime.datetime):
                    __dict[k] = "" if v is None else v.strftime(
                        '%Y-%m-%d %H:%M:%S')
                else:
                    __dict[k] = v
        return __dict


class Pdf(db.Model, Common):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256))
    password = db.Column(db.String(50))
    uuid = db.Column(db.String(50))
    url_prefix = db.Column(db.String(256))
    page_size = db.Column(db.INTEGER)
    format = db.Column(db.String(50), default="JPEG")
    open = db.Column(db.Boolean, default=True)


class PdfLog(db.Model, Common):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_at = db.Column('create_at', db.DateTime, default=datetime.datetime.now)
    action = db.Column(db.String(50))
    pdf_id = db.Column(db.INTEGER)
    old = db.Column(db.TEXT)
    new = db.Column(db.TEXT)
    who = db.Column(db.String(50))
