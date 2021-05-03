import uuid

from mongoengine import BooleanField, UUIDField


class Atomic:

    in_freeze = BooleanField(default=False)
    freeze_by = UUIDField()

    def lock(self):
        class Context:
            def __init__(self, _id, atomic_model):
                self._id = _id
                self.atomic_model = atomic_model

            def __enter__(self):
                _uuid = uuid.uuid4()
                self.atomic_model.objects.filter(id=self._id, in_freeze=False).update(freeze_by=_uuid, in_freeze=True)
                obj = self.atomic_model.find_by_id_(self._id)
                if obj.freeze_by != _uuid:
                    raise Exception('user is freeze')
                return obj

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.atomic_model.find_by_id_(self._id).update(in_freeze=False)
        return Context(self.id, type(self))
