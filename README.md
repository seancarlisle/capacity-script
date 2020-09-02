Python class and functions to gather capacity info from OpenStack and write it to InfluxDB.

Setup:
- Make sure you have python3-venv and python3 installed.
- Create a new python3 virtual environment
  - python3 -m venv my-venv
- Activate the new venv and install the needed things
  - cd my-venv
  - source bin/activate
  - pip3 --isolated install wheel
  - pip3 --isolated install shade
  - pip3 --isolated install influxdb

Requirements:
- A locally running InfluxDB server
- A database in InfluxDB named "capacity"
- A cloud.yaml file in /root/.config/openstack

Running the script:
- The script is designed to write to an existing InfluxDB database.
- source bin/activate
- python3 /path/to/report_capacity_info.py
