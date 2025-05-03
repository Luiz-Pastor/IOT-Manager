from rest_framework import viewsets, mixins
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
	"""
	API endpoint that allows devices to be viewed.
		· GET: /devices: returns all the devices data
	"""
	queryset = Device.objects.all()
	serializer_class = DeviceSerializer

class RuleViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	API endpoint that allows rules to be viewed.
		· GET: /rules: returns all the rules data
	"""
	queryset = Rule.objects.all()
	serializer_class = RuleSerializer

class LogViewSet(
	mixins.CreateModelMixin,	# Create the logs
	viewsets.GenericViewSet,
):
	"""
	API endpoint that allows logs to be created.
		· POST: /logs: create the new log
	"""
	queryset = Log.objects.all()
	serializer_class = LogSerializer
	http_method_names = ['POST']
