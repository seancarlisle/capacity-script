#!/usr/bin/env python3

#
# Simple class to gather hypervisor and cloud usage for capacity planning
#

import shade
from shade.exc import OpenStackCloudException
import datetime

class CapacityInfo():
  
  def __init__(self):
    try:
       self.cloud = shade.openstack_cloud(cloud='default')
    except OpenStackCloudException as e:
       print(e)

  def get_hypervisor_usage(self):
    ''' Returns a dictionary of dictionaries for further data manipulation.
        Returns fields are as follows:
          vcpus 
          vcpus_used 
          memory_mb_used 
          memory_mb 
          local_gb 
          disk_available_least 
          running_vms'''
    try:
       hypervisors = self.cloud.list_hypervisors()
    except OpenStackCloudException as e:
       print(e)
      
    hypervisor_usage = {}
    for hypervisor in hypervisors:
      hypervisor_usage[hypervisor["hypervisor_hostname"]] = { 
         "vcpus": hypervisor["vcpus"], 
         "vcpus_used": hypervisor["vcpus_used"],
         "memory_mb_used": hypervisor["memory_mb_used"],
         "memory_mb": hypervisor["memory_mb"],
         "local_gb": hypervisor["local_gb"],
         "disk_available_least": hypervisor["disk_available_least"],
         "running_vms": hypervisor["running_vms"], 
         "vcpu_util": self.calculate_usage(hypervisor["vcpus_used"], hypervisor["vcpus"]),
         "ram_util": self.calculate_usage(hypervisor["memory_mb_used"], hypervisor["memory_mb"]),
         "disk_util": self.calculate_usage(hypervisor["local_gb"] - hypervisor["disk_available_least"], hypervisor["local_gb"])}

    return hypervisor_usage

  def calculate_usage(self, used, total):
    return float(used) / float(total)

  def get_cloud_usage(self):
    hypervisor_usage = self.get_hypervisor_usage()

    #create a shallow copy to make our lives easier
    cloud_usage = hypervisor_usage[next(iter(hypervisor_usage))].copy()

    for hypervisor in hypervisor_usage:
       cloud_usage["vcpus"] += int(hypervisor_usage[hypervisor]["vcpus"])
       cloud_usage["vcpus_used"] += int(hypervisor_usage[hypervisor]["vcpus_used"])
       cloud_usage["memory_mb_used"] += int(hypervisor_usage[hypervisor]["memory_mb_used"])
       cloud_usage["memory_mb"] += int(hypervisor_usage[hypervisor]["memory_mb"])
       cloud_usage["local_gb"] += int(hypervisor_usage[hypervisor]["local_gb"])
       cloud_usage["disk_available_least"] += int(hypervisor_usage[hypervisor]["disk_available_least"])
       cloud_usage["running_vms"] += int(hypervisor_usage[hypervisor]["running_vms"])
       
    cloud_usage["vcpu_util"] = self.calculate_usage(cloud_usage["vcpus_used"], cloud_usage["vcpus"]),
    cloud_usage["ram_util"] = self.calculate_usage(cloud_usage["memory_mb_used"], cloud_usage["memory_mb"]),
    cloud_usage["disk_util"] = self.calculate_usage(cloud_usage["local_gb"] - cloud_usage["disk_available_least"], cloud_usage["local_gb"])

    return cloud_usage
