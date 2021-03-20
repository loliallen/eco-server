from mongoengine import Document, StringField, QuerySet, DateTimeField
from pathlib import Path
from slugify import slugify
from datetime import datetime

import markdown
import os


REL_PATH = "/statics/news"
files_storage = Path('./src'+REL_PATH)


class News(Document):
    header = StringField(required=True)
    slug = StringField(required=True)
    text = StringField(required=True)
    image = StringField()
    updated = DateTimeField(default=datetime.utcnow())
    meta = {
        'db_alias': 'core',
        'collection': 'news'
    }


def read():
    news = News.objects.all()
    return news


def create(header: str, text: str, image: str = "") -> News:
    news = News()
    news.header = header
    news.text = markdown.markdown(text)
    news.slug = slugify(header)
    news.save()

    if image != "":
        mime_type = image.split('.').pop()
        filename = str(news.id) + "." + mime_type
        img_path = REL_PATH + "/" + filename
        old_path = files_storage / image
        new_path = files_storage / filename
        os.rename(old_path.resolve(), new_path.resolve())
        news.image = img_path

    news.save()

    return news


def update(_id:str, updates: dict):
    news = find_by_id(_id)

    if not news:
        return None

    if "header" in updates:
        updates['slug'] = slugify(updates['header'])

    if 'image' in updates:
        mime_type = updates['image'].split('.').pop()
        filename = str(news.id) + "." + mime_type
        img_path = REL_PATH + "/" + filename
        old_path = files_storage / updates['image']
        new_path = files_storage / filename
        os.remove(Path(str(Path.cwd()) + '/src/' + news.image))
        os.rename(old_path.resolve(), new_path.resolve())
        updates['image'] = img_path

    updates['updated'] = datetime.utcnow()

    news.update(**updates)
    return news


def delete(_id: str) -> News:
    news = find_by_id(_id)

    if not news:
        return None

    os.remove(Path(str(Path.cwd()) + '/src/' + news.image))
    news.delete()
    return news


def find_by_id(_id: str) -> News:
    news = None
    news = News.objects(id=_id).first()
    return news


def find_by_slug(_slug: str) -> News:
    news = None
    news = News.objects(slug=_slug).first()
    return news