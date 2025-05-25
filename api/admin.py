from django.contrib import admin
from . models import User,CRUD
# Register your models here.

admin.site.register(CRUD)
admin.site.register(User)