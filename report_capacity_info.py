#!/usr/bin/env python3

#
# Script used to write to an InfluxDB database for capacity tracking
#

import datetime
import json
from gather_capacity_info import CapacityInfo
from influxdb import InfluxDBClient

def get_hypervisor_usage():
   cap_info = CapacityInfo()
   return cap_info.get_hypervisor_usage()

def get_cloud_usage():
   cap_info = CapacityInfo()
   return cap_info.get_cloud_usage()


def jsonify_hypervisor_usage(hypervisor_usage):
   timestring = str(datetime.datetime.now())
   write_string = "["
   for hypervisor in hypervisor_usage:
      if '}' in write_string:
         write_string += ','
      write_string +=""" 
   { \"measurement\": \"hypervisor_usage\",
     \"time\": \"%s\",
     \"tags\": {
        \"hypervisor_hostname\": \"%s\"
     },
     \"fields\": {
        \"vcpus\": %d,
        \"vcpus_used\": %d,
        \"memory_mb_used\": %d,
        \"memory_mb\": %d,
        \"local_gb\": %d,
        \"disk_available_least\": %d,
        \"running_vms\": %d,
        \"vcpu_util\": %f,
        \"ram_util\": %f,
        \"disk_util\": %f
     }
   }""" % (str(timestring), 
              str(hypervisor), 
              hypervisor_usage[hypervisor]["vcpus"], 
              hypervisor_usage[hypervisor]["vcpus_used"], 
              hypervisor_usage[hypervisor]["memory_mb_used"], 
              hypervisor_usage[hypervisor]["memory_mb"], 
              hypervisor_usage[hypervisor]["local_gb"], 
              hypervisor_usage[hypervisor]["disk_available_least"], 
              hypervisor_usage[hypervisor]["running_vms"], 
              hypervisor_usage[hypervisor]["vcpu_util"], 
              hypervisor_usage[hypervisor]["ram_util"], 
              hypervisor_usage[hypervisor]["disk_util"])  
   write_string += "\n]"
   return write_string

def write_to_influx(json_payload):
   try:
      influx_client = InfluxDBClient(host='localhost', port=8086)
      influx_client.switch_database('capacity')
      print(json_payload)
      influx_client.write_points(json_payload)
   except Exception as e:
      print(e)

#print(jsonify_hypervisor_usage(get_hypervisor_usage()))
hypervisor_usage = get_hypervisor_usage()
json_payload = jsonify_hypervisor_usage(hypervisor_usage)
write_to_influx(json.loads(json_payload))
