from .models import Machine_IO, Machine_IO_Log,PLCConfig
from rest_framework import viewsets
from .serializers import Machine_IO_Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pymcprotocol
from django.utils import timezone
import requests
import threading
import socket


def trigger_update_plc_values():
    try:
        update_url = 'http://localhost:8000/api/get/machine_io/update_plc_values/'
        requests.get(update_url)
        print("PLC values update triggered.")
    except Exception as e:
        print(f"Failed to trigger PLC update: {e}")

class Machine_IO_ViewSet(viewsets.ViewSet):
    def list(self, request):
        # Fetch and sort Machine_IO objects by 'parameter_name'
        queryset = Machine_IO.objects.all().order_by('parameter_name')
        serializer = Machine_IO_Serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = Machine_IO_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, parameter_name=None):
        try:
            machine_io = Machine_IO.objects.get(parameter_name=parameter_name)
        except Machine_IO.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Machine_IO_Serializer(machine_io)
        return Response(serializer.data)

    def update(self, request, parameter_name=None):
        try:
            machine_io = Machine_IO.objects.get(parameter_name=parameter_name)
        except Machine_IO.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Machine_IO_Serializer(machine_io, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, parameter_name=None):
        try:
            machine_io = Machine_IO.objects.get(parameter_name=parameter_name)
        except Machine_IO.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        machine_io.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MachineIOLogsTop10(APIView):
    def get(self, request, format=None):
        threading.Thread(target=trigger_update_plc_values).start()

        # Fetch and sort Machine_IO objects by 'parameter_name'
        parameters = Machine_IO.objects.all().order_by('parameter_name')
        response_data = []

        for parameter in parameters:
            logs = Machine_IO_Log.objects.filter(machine_io=parameter).order_by('-timestamp')[:10]
            log_values = [log.actual_values for log in logs][::-1]
            log_values += [0] * (10 - len(log_values))  # Fill with zeros

            response_data.append({
                'parameter_name': parameter.parameter_name,
                '01': log_values[0],
                '02': log_values[1],
                '03': log_values[2],
                '04': log_values[3],
                '05': log_values[4],
                '06': log_values[5],
                '07': log_values[6],
                '08': log_values[7],
                '09': log_values[8],
                '10': log_values[9]
            })

        return Response(response_data, status=status.HTTP_200_OK)


# Create a PLC client to connect to Mitsubishi PLC with error handling
def connect_to_plc(ip, port):
    try:
        plc_client = pymcprotocol.Type3E()
        plc_client.connect(ip, port)
        return plc_client
    except socket.timeout:
        print(f"Timeout connecting to PLC at {ip}:{port}")
        return None
    except Exception as e:
        print(f"Failed to connect to PLC at {ip}:{port}: {e}")
        return None


# UpdatePLCValues API with error handling for PLC communication
class UpdatePLCValues(APIView):
    def get(self, request, format=None):
        # Fetch PLC IP and port from PLCConfig model
        try:
            plc_config = PLCConfig.objects.first()  # Assuming only one config entry
            if not plc_config:
                return Response({"error": "PLC configuration not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            plc_ip = plc_config.plc_ip
            plc_port = plc_config.plc_port
        except Exception as e:
            return Response({"error": f"Error fetching PLC configuration: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Connect to the PLC
        plc_client = connect_to_plc(plc_ip, plc_port)

        if plc_client is None:
            # If connection failed, return a 500 error response
            return Response({"error": "PLC not connected. Unable to read values."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # Fetch and sort Machine_IO objects by 'parameter_name'
            machine_ios = Machine_IO.objects.all().order_by('parameter_name')
            response_data = []

            # Loop through each record, read the PLC value, update, and log it only if there's a change
            for machine_io in machine_ios:
                plc_address = machine_io.plc_address

                # Read the current value from the PLC
                try:
                    actual_value = plc_client.batchread_wordunits(headdevice=plc_address, readsize=1)[0]
                except Exception as e:
                    print(f"Failed to read from PLC address {plc_address}: {e}")
                    continue  # Skip this entry and move to the next

                # Check if the new value is different from the existing value
                if machine_io.actual_values != actual_value:
                    # Update the actual value in the Machine_IO model
                    machine_io.actual_values = actual_value
                    machine_io.save()

                    # Create a new log entry in Machine_IO_Log if the value has changed
                    Machine_IO_Log.objects.create(
                        machine_io=machine_io,
                        actual_values=actual_value,
                        timestamp=timezone.now()
                    )

                # Prepare the response data, even if there was no change
                response_data.append({
                    'parameter_name': machine_io.parameter_name,
                    'plc_address': plc_address,
                    'actual_value': actual_value
                })

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)