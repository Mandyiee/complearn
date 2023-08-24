from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from .models import *

admin.site.unregister(User)

admin.site.unregister(Group)

admin.site.register(Composite)