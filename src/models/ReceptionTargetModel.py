from mongoengine import Document, StringField, ReferenceField,ListField
from mongoengine.queryset import QuerySet


class ReceptionTarget(Document):
    '''
    That class using to sorting Recycle Points
    (Утилизация, Благо, Переработка)

    Args:
        Document ([type]): [description]
    '''
    name = StringField(required=True)
    meta = {
        "db_alias": "core",
        "collection": "reception_targets"
    }


def read() -> QuerySet:
    """This is function return all Targets of receptions

    Returns:
        QuerySet: Set of ReceptionTarget Documents
    """

    recep_targets = ReceptionTarget.objects.all()
    return recep_targets


def create(name: str) -> ReceptionTarget:
    """This is functon thats creates Reception Targets

    Args:
        name (str): ReceptionTarget name

    Returns:
        ReceptionTarget: Created ReceptionTargets
    """
    recep_target = ReceptionTarget()
    recep_target.name = name
    recep_target.save()
    return recep_target


def update(_id: str, updates: object) -> ReceptionTarget:
    """This is function thats updates RecepionTarget

    Args:
        _id (str): - Filter id
        updates (object) - Updates
        updates.name (str): Filter new name


    Returns:
        ReceptionTarget: Updated ReceptionTarget
    """
    recep_target = ReceptionTarget.objects(id=_id).first()
    if not recep_target:
        return None
    recep_target.update(**updates)
    return recep_target

def delete(_id: str) -> ReceptionTarget:
    """This is function thats deletes ReceptionTarget

    Args:
        _id (str): ReceptionTarget id

    Returns:
        ReceptionTarget: Deleted ReceptionTarget
    """
    recep_target = ReceptionTarget.objects(id=_id).first()
    if not recep_target:
        return None
    recep_target.delete()
    return recep_target


def add_recpoint(_id: str ,rec_point: object):
    reception_target = ReceptionTarget.objects(id=_id).first()
    if not reception_target:
        return {"message": "Reception target not found id={}".format(_id)}, 404
    reception_target.rec_points.append(rec_point)
    reception_target.save()
    return reception_target


def find_by_id(_id:str)-> ReceptionTarget:
    rec_target = ReceptionTarget.objects(id=_id).first()
    if not rec_target:
        return None
    return rec_target