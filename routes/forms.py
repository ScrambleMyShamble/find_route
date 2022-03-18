from django import forms
from cities.models import City

from .models import Route


class RouteForm(forms.Form):
    from_city = forms.ModelChoiceField(label='Город отправления', queryset=City.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}
                                                           ))
    to_city = forms.ModelChoiceField(label='Город прибытия', queryset=City.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}
                                                         ))
    cities = forms.ModelMultipleChoiceField(label='Через города', queryset=City.objects.all(),
                                            required=False, widget=forms.SelectMultiple(attrs={'class': 'form-control'}
                                                                                        ))
    traveling_time = forms.IntegerField(label='Время в пути', widget=forms.NumberInput(attrs={
        'class': 'form-control', 'placeholder': 'Время в пути'}
    ))

    class Meta:
        model = Route
        fields = '__all__'
