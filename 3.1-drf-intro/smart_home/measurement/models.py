from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя датчика')
    description = models.TextField(verbose_name='Описание')
    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'
        ordering = ['id']
    def __str__(self):
        return f'{self.id} {self.name}: {self.description}'


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements', verbose_name='Датчик')
    temperature = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Температура')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время')
    image = models.ImageField(upload_to='images', null=True, blank=True, verbose_name='Фото')
    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'
        ordering = ['sensor', 'created_at']

    def __str__(self):
        return f'{self.sensor} {self.temperature} / {self.created_at}'




