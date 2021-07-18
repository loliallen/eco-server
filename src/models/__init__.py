# импорт всех моделей, для корректной работы запросов
from .partner.PartnerModel import Partner
from .filter.FilterModel import Filter
from .recpoint.RecPointModel import RecPoint
from .user.UserModel import User
from .transaction.AdmissionTransaction import AdmissionTransaction
from .recycle.RecycleTransaction import RecycleTransaction
from .test.Test import Test
from .test.QuestionModel import Question
from .test.UsersAttemtps import UserAttempts
from .product.ProductModel import Product
from .product.ProductItemModel import ProductItem
from .news.NewsModel import News
