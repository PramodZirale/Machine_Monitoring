from django.db import models
from django.utils import timezone

class Machine_IO(models.Model):
    parameter_name = models.CharField(max_length=255)
    plc_address = models.CharField(max_length=255)
    min_max_flag = models.BooleanField(null=True, blank=True, default=False)  # Updated
    min_range = models.IntegerField(null=True, blank=True)
    max_range = models.IntegerField(null=True, blank=True)
    actual_values = models.IntegerField(null=True, blank=True)
    email_flag = models.BooleanField(default=False)  # Updated

    def __str__(self):
        return self.parameter_name

# Machine_IO_Log model to store dynamic log data related to Machine_IO
class Machine_IO_Log(models.Model):
    machine_io = models.ForeignKey(Machine_IO, on_delete=models.CASCADE, related_name='logs')  # Connect to parent Machine_IO model
    actual_values = models.IntegerField(null=True, blank=True)  # Actual IO values logged
    timestamp = models.DateTimeField(default=timezone.now)  # Logs the time of entry

    def __str__(self):
        return f"Log for {self.machine_io.parameter_name} at {self.machine_io.plc_address}"


class PLCConfig(models.Model):
    plc_ip = models.CharField(max_length=255, default='192.168.228.52')  # Default IP
    plc_port = models.IntegerField(default=5010)  # Default Port

    def __str__(self):
        return f"PLC Config - {self.plc_ip}:{self.plc_port}"
