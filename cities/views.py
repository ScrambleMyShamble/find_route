from django.shortcuts import render, get_object_or_404
from .models import City
from django.views.generic import DetailView

__all__ = (
    'home',
    'CityDetailView'
)


# Create your views here.
def home(requests):
    all_city_objects = City.objects.all()
    context = {'objects_list': all_city_objects}
    return render(requests, 'cities/home.html', context)


class CityDetailView(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/detail.html'
