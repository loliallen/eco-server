from enum import Enum


class Status(Enum):
    idle = 'idle'
    confirmed = 'confimed'
    dismissed = 'dismissed'


STATUS_CHOICES = ('idle', 'confimed', 'dismissed')
