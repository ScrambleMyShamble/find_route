from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RouteForm
from .utils import get_routes


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
        return render(request, 'routes/create.html', context)
    else:
        return redirect('/')
