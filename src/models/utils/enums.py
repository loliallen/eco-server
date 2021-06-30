from enum import Enum


class Status(Enum):
    idle = 'idle'
    confirmed = 'confirmed'
    dismissed = 'dismissed'


STATUS_CHOICES = ('idle', 'confirmed', 'dismissed')
