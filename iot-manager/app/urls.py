from django.urls import path
from django.shortcuts import redirect, get_object_or_404
from .views import (
	IndexView,

	DeviceCreateView,
	DeviceListView,
	device_delete,
	DeviceDetailView,
	# DeviceUpdateView,
    SensorUpdateView,
	ClockUpdateView,
	SwitchUpdateView,

	RuleCreateView,
	RuleListView,
	rule_delete,
	RuleDetailView,
	RuleUpdateView,

	LogListView
)
from .models import Device

def device_update_redirect(request, pk):
    base = get_object_or_404(Device, pk=pk)
    concrete = base.get_concrete()
    name = concrete.__class__.__name__.lower()
    if name == "dummysensor":
        return redirect("sensor-update", pk=pk)
    if name == "dummyclock":
        return redirect("clock-update",  pk=pk)
    if name == "dummyswitch":
        return redirect("switch-update", pk=pk)
    return redirect("device-list")

urlpatterns = [
	path("", IndexView.as_view(), name="index"),

	path("device/create", DeviceCreateView.as_view(), name="device-create"),
	path("device/list", DeviceListView.as_view(), name="device-list"),
	path("device/delete/<str:pk>", device_delete, name="device-delete"),
	path("device/<str:pk>", DeviceDetailView.as_view(), name="device-detail"),
    # path("device/<str:pk>/update", DeviceUpdateView.as_view(), name="device-edit"),

    path("device/<str:pk>/update/", device_update_redirect, name="device-edit"),
    path("sensor/<str:pk>/edit/",  SensorUpdateView.as_view(), name="sensor-update"),
    path("clock/<str:pk>/edit/",   ClockUpdateView.as_view(),  name="clock-update"),
    path("switch/<str:pk>/edit/",  SwitchUpdateView.as_view(), name="switch-update"),

	path("rule/create", RuleCreateView.as_view(), name='rule-create'),
	path("rule/list", RuleListView.as_view(), name="rule-list"),
	path("rule/delete/<int:pk>", rule_delete, name="rule-delete"),
	path("rule/<int:pk>", RuleDetailView.as_view(), name="rule-detail"),
	path("rule/<int:pk>/update", RuleUpdateView.as_view(), name="rule-edit"),

	path("log/list", LogListView.as_view(), name="log-list"),
]
