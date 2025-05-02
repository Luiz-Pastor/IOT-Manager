from django.contrib import admin
from .models import (
	DummySensor,
	DummyClock,
	DummySwitch,
	Rule,
	Log
)

# Register your models here.
admin.site.register(DummySensor)
admin.site.register(DummyClock)
admin.site.register(DummySwitch)
admin.site.register(Rule)
admin.site.register(Log)
