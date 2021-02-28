import qrcode
from PIL import Image
from src.config import Configuration
from uuid import uuid1
from pathlib import Path

REL_PATH = "/statics/users"
files_storage = Path('./src'+REL_PATH)

def create_qr_code(plain_text):
    filename = "{}.png".format(str(uuid1()))
    dest = files_storage / filename
    img = qrcode.make(plain_text)
    dest = dest.resolve()
    img.save(dest)
    return REL_PATH +"/"+ filename

