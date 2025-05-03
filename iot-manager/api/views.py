from rest_framework import viewsets
from app.models import (
	Device,
	Rule,
	Log
)
from app.serializers import (
	DeviceSerializer,
	RuleSerializer,
	LogSerializer
)

# Create your views here.
class DeviceViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Device.objects.all()
	serializer_class = DeviceSerializer
