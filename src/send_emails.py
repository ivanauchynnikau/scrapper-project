import os
import sys
import datetime
import django
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scrappingservice.settings"
django.setup()

from scraping.models import Vacancy
from scraping.models import Error
from scrappingservice.settings import EMAIL_HOST_USER

ADMIN_USER = EMAIL_HOST_USER
today = datetime.date.today()
empty = '<h2>Sorry, but today no any new vacancies</h2>'
subject = f'Vacancies from scraping.service for {today}'
text_content = f'Vacancies from scraping.service {today}'
from_email = EMAIL_HOST_USER


User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dct = {}

for i in qs:
    users_dct.setdefault((i['city'], i['language']), [])
    users_dct[(i['city'], i['language'])].append(i['email'])

if users_dct:
    params = {'city_id__in': [], 'language_id__in': []}

    for pair in users_dct.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])

    qs = Vacancy.objects.filter(**params, timestamp=today).values()

    vacancies = {}
    for i in qs:
        vacancies.setdefault((i['city_id'], i['language_id']), [])
        vacancies[(i['city_id'], i['language_id'])].append(i)

    for keys, emails in users_dct.items():
        rows = vacancies.get(keys, [])
        html = ''

        for row in rows:
            html += f'<p><a href="{ row["url"] }" target="_blank">{ row["title"] }</a></p>'
            html += f'<p>{ row["company"] }</p>'
            html += f'<p>{ row["description"] }</p>'
            html += f'<br><hr>'

        _html = html if html else empty

        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()


qs = Error.objects.filter(timestamp=today)

if qs.exists():
    error = qs.first()
    errors = error.data

    errors_html = ''

    for item in errors:
        errors_html += f'<p>{item["title"]}</p>'
        errors_html += f'<p>Error with <a href="{item["url"]}" target="_blank">{item["url"]}</a></p>'
        errors_html += f'<br><hr>'

    subject = f'Scraping error report {today}'

    msg = EmailMultiAlternatives(subject, subject, from_email, [ADMIN_USER])
    msg.attach_alternative(errors_html, "text/html")
    msg.send()
