from django.db import models
from cities.models import City
from trains.models import Train


# Create your models here.


class Route(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название маршрута')
    travel_times = models.IntegerField(verbose_name='Общее время в пути')
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='route_from_city_set',
                                  verbose_name='Город отправления')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='route_to_city_set',
                                verbose_name='Город прибытия')
    trains = models.ManyToManyField(Train, verbose_name='Список поездов')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
