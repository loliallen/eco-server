from datetime import datetime

import factory

from src.controllers.utils.hash_password import generate_salt, hash_password
from src.models.user.UserModel import User
from src.utils.roles import Roles


class UserFactory(factory.DictFactory):
    name = factory.Faker('name')
    username = factory.Faker('email')
    password = 'SuperPassword1234'


class UserModelFactory(factory.mongoengine.MongoEngineFactory):
    name = factory.Faker('name')
    username = factory.Faker('email')
    salt = factory.LazyFunction(lambda: generate_salt())
    password_ = 'SuperPassword1234'
    password = factory.LazyAttribute(lambda x: hash_password(x.password_, x.salt))
    confirmed = True
    confirmed_on = factory.LazyFunction(lambda: datetime.utcnow())
    role = Roles.user.value

    class Meta:
        exclude = ('password_',)
        model = User
