import os
import sys
import django

project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ["DJANGO_SETTINGS_MODULE"] = "scrappingservice.settings"
django.setup()

from scraping.parsers import *
from django.db import DatabaseError
from scraping.models import Vacancy, City, Language

parsers = (
    (work, 'https://www.work.ua/jobs-kyiv-python/'),
    (rabota, 'https://rabota.ua/jobsearch/vacancy_list?regionId=1&keyWords=python'),
)

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
        print('error')
        pass


#  Write to file
import codecs

# h = codecs.open('work.json', 'w', 'utf-8')  # 'w' work with file in write mode
# h.write(str(jobs))  # write to file
# h.close()

