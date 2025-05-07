# devices/forms.py
from django import forms
from .models import DummySensor, DummyClock, DummySwitch, Rule

class DummySensorForm(forms.ModelForm):
    class Meta:
        model = DummySensor
        fields = ["id", "host", "port", "interval", "min_value", "max_value", "increment"]

    def get_extra_args(self):
        """
        Get the extra arguments for the form.
        """
        return [
            "--interval", str(self.cleaned_data.get("interval")),
            "--min", str(self.cleaned_data.get("min_value")),
            "--max", str(self.cleaned_data.get("max_value")),
            "--increment", str(self.cleaned_data.get("increment")),
        ]

class DummyClockForm(forms.ModelForm):
    class Meta:
        model = DummyClock
        fields = ["id", "host", "port", "start_time", "increment", "rate"]

    def get_extra_args(self):
        """
        Get the extra arguments for the form.
        """
        return [
            "--time", str(self.cleaned_data.get("start_time")),
            "--increment", str(self.cleaned_data.get("increment")),
            "--rate", str(self.cleaned_data.get("rate")),
        ]

class DummySwitchForm(forms.ModelForm):
    class Meta:
        model = DummySwitch
        fields = ["id", "host", "port", "probability"]

    def get_extra_args(self):
        """
        Get the extra arguments for the form.
        """
        return [
            "--probability", str(self.cleaned_data.get("probability")),
        ]

class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ['name', 'source_device', 'operator', 'threshold', 'target_device', 'command_payload']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kitchen temperature manager'
            },),
            'source_device': forms.Select(attrs={'class': 'form-select'}),
            'operator': forms.Select(attrs={'class': 'form-select'}),
            'threshold': forms.TextInput(attrs={'class': 'form-control'}),
            'target_device': forms.Select(attrs={'class': 'form-select'}),
            'command_payload': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        help_texts = {
            'name': 'Name of the rule to create',
            'source_device': 'Device that will activate the rule',
            'operator': 'Comparation to do between the value and the threshold',
            'threshold': 'Value to compare with the actual limit value',
            'target_device': 'Device to which the message will be sent if the condition is met',
            'command_payload': 'Message to send. Has to have the "cmd" field, e.j. {"cmd":"set","state":"ON"}',
        }