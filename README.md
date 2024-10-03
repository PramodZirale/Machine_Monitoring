# Machine Monitoring System

This is a Django-based Machine Monitoring System for logging and retrieving machine input/output (I/O) data. The system interfaces with Mitsubishi PLCs to read actual values and logs changes. It also provides a web-based interface for managing machine data, PLC configurations, and viewing logs through REST APIs.

## Features

- **PLC Communication:** Connect to Mitsubishi PLCs using `pymcprotocol` to read I/O data.
- **Machine I/O Logging:** Log changes to machine I/O data in the `Machine_IO_Log` model.
- **Dynamic PLC Configuration:** PLC IP address and port can be configured via the Django admin panel.
- **REST APIs:** Provides APIs for fetching machine data, logs, and triggering PLC value updates.
- **Admin Panel:** Manage machine I/O, view logs, and clear log records with a single click from the admin panel.

## Key Models

1. **Machine_IO:** Represents machine I/O data including parameters, PLC address, ranges, and actual values.
2. **Machine_IO_Log:** Stores historical logs of changes to I/O data, including timestamps.
3. **PLCConfig:** Stores dynamic PLC connection information (IP address and port).

## Key APIs

1. **Machine I/O List and Create API:** 
   - `GET /api/machine_io/` - List all machine I/O data, sorted by `parameter_name`.
   - `POST /api/machine_io/` - Create a new machine I/O entry.

2. **Machine I/O Retrieve, Update, and Delete API:** 
   - `GET /api/machine_io/<parameter_name>/` - Retrieve a specific machine I/O record.
   - `PUT /api/machine_io/<parameter_name>/` - Update a machine I/O record.
   - `DELETE /api/machine_io/<parameter_name>/` - Delete a machine I/O record.

3. **Machine I/O Logs (Top 10) API:** 
   - `GET /api/get/machine_io/top10/` - Retrieve the top 10 log entries for each machine I/O parameter, sorted by timestamp.

4. **Update PLC Values API:** 
   - `GET /api/get/machine_io/update_plc_values/` - Fetch the current values from the PLC, update `Machine_IO`, and log changes if necessary. This API retrieves dynamic PLC IP and port configuration from the `PLCConfig` model.

## Admin Panel

- **Machine I/O Management:** Add, edit, and delete machine I/O entries from the Django admin interface.
- **PLC Configuration:** Configure PLC IP and port dynamically via the `PLCConfig` model.
- **Log Management:** View and manage `Machine_IO_Log` entries. A custom action is available to clear all log entries using the "Flush all log records" button.

## Installation

### Prerequisites

- Python 3.6+
- Django 3.x+
- `pymcprotocol` for Mitsubishi PLC communication
- PostgreSQL or SQLite for database management

### Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/Machine_Monitoring.git
   cd Machine_Monitoring

# Install the Dependencies:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run Database Migrations:
python manage.py migrate

# Create a Superuser:
python manage.py createsuperuser

# Run server
python manage.py runserver
