import factory.fuzzy

from src.models.filter.FilterModel import Filter
from src.models.recpoint.RecPointModel import RecPoint, DISTRICTS
from src.models.utils.enums import Status


class FilterFactory(factory.DictFactory):
    name = factory.Faker('word')
    var_name = factory.LazyAttribute(lambda x: x.name.lower() + '__test')
    key_words = factory.List([factory.Faker('word') for _ in range(2)])
    bad_words = factory.List([factory.Faker('word') for _ in range(2)])
    image = None
    coins_per_unit = factory.fuzzy.FuzzyInteger(1, 15)
    visible = True


class FilterModelFactory(factory.mongoengine.MongoEngineFactory):
    name = factory.Faker('word')
    var_name = factory.LazyAttribute(lambda x: x.name.lower() + '__test')

    class Meta:
        model = Filter


class RecPointModelFactory(factory.mongoengine.MongoEngineFactory):
    name = factory.Faker('word')
    address = factory.Faker('word')
    # accept_types = factory.RelatedFactory(FilterModelFactory)
    approve_status = Status.confirmed.value
    district = factory.fuzzy.FuzzyChoice(DISTRICTS)

    class Meta:
        model = RecPoint
