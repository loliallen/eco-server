

class FieldError(Exception):
    def __init__(self, field, info):
        self.field = field
        self.info = info
