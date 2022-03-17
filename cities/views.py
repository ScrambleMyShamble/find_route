from django.shortcuts import render, get_object_or_404
from .models import City

__all__ = (
    'home'
)


# Create your views here.
def home(requests, pk=None):
    if pk:
        city = get_object_or_404(City, id=pk)
        context = {'object': city}
        return render(requests, 'cities/detail.html', context)

    all_city_objects = City.objects.all()
    context = {'objects_list': all_city_objects}
    return render(requests, 'cities/home.html', context)
