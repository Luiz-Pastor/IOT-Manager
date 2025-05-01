from django.urls import path
from .views import DeviceCreateView

urlpatterns = [
	path("device/create", DeviceCreateView.as_view(), name="create-device"),
]