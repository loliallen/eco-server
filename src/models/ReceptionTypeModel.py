from mongoengine import Document, StringField, ReferenceField,ListField
from mongoengine.queryset import QuerySet


class ReceptionType(Document):
    '''
    That class using to sorting Recycle Points
    (Платные прием, Бесплатныей, Круглосуточно, Пункты партнеры)

    Args:
        Document ([type]): [description]
    '''
    name = StringField(required=True)
    meta = {
        "db_alias": "core",
        "collection": "reception_type"
    }


def read() -> QuerySet:
    """This is function return all Types of receptions

    Returns:
        QuerySet: Set of ReceptionType Documents
    """

    recep_types = ReceptionType.objects.all()

    return recep_types


def create(name: str) -> ReceptionType:
    """This is functon thats creates Reception Types

    Args:
        name (str): ReceptionType name

    Returns:
        ReceptionType: Created ReceptionType
    """
    recep_type = ReceptionType()

    recep_type.name = name

    recep_type.save()

    return recep_type


def update(_id: str, updates: object) -> ReceptionType:
    """This is function thats updates RecepionType

    Args:
        _id (str): - ReceptionType id
        updates (object) - Updates
        updates.name (str): ReceptionType new name


    Returns:
        ReceptionType: Updated ReceptionType
    """
    recep_type = ReceptionType.objects(id=_id).first()

    if not recep_type:
        return None

    recep_type.update(**updates)

    return recep_type

def delete(_id: str) -> ReceptionType:
    """This is function thats deletes ReceptionType

    Args:
        _id (str): ReceptionType id

    Returns:
        ReceptionType: Deleted ReceptionType
    """
    recep_type = ReceptionType.objects(id=_id).first()

    if not recep_type:
        return None

    recep_type.delete()

    return recep_type

def add_recpoint(_id: str ,rec_point: object):
    reception_type = ReceptionType.objects(id=_id).first()

    if not reception_type:
        return {"message": "Reception target not found id={}".format(_id)}, 404

    reception_type.rec_points.append(rec_point)

    reception_type.save()

    return reception_type

def find_by_id(_id:str)-> ReceptionType:

    rec_type = ReceptionType.objects(id=_id).first()

    if not rec_type:
        return None

    return rec_type