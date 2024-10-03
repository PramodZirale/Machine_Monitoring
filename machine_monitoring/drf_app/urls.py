from django.urls import path
from .views import Machine_IO_ViewSet, MachineIOLogsTop10,UpdatePLCValues


# Explicitly map the routes
urlpatterns = [
    path('machine_io/', Machine_IO_ViewSet.as_view({'get': 'list', 'post': 'create'}), name='machine-io-list-create'),
    path('machine_io/<str:parameter_name>/', Machine_IO_ViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('get/machine_io/top10/', MachineIOLogsTop10.as_view(), name='machine-io-top10'),  # Custom API for top 10 logs
    path('get/machine_io/update_plc_values/', UpdatePLCValues.as_view(), name='update-plc-values'),
]
