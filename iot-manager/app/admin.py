from django.contrib import admin
from .models import DummySensor, DummyClock, DummySwitch

# Register your models here.
admin.site.register(DummySensor)
admin.site.register(DummyClock)
admin.site.register(DummySwitch)
