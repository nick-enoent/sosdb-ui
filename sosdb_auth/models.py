from django.contrib.auth.models import AbstractUser
from django.db import models
from random import randint

def random_id():
    return randint(1, 1000)

class SosdbUser(AbstractUser):
	user_id = models.IntegerField(unique=True, default=random_id)
