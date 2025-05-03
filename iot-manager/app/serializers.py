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

    # Specific config for each device
    config      = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = ['id','host','port','device_type','config']

    def get_device_type(self, obj):
        """
        Returns the specific type of device.
        To it, check if it has the specific attribute
        """
        if hasattr(obj, 'dummysensor'): return 'dummysensor'
        if hasattr(obj, 'dummyclock'):  return 'dummyclock'
        if hasattr(obj, 'dummyswitch'): return 'dummyswitch'

        # This case should not happen if the device is created corerctly in the app
        return 'unknown'

    def get_config(self, obj):
        """
        Returns the specific config for the device.
        To it, check if it has the specific attribute, and for aech case it
        return the correct data
        """
        concrete = obj.get_concrete()
        if hasattr(concrete, 'interval'):
            return {
                'interval':  concrete.interval,
                'min_value': concrete.min_value,
                'max_value': concrete.max_value,
                'increment': concrete.increment,
            }
        if hasattr(concrete, 'start_time'):
            return {
                'start_time': concrete.start_time.isoformat(),
                'increment':  concrete.increment,
                'rate':       concrete.rate,
            }
        if hasattr(concrete, 'probability'):
            return {'probability': concrete.probability}
        
        # This case should not happen if the device is created corerctly in the app
        return {}
        
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
