#!/usr/bin/python
import socket
import struct
import binascii


# making the IP header, your_ip and dest_ip are handled by distMeasurement
def ip_header(your_ip, dest_ip):

    destination_address = socket.gethostbyname(dest_ip)

    """ following lines of code are referenced from http://www.binarytides.com/raw-socket-programming-in-python-linux/
    instructions for packing an ip header in python using the struct package, only changes are the TTL, id, source and destination IP address"""
    ip_ihl = 5      # internet header length
    ip_version = 4      # ip version number
    ip_tos = 0
    ip_tot_len = 0  # kernel fills in the correct length
    ip_id = 5036    # packet id number
    ip_frag_off = 0 # only packet, not fragmented
    ip_ttl = 32     # TTL specified in instructions as 32
    ip_proto = socket.IPPROTO_UDP   # UDP receive socket
    ip_check = 0    # kernel will fill checksum
    ip_send_address = socket.inet_aton(your_ip)  # source ip address
    ip_destination_address = socket.inet_aton(destination_address)

    ip_ihl_ver = (ip_version << 4) + ip_ihl # packing in the version before the ihl

    # packing the header all together
    ip_header_out = struct.pack('!BBHHHBBH4s4s', ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto,
                            ip_check, ip_send_address, ip_destination_address)

    return ip_header_out


# Making a UDP header, your_ip and dest_ip are handled by distMeasurement.py
def udp_header():

    #udp header fields, names explain the values
    udp_length = 8       # 1500 - 20 (ip header) - 8 (udp header) = 1476
    udp_checksum = 0        # we're not implementing a checksum, we don't care about the payload
    udp_send_port = 0    # send port
    udp_destination_port = 33434 # destination port (ping port basically)

    # this was created using a byte calculator... just a bunch of copy-paste until I hit 1480
    data = binascii.hexlify(b'hitestingfornumberofhopsversusRTT.pleasereturntosender...FGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNANNEEDFOURTEENMYINITIALSARECYT')

    # format code (!HHHH) for this found on stackoverflow.com/questions/15049143/raw-socket-programming-udp-python
    udp_header_out = struct.pack('!HHHH', udp_send_port, udp_destination_port, udp_length, udp_checksum)
    return udp_header_out + data