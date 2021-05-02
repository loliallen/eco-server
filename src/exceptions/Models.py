
class ObjectNotFound(Exception):
    message = "Object with {} not found"
    def __init__(self, id):
        self.message = self.message.format(id)

