from mongoengine import Document, ReferenceField, IntField, BooleanField

from src.utils.generator import generate_code
from .UserModel import find_user_by_id

class Invitation(Document):
    sender = ReferenceField('User')
    code = IntField(default=generate_code)
    is_active  = BooleanField(default=True)

    ammount = IntField(default=20)

    meta = {
        "db_alias": "core",
        "collection": "invitations"
    }

def use_invitation_code(code):
    iv = Invitation.objects.get(code=int(code), is_active=True)

    iv.is_active = False
    user = iv.sender
    print(user.name)
    user.eco_coins += iv.ammount
    user.save()
    iv.save()
    return iv

def create(sender_id):
    user = find_user_by_id(sender_id)

    iv = Invitation()
    iv.sender = user;

    iv.save()
    return iv



