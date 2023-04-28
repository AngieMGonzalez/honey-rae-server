from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=155)

    @property
    def full_name(self):
        """Additional address field to capture from the client"""
        return f'{self.user.first_name} {self.user.last_name}'
