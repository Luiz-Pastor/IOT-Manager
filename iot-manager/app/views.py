from django.urls import reverse, reverse_lazy
from django.views.generic import (
	CreateView,
	TemplateView,
	ListView,
	DetailView,
	UpdateView,
)
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404

from .models import (
	Device,
	Rule
)
from .forms import (
	DummySensorForm,
	DummyClockForm,
	DummySwitchForm,
	RuleForm
)

##############
# NOTE: Home #
##############

class IndexView(TemplateView):
    """
    Index view for the devices and rules.
    """
    template_name = "index.html"


#################
# NOTE: Devices #
#################

DEVICE_FORMS = {
    "sensor":  (DummySensorForm,  "DummySensor"),
    "clock":   (DummyClockForm,   "DummyClock"),
    "switch":  (DummySwitchForm,  "DummySwitch"),
}

class DeviceCreateView(CreateView):
    """
    View to create a new device.
    """
    template_name = "devices/device_create.html"    
    success_url = reverse_lazy("device-list")

    def dispatch(self, request, *args, **kwargs):
        """
        Redirect taking into account the device type.
        """
        # Get the device type
        self.dev_type = request.GET.get("type")
        if request.method == "POST":
            self.dev_type = request.POST.get("dev_type")
        
        # If there is no device, or an unknown one, show the type selection
        if not self.dev_type or self.dev_type not in DEVICE_FORMS:
            return TemplateView.as_view(
                template_name="devices/device_type_select.html"
            )(request, *args, **kwargs)
        
        # If the device type is valid, continue with the form
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        """
        Get the form class based on the device type.
        Used to know what form has to be redered
        """
        form_class, _ = DEVICE_FORMS[self.dev_type]
        return form_class

    def get_context_data(self, **ctx):
        context = super().get_context_data(**ctx)
        _, pretty = DEVICE_FORMS[self.dev_type]
        context["device_type_name"] = pretty
        context["dev_type"] = self.dev_type
        return context

    def form_valid(self, form):
        # TODO: send the information to the controller
        return super().form_valid(form)

class DeviceListView(ListView):
    """
    Show all the registered devices
    """
    model = Device
    template_name = "devices/device_list.html"
    context_object_name = "devices"
    paginate_by = 10

@require_POST
def device_delete(request, pk):
    """
    Delete the device with the provided primary key
    """
    device = get_object_or_404(Device, pk=pk)
    device.delete()
    return redirect(reverse('device-list'))

class DeviceDetailView(DetailView):
    """
    Muestra todos los datos (comunes y específicos) de un dispositivo.
    """
    model = Device
    template_name = "devices/device_detail.html"
    context_object_name = "device"


###############
# NOTE: Rules #
###############

class RuleCreateView(CreateView):
    model = Rule
    form_class = RuleForm
    template_name = "rules/rule_form.html"
    success_url = reverse_lazy("rule-list")

    def form_valid(self, form):
        # TODO: send the information to the controller
        return super().form_valid(form)

class RuleListView(ListView):
    model = Rule
    template_name = "rules/rule_list.html"
    context_object_name = "rules"

@require_POST
def rule_delete(request, pk):
    """
    Delete the rule with the provided primary key
    """
    rule = get_object_or_404(Rule, pk=pk)
    rule.delete()
    return redirect(reverse('rule-list'))

class RuleDetailView(DetailView):
    """
    Muestra los datos de una regla.
    """
    model = Rule
    template_name = "rules/rule_detail.html"
    context_object_name = "rule"

class RuleUpdateView(UpdateView):
    """
    Muestra un formulario para editar una regla existente
    y actualiza la base de datos.
    """
    model = Rule
    form_class = RuleForm
    template_name = "rules/rule_update.html"
    success_url = reverse_lazy("rule-list")

    def form_valid(self, form):
        # TODO: send the information to the controller
        return super().form_valid(form)
