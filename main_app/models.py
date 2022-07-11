from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Tix(models.Model):
    event_name = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'tix_id': self.id})