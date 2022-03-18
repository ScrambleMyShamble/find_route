from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from cities.models import City


class Train(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название поезда')
    travel_time = models.IntegerField(verbose_name='Время в пути')
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='from_city_set',
                                  verbose_name='Город отправления')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='to_city_set',
                                verbose_name='Город прибытия')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поезд'
        verbose_name_plural = 'Поезда'

    def clean(self):
        if self.from_city == self.to_city:
            raise ValidationError('Измените город прибытия')
        checking_entry = Train.objects.filter(from_city=self.from_city, travel_time=self.travel_time,
                                              to_city=self.to_city).exclude(pk=self.pk)
        if checking_entry.exists():
            raise ValidationError('Измените время в пути')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
