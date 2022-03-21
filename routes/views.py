from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView

from .forms import RouteForm, RouteModelForm
from .utils import get_routes
from .models import Train, Route
from .models import City


# Create your views here.


def home(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})


def find_routes(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            try:
                context = get_routes(request, form)
            except ValueError as error_message:
                messages.error(request, error_message)
                return render(request, 'routes/home.html', {'form': form})
            return render(request, 'routes/home.html', context)
        return render(request, 'routes/home.html', {'form': form})
    else:
        form = RouteForm()
        messages.error(request, 'Введите данные для поиска')
        return render(request, 'routes/home.html', {'form': form})


def add_route(request):
    if request.method == 'POST':
        context = {}
        if request.POST:
            total_time = request.POST.get('total_time', False)
            from_city = request.POST['from_city']
            to_city = request.POST['to_city']
            trains = request.POST['trains'].split(',')
            id_from_trains = [int(i) for i in trains if i.isdigit()]
            query = Train.objects.filter(id__in=id_from_trains)
            cities = City.objects.filter(id__in=[from_city, to_city]).in_bulk()
            form = RouteModelForm(initial=
                                  {'from_city': cities[int(from_city)],
                                   'to_city': cities[int(to_city)],
                                   'travel_times': total_time,
                                   'trains': query})
            context['form'] = form

        return render(request, 'routes/create.html', context)
    else:
        return redirect('/')


def save_route(request):
    if request.method == "POST":
        form = RouteModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Маршрут успешно сохранен")
            return redirect('/')
        return render(request, 'routes/create.html', {'form': form})
    else:
        return redirect('/')


class RouteListView(ListView):
    paginate_by = 10
    model = Route
    template_name = 'routes/route_list.html'


class RouteDetailView(DetailView):
    queryset = Route.objects.all()
    template_name = 'routes/route_detail.html'


class RouteDeleteView(LoginRequiredMixin, DeleteView):
    model = Route
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Маршрут успешно удален')
        return self.post(request, *args, **kwargs)
