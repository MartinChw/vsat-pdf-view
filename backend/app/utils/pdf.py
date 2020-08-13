from urllib import parse

from pdf2image import convert_from_path
import tempfile
import oss2
import os
import random
import shutil

from config import KEY, SECRET


def gen_random_word(num):
    seed = "abcdefghijklmnopqrstuvwxyz"
    sa = []
    for i in range(num):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt


def gen_random_password(num):
    seed = "1234567890abcdefghijklmnopqrstuvwxyz"
    sa = []
    for i in range(num):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt


def upload_image_to_aliyun(title, pdf_path):
    path = tempfile.mkdtemp(dir=os.getcwd())
    convert_from_path(pdf_path, fmt="JPEG", output_folder=path, thread_count=1)
    url_prefix = parse.quote(title) + '/'
    for index, jpg in enumerate(os.listdir(path)):
        jpg_index = jpg[-6:-4]
        os.rename(os.path.join(path, jpg),
                  os.path.join(path,
                               str(int(jpg_index)) + '.jpg'))
        auth = oss2.Auth(KEY,
                         SECRET)
        headers = {}
        headers["x-oss-forbid-overwrite"] = "true"
        bucket = oss2.Bucket(auth, 'http://oss-cn-shanghai.aliyuncs.com',
                             'vsat-pdf')
        objectName = title + "/" + str(int(jpg_index)) + '.jpg'
        bucket.put_object_from_file(objectName,
                                    os.path.join(path,
                                                 str(int(jpg_index)) + '.jpg'),
                                    headers=headers)
    num = len(os.listdir(path))
    shutil.rmtree(path)
    return "https://vsat-pdf.oss-cn-shanghai.aliyuncs.com/" + url_prefix, num
