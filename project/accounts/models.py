from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserInfo(User):
    middle_name = models.CharField(max_length=100, null=True, blank=True)

    def get_full_name(self):
        if self.middle_name:
            return f'{self.last_name} {self.middle_name} {self.first_name}'
        return f'{self.last_name} {self.first_name}'

