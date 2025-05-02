# devices/forms.py
from django import forms
from .models import DummySensor, DummyClock, DummySwitch, Rule

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

class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ['name', 'source_device', 'operator', 'threshold', 'target_device', 'command_payload']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'source_device': forms.Select(attrs={'class': 'form-select'}),
            'operator': forms.Select(attrs={'class': 'form-select'}),
            'threshold': forms.TextInput(attrs={'class': 'form-control'}),
            'target_device': forms.Select(attrs={'class': 'form-select'}),
            'command_payload': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        help_texts = {
            'command_payload': 'Debe incluir al menos el campo "cmd", e.j. {"cmd":"set","state":"ON"}',
        }