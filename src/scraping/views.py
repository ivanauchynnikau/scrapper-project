from django.shortcuts import render
from .forms import FindForm
from .models import Vacancies


def home_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')

    if city or language:
        _filter = {}

        if city:
            _filter['city__slug'] = city
        elif language:
            _filter['language__slug'] = language

    qs = Vacancies.objects.filter(**_filter)  # TODO зачем тут **_filter ???
    return render(request, 'scraping/home.html', {'object_list': qs, 'form': form})
