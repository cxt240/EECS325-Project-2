#!/usr/bin/python

import socket
import time
import select
import struct
import packet



def main(): # reads each line of targets.txt and calls my_ping for each website
    file = open("targets.txt")
    websites = file.read().splitlines()
    map(my_ping(), websites)
    return


def my_ping(website):
    my_ip = socket.gethostbyname_ex(socket.gethostname())[2][0]

    x = 0

    print("getting ttl and rtt from: " + website)
    for x in range(0, 2):
        destination_ip = socket.gethostbyname(website)  # getting the destination IP address

        print("creating sending and receiving sockets for " + website)
        # creating the send socket
        sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.getprotobyname('udp'))  # creating the udp transmitting socket
        # sender.bind(('', 33434))

        # creating receiving sockets
        receiver = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
        receiver.bind(("", 33434))  # ports 33434 -33523 are the traceroute/ping ports for tcp/udp

        # creating the send packet
        this_ip = packet.ip_header(my_ip, destination_ip)  # IP header
        send_packet = this_ip + packet.udp_header()

        print("created packet and sending to " + website)

        # sending the packet and starting the timer for transmission time
        sender.sendto(send_packet, (website, 33434))
        start = time.time()  # start timer
        print("packet sent to " + website)

        receiving = select.select([receiver], [], []) #selecting the receiving socket to watch
        print("setting a select")
        if(receiving[0]):
            print("receiving from " + website)
            raw_data, data = receiver.recvfrom(512)
            receive_time = time.time()
            response_time = (receive_time - start) * 1000
            data_array = raw_data

            # unpacking the bytes 28 to 48 of the header, IP information... First 20 bytes are the return IP header
            # followed by the 8 bytes that are ICMP error messages
            # followed by the "original packet" fragment, so the first 20 bytes of the original are the IP header
            # which should be able to be used to get the packetID and remaining TTL
            # saving the unpacked format as a list
            response = struct.unpack('!BBHHHBBH4s4s', data_array[28:48])
            print(response)

            # packet id should be the same as the original one in the header
            # in the original packing, the 3rd element was the packet id, 5th element was the TTL
            if True or response[3] == 5036:  # packet_id is the same
                hops =  response[5]-32  # calculating hops
                print(str(response_time) + "milliseconds in " + str(hops) + " hops")
                return

        # close send and receive sockets
        sender.close()
        receiver.close()
        print("Packet timed out trying again " + str(3 - x) + "times")
    return

if __name__ == "__main__":
    main()
