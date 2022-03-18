from django.shortcuts import render, get_object_or_404
from .models import City
from django.views.generic import DetailView
from .forms import CityForm


# Create your views here.
def home(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
    form = CityForm
    all_city_objects = City.objects.all()
    context = {'objects_list': all_city_objects, 'form': form}
    return render(request, 'cities/home.html', context)


class CityDetailView(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/detail.html'
