from django.db import models

# Create your models here.
class Register(models.Model):
    username = models.CharField(max_length=150, unique=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username