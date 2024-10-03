from django.contrib import admin
from .models import Machine_IO,Machine_IO_Log,PLCConfig

@admin.register(Machine_IO)
class MachineIOAdmin(admin.ModelAdmin):
    list_display = ['parameter_name', 'plc_address', 'min_max_flag', 'min_range', 'max_range', 'actual_values','email_flag']


@admin.register(Machine_IO_Log)
class MachineIOLogAdmin(admin.ModelAdmin):
    list_display = ('machine_io', 'actual_values', 'timestamp')

    # Define the custom action
    actions = ['flush_all_records']

    # Action to delete all records in Machine_IO_Log
    def flush_all_records(self, request, queryset):
        # Delete all Machine_IO_Log records
        Machine_IO_Log.objects.all().delete()
        self.message_user(request, "All Machine_IO_Log records have been cleared.")

    # Give the action a user-friendly name
    flush_all_records.short_description = "Flush all log records"

@admin.register(PLCConfig)
class PLCConfigAdmin(admin.ModelAdmin):
    list_display = ('plc_ip', 'plc_port')