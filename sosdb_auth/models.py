from django.contrib.auth.models import AbstractUser
from django.db import models
from random import randint

class SosdbUser(AbstractUser):
	user_id = models.IntegerField(unique=True, default=randint(1,1000))

