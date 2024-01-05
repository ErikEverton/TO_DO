from django.db import models

# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField("date published")

    def __str__(self) -> str:
        return self.title
