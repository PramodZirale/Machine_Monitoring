from rest_framework import serializers
from .models import Machine_IO

class Machine_IO_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Machine_IO
        fields = ['parameter_name', 'plc_address', 'min_max_flag', 'min_range', 'max_range', 'actual_values', 'email_flag']
