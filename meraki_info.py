api_key = 'XXXXXX'
base_url = 'https://dashboard.meraki.com/api/v0'
snmp_port = 16100
org_id = 000000 # 

### SwitchRewriteVLAN Settings
# If a client matches the ip_address_string and the VLAN matches source_vlan,
# this script will change the port VLAN to dest_VLAN
###

tag = 'switchtest' #Network tag to match (for scoping)
ip_address_string = '172.' #String to match from clients IP address
source_vlan = '5' #VLAN to move devices from
dest_vlan = '6' #VLAN to move devices to
uplink1 = '1' #Uplink port number to protect (will not rewrite)
uplink2 = '2' #Uplink port number to protect (will not rewrite)