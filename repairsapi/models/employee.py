from django.db import models
from django.contrib.auth.models import User

# user, a 1 to 1 is considered a foreign key
# which means we can expand this
# but this property is in essence
# 2 levels down from the service ticket

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=155)

    # property decorator, we define a new property
    @property
    def full_name(self):
        """Additional address field to capture from the client"""
        return f'{self.user.first_name} {self.user.last_name}'
