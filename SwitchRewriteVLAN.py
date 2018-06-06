### SwitchRewriteVLAN.py
# If a client matches the ip_address_string and the VLAN matches source_vlan,
# this script will change the port VLAN to dest_VLAN
# 
# Written by Nathan Wiens (nathan@wiens.co)
###

import json
import os
import sys
import time
import meraki_info
import merakiapi
import requests

api_key = meraki_info.api_key
org_id = meraki_info.org_id
base_url = meraki_info.base_url
tag = meraki_info.tag

net_id_list = []  # create a blank list
device_id_list = []  # create a blank list

per_net_list = merakiapi.getnetworklist(api_key,org_id)
for row in per_net_list:
	# For each 'row' of JSON in per_net_list, append to network list
	for key,value in row.items():
		# print "k,v is %s,%s" % (key,value) # example
		if key == 'name':
			net_name = value
		elif key == 'id':
			net_id = value
		elif key == 'tags':
			net_tags = value
		else:
			continue
	if tag in net_tags:
		net_id_list.append(net_id)

print ("NETWORKS TO MODIFY")
print (net_id_list)

for net in net_id_list:
	per_net_devices = merakiapi.getnetworkdevices(api_key,net)
	for d in per_net_devices:
		for key,value in d.items():
			if key == 'name':
				device_name = str(value)
			elif key == 'serial':
				device_serial = str(value)
			elif key == 'model':
				device_model = str(value)
			else:
				continue
		# For combined networks, only look at MX
		if 'MS' in device_model:
			device_id_list.append(device_serial)

print ("SWITCHES TO MODIFY")
print (device_id_list)

for dev in device_id_list:
	switch_clients = merakiapi.getclients(api_key,dev)
	#print (switch_clients)
	for c in switch_clients:
		for key,value in c.items():
			if key == 'switchport':
				c_port = str(value)
			elif key == 'ip':
				c_ip = str(value)
			elif key == 'vlan':
				c_vlan = str(value)
			elif key == 'dhcpHostname':
				c_name = str(value)
			else:
				continue
		if meraki_info.ip_address_string in c_ip and c_vlan == meraki_info.source_vlan:
			if c_port == meraki_info.uplink1 or c_port == meraki_info.uplink2: # SPECIFY UPLINK PORTS TO PROTECT
				print ("UPLINK PORT %s FOR CLIENT %s, SKIPPING..." % (c_port, c_name))
			else:
				print ("MOVING CLIENT %s TO VLAN %s ON SWITCH %s PORT %s" % (c_name, meraki_info.dest_vlan, dev, c_port)) 
				swport = merakiapi.getswitchportdetail(api_key, dev, c_port)
				print (swport)
				swport['vlan'] = meraki_info.dest_vlan
				#print (swport)
				print(merakiapi.updateswitchport (api_key, dev, swport['number'], swport['name'], swport['tags'], True, porttype=swport['type'], vlan=swport['vlan'], voicevlan=swport['voiceVlan'], allowedvlans=swport['allowedVlans'], poe=True, isolation=swport['isolationEnabled'], rstp=swport['rstpEnabled'], stpguard=swport['stpGuard'], accesspolicynum=swport['accessPolicyNumber']))
				swport = merakiapi.getswitchportdetail(api_key, dev, c_port)
				#print (swport)
                
