from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass    


class CRUD(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=200)
    message = models.CharField(max_length=1000)
    createdAt = models.DateTimeField(auto_now_add=True)