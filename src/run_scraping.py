import os
import sys
import django
from django.contrib.auth import get_user_model

project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ["DJANGO_SETTINGS_MODULE"] = "scrappingservice.settings"
django.setup()

from scraping.parsers import *
from django.db import DatabaseError
from scraping.models import Vacancy, City, Language, Error, Url

User = get_user_model()

parsers = (
    (work, 'https://www.work.ua/jobs-kyiv-python/'),
    (rabota, 'https://rabota.ua/jobsearch/vacancy_list?regionId=1&keyWords=python'),
)


def get_settings():
    qs = User.objects.filter(send_email=True).values()  # .values() вернет список словарей (массивов
    settings_list = set((q['city_id'], q['language_id']) for q in qs)  # TODO что такое set()
    return settings_list


def get_urls(_settings):  # TODO зачем _ в начале аргумента?
    qs = Url.objects.all().values()
    url_dictionary = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []

    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dictionary[pair]
        urls.append(tmp)

    return urls


settings = get_settings()
u = get_urls(settings)


city = City.objects.filter(slug='kiev').first()
language = Language.objects.filter(slug='python').first()

jobs, errors = [], []

for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, city=city, language=language)

    try:
        v.save()
    except DatabaseError:
        pass  # просто скипаем ошибку

if errors:
    er = Error(data=errors)

#  Write to file
import codecs

# h = codecs.open('work.json', 'w', 'utf-8')  # 'w' work with file in write mode
# h.write(str(jobs))  # write to file
# h.close()

