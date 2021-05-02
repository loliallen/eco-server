import uuid

from mongoengine import BooleanField, UUIDField


class Atomic:
    atomic_model = None

    in_freeze = BooleanField(default=False)
    freeze_by = UUIDField()

    def lock(self):
        class Context:
            def __init__(self, _id, atomic_model):
                self._id = _id
                self.atomic_model = atomic_model

            def __enter__(self):
                uuid_ = uuid.uuid1()
                self.atomic_model.objects.filter(_id=self._id, in_freeze=False).first().update({'freeze_by': uuid_,
                                                                                       'in_freeze': True})
                user = self.atomic_model.find_by_id_(self._id)
                if user.freeze_by != uuid_:
                    raise Exception('user is freeze')

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.atomic_model.find_by_id_(self._id).update({'in_freeze': False})
        return Context(self._id, self.atomic_model)
