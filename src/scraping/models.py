from django.db import models

from scraping.utils import from_cyrillic_to_eng
import jsonfield


def default_urls():
    return {"work": "", "rabota": ""}


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='City', unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)  # TODO зачем передвавать args kwargs ???


class Language(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Programming language', unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Programming language'
        verbose_name_plural = 'Programming languages'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)  # TODO зачем передвавать args kwargs ???


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Vacancy title')
    company = models.CharField(max_length=250, verbose_name='Company')
    description = models.TextField(verbose_name='Vacancy description')
    city = models.ForeignKey('City', on_delete=models.CASCADE,
                             verbose_name='City', related_name='vacancies')
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 verbose_name='Programming language')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title


class Error(models.Model):
    title = models.CharField(max_length=250, verbose_name='Error title')
    data = jsonfield.JSONField(verbose_name='Error details')

    class Meta:
        verbose_name = 'Error'
        verbose_name_plural = 'Errors'


class Url(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE,
                             verbose_name='City')
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 verbose_name='Programming language')
    url_data = jsonfield.JSONField(default=default_urls)

    class Meta:
        unique_together = ("city", "language")

    def __str__(self):
        return '{} {}'.format(self.city, self.language)  

