from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

STATUS = (
    ('W', 'Want to go'),
    ('P', 'Tix Purchased'),
    ('G', 'Went to Show')
)
# Create your models here.
class Tix(models.Model):
    event_name = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    date = models.DateField()
    status = models.CharField(
        max_length=1,
        choices=STATUS,
        default=STATUS[0][0]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'tix_id': self.id})

class Photo(models.Model):
    url = models.CharField(max_length=200)
    tix = models.ForeignKey(Tix, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for tix_id: {self.tix_id} @{self.url}"