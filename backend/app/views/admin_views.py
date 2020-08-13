import json
import os

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.utils import secure_filename
from app.db.models import Pdf
from app.db.dao import create_pdf, list_pdf, get_pdf, update_pdf, get_pdf_by_id
from app.db.dao import has_pdf_by_title
from app.utils.common import args_strip
from app.utils.pdf import upload_image_to_aliyun, gen_random_word, gen_random_password

ns = Blueprint('admin api', __name__, url_prefix="/api/v1")


@ns.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    if not username:
        return {"code": 0, "msg": "Missing username parameter"}, 400
    if not password:
        return {"msg": "Missing password parameter"}, 400

    if username != 'admin' or password != 'admin':
        return {"msg": "Bad username or password"}, 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return {
        "code": 0,
        "msg": "success",
        "data": {
            "access_token": access_token
        }
    }, 200


ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@ns.route('/pdf', methods=['POST'])
@jwt_required
def handlerCreatePdf():
    if 'title' not in request.form:
        return {"code": 10001, "msg": "缺少title参数"}, 200
    title = request.form.get('title')
    if title.strip() == '':
        return {"code": 10001, "msg": "title不能为空"}, 200
    if has_pdf_by_title(title) is not None:
        return {"code": 10001, "msg": "title 已存在"}, 200
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(os.getcwd(), 'uploads', filename)
            file.save(filepath)
            url_prefix, page_size = upload_image_to_aliyun(title, filepath)
            pdf = Pdf(
                title=title,
                password=gen_random_password(6),
                uuid=gen_random_word(8),
                url_prefix=url_prefix,
                page_size=page_size,
            )
            create_pdf(pdf)
            return {"code": 0, "msg": "success"}, 200
        else:
            return {"code": 10002, "msg": "文件为空或类型不支持"}, 200
    else:
        try:
            args = args_strip(request.form,
                              ['url_prefix', 'page_size', 'uuid'])
        except Exception as e:
            return {"code": 10002, "msg": str(e)}, 200
        url_prefix = args['url_prefix']
        page_size = args['page_size']
        uuid = args['uuid']

        pdf = Pdf(
            title=title,
            password=gen_random_password(6),
            uuid=uuid,
            url_prefix=url_prefix,
            page_size=page_size,
        )
        create_pdf(pdf)
        return {"code": 0, "msg": "success"}, 200


@ns.route('/pdf', methods=['GET'])
@jwt_required
def handlerListPdf():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    items, count = list_pdf(page, limit)
    data = {"items": items, "count": count}
    return {"code": 0, "data": data}, 200


@ns.route('/pdf/item', methods=['GET'])
def handlerGetPdf():
    uuid = request.args.get('uuid', None)
    if uuid is None:
        return {"code": 10001, "msg": "无效的uuid"}, 200
    data = get_pdf(uuid)
    if data is None:
        return {"code": 10001, "msg": "未找到文件"}, 200
    return {"code": 0, "data": data}, 200


@ns.route('/pdf/item', methods=['PUT'])
def handlerUpdatePdf():
    args = json.loads(request.data)
    id = args.get('id', None)
    if id is None:
        return {"code": 10001, "msg": "无效的id"}, 200
    uuid = args.get('uuid', None)
    if uuid is None or uuid.strip() == '':
        return {"code": 10001, "msg": "无效的uuid"}, 200
    password = args.get('password', None)
    if password is None or password.strip() == '':
        return {"code": 10001, "msg": "无效的password"}, 200
    url_prefix = args.get('url_prefix', None)
    if url_prefix is None or url_prefix.strip() == '':
        return {"code": 10001, "msg": "无效的url_prefix"}, 200
    title = args.get('title', None)
    if title is None or title.strip() == '':
        return {"code": 10001, "msg": "无效的title"}, 200
    page_size = args.get('page_size', None)
    if page_size is None:
        return {"code": 10001, "msg": "无效的page_size"}, 200
    data = get_pdf_by_id(uuid, id)
    if data is not None:
        return {"code": 10001, "msg": "uuid已存在，请更换新的uuid"}, 200
    try:
        update_pdf(args)
    except Exception as e:
        return {"code": 10001, "msg": str(e)}, 200
    return {"code": 0, "data": data}, 200
