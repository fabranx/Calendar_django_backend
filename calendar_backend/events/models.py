from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model


class Event(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # date = models.CharField(max_length=10)
    date = models.DateField(auto_now=False, blank=False)
    description = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Author:{self.author}\n Date: {self.date}\n Description {self.description}"
