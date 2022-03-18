from django.shortcuts import render
from .forms import RouteForm


# Create your views here.
def home(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})
