# coding=utf-8

# some imports
import os
import socket, sys, random, time, argparse
from struct import *

# $1: numero de pacotes
# $2: endereço de origem
# $3: porta de destino

mac_addr = "00:04:23:08:91:dc"
idx=1
def sendPacket(source_ip,dest_ip,port,payload,sock): 

    packet = ""
    # ip header fields
    ip_ihl = 5
    ip_ver = 4
    ip_tos = 0
    ip_tot_len = 0  # kernel will fill the correct total length
    global idx
    idx = idx%65535 + 1   #Id of this packet
    ip_id = idx
    ip_frag_off = 0
    ip_ttl = 64
    ip_proto = socket.IPPROTO_UDP
    ip_check = 0    # kernel will fill the correct checksum
    ip_saddr = socket.inet_aton ( source_ip )   #Spoof the source ip address if you want to
    ip_daddr = socket.inet_aton ( dest_ip )
 
    ip_ihl_ver = (ip_ver << 4) + ip_ihl
 
    # the ! in the pack format string means network order
    ip_header = pack('!BBHHHBBH4s4s' , ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)
 
    # udp header fields
    udp_source = 38388
    udp_dest = port
    udp_length = 8 + len(payload)
    udp_checksum = 0 

    # the ! in the pack format string means network order
    udp_header = pack('!HHHH' , udp_source, udp_dest, udp_length, udp_checksum)
    # final full packet - syn packets dont have any data
    packet = ip_header + udp_header + payload

    r = sock.sendto(packet, (dest_ip , 0 ))
    #print dest_ip


def prod():
    global mac_addr
    parser = argparse.ArgumentParser()
    parser.add_argument("npkt", help="Total number of packets to send.") # we assume one packet per flow
    parser.add_argument("serv_ip", help="Service IP.")
    parser.add_argument("port", help="Destination port.")
    
    args = parser.parse_args()

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        s.setsockopt(socket.SOL_SOCKET, 25, "p4p1" + '\0')
        #s.setsockopt(socket.SOL_SOCKET, IN.SO_BINDTODEVICE, "p4p1" + '\0')
        #s.setsockopt(socket.SOL_SOCKET,IN.SO_BINDTODEVICE, struct.pack("%ds" % (len("eth0")+1,), "eth0"))
        #s.bind('192.168.10.1', 38388)

    except socket.error , msg:
        print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
    
    port = int(args.port)
    duration = 1
    payloadSource = 'v' * (1500 - (8 + 20)) # Ethernet frame is 1500 bytes, ip header takes up 20, udp header takes up another 8

    num_pkts = 0
    for k in range(1, int(args.npkt)+1):
        src_address = args.serv_ip
        i = int((k-1) / 254) + 10
        j = k % 254
        if j == 0:
            j = 254
        if k != 1: 
            cmd = "arp -d " + str(dst_address)
            os.system(cmd)
        dst_address = '172.31.' + str(i) + '.' + str(j)
        cmd2 = "arp -s " + str(dst_address) + " " + str(mac_addr)
        os.system(cmd2)
     

        try:
            while True:
		sendPacket(src_address, dst_address, port, payloadSource[:int(random.expovariate(1.0/duration))], s)
		num_pkts = num_pkts + 1
            	#print ('src=%s dst=%s num=%d' % (src_address, dst_address, num_pkts))
        except:
            import traceback
            traceback.print_exc()
            print('Too bad! %s:%s' % (src_address, int(port)))
    

if __name__ == '__main__':
    prod()

