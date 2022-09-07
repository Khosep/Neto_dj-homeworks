from django.db import models
from django.utils.text import slugify


class Phone(models.Model):
    name = models.CharField(max_length=40)
    image = models.URLField(max_length=200)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    release_date = models.DateField()
    lte_exists = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Phone, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id} {self.name}: {self.price} RUB'
