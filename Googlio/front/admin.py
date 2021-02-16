from django.contrib import admin
from .models import Email
from .models import Event

# Register your models here.
admin.site.register(Email)
admin.site.register(Event)
