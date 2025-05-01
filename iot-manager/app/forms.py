# devices/forms.py
from django import forms
from .models import DummySensor, DummyClock, DummySwitch

class DummySensorForm(forms.ModelForm):
    class Meta:
        model = DummySensor
        fields = ["id", "host", "port", "interval", "min_value", "max_value", "increment"]

class DummyClockForm(forms.ModelForm):
    class Meta:
        model = DummyClock
        fields = ["id", "host", "port", "start_time", "increment", "rate"]

class DummySwitchForm(forms.ModelForm):
    class Meta:
        model = DummySwitch
        fields = ["id", "host", "port", "probability"]
