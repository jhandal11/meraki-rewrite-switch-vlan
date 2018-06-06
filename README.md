# SourceRewriteVLAN.py
Written by Nathan Wiens (nathan@wiens.co)

This script will look for devices with static IP addresses on Meraki switch networks that have been assigned to the wrong VLAN, and dynamically move them to the correct one. Because Meraki switches use ARP to identify a client, we can detect the IP address assigned to a client even if it's in the wrong VLAN

To set up the script, modify the meraki_info.py file with an API key, Org ID, network tag (to scope the script to a subset of networks).
ip_address_string is used to match the subnet of the client to be moved from source_vlan to dest_vlan.
uplink1 and uplink2 variables are used to identify ports that should never be overwritted (such as uplink or trunk ports). Be sure to include all trunk ports or multi-access ports to prevent them from being overwritten
