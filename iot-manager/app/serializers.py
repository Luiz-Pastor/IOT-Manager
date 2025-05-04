from rest_framework import serializers
from .models import (
	Device,
    Rule,
    Log
)

class DeviceSerializer(serializers.ModelSerializer):
    """
    Device general serializer
    """
    # Device type (dummysensor, dummyclock or dummyswitch)
    device_type = serializers.SerializerMethodField()

    # Specific variable where the device state is stored
    state_variable = serializers.SerializerMethodField()

    # Specific config for each device
    configuration = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = [
            'id',
            'host',
            'port',
            'status_topic',
            'command_topic',
            'device_type',
            'state_variable',
            'configuration'
        ]

    def get_device_type(self, obj):
        """
        Returns the specific type of device.
        To it, check if it has the specific attribute.
        
        It is made in such a way that what is returned is
        the name of the script to be executed, so that the
        controller is as generic as possible.
        """
        if hasattr(obj, 'dummysensor'): return 'dummy-sensor'
        if hasattr(obj, 'dummyclock'):  return 'dummy-clock'
        if hasattr(obj, 'dummyswitch'): return 'dummy-switch'

        # This case should not happen if the device is created corerctly in the app
        return 'unknown'

    def get_state_variable(self, obj):
        try:
            concrete = obj.get_concrete()
            return concrete.variable_name
        except Exception:
            return None

    def get_configuration(self, obj):
        """
        Returns the specific config for the device.
        To it, check if it has the specific attribute, and for aech case it
        return the correct data
        """
        concrete = obj.get_concrete()
        configuration = {}
        if hasattr(concrete, 'interval'):
            configuration = {
                'interval':  concrete.interval,
                'min_value': concrete.min_value,
                'max_value': concrete.max_value,
                'increment': concrete.increment,
            }
        if hasattr(concrete, 'start_time'):
            configuration = {
                'start_time': concrete.start_time.isoformat(),
                'increment':  concrete.increment,
                'rate':       concrete.rate,
            }
        if hasattr(concrete, 'probability'):
            configuration = {
                'probability': concrete.probability
            }
        
        # This case should not happen if the device is created corerctly in the app
        return configuration
        
class RuleSerializer(serializers.ModelSerializer):
    """
    Rule serializer
    """
    class Meta:
        model = Rule
        fields = [
            'id','name',
            'source_device','operator','threshold', 'target_device','command_payload'
        ]

class LogSerializer(serializers.ModelSerializer):
    """
    Log serializer
    """
    class Meta:
        model = Log
        fields = ['id','message','timestamp']
        read_only_fields = ['id','timestamp']
