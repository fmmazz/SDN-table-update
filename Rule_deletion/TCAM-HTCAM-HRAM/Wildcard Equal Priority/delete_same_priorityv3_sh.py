# coding=utf-8


import sys
import os
import time
import os.path
import socket
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, HANDSHAKE_DISPATCHER 
from ryu.controller.handler import set_ev_cls
from ryu.controller.handler import set_ev_handler
from ryu.ofproto import ofproto_v1_3 
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ipv4
from ryu.lib.packet import udp
from ryu.lib.packet import arp
from ryu.lib.packet import ether_types



initial_rules = 1950
measure_rules = 1
counter = 1
initial_priority = 1000
measure_priority = 10
ipv4_src = "192.168.10.1"
ipv4_dst = 0
ipv4_dst_first = ""
udp_port_dst = 30000
burst = {}


class FirstExperiment(app_manager.RyuApp):
	OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION] 

	def __init__(self, *args, **kwargs):
		super(FirstExperiment, self).__init__( *args, **kwargs)
		self.mac_to_port = {}
		print 'Initializing experiment!'


	def send_flow_mod(self, datapath):
		
		global ipv4_src
		global ipv4_dst
		global ipv4_dst_first
		global burst
		global initial_priority

		ofp = datapath.ofproto
		ofp_parser = datapath.ofproto_parser

		for k in xrange(1,2001):
			cookie = 0
			cookie_mask = k
			table_id = 0
			idle_timeout = hard_timeout = 0
			priority = 1
			buffer_id = ofp.OFP_NO_BUFFER
			match = ofp_parser.OFPMatch(eth_type=0x800)
			actions = [ofp_parser.OFPActionOutput(ofp.OFPP_NORMAL, 6)]
			inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
			req = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
						table_id, ofp.OFPFC_DELETE,
						idle_timeout, hard_timeout,
						priority, buffer_id,
						ofp.OFPP_ANY, ofp.OFPG_ANY,
						ofp.OFPFF_SEND_FLOW_REM,
						match, inst)
			datapath.send_msg(req)

		time.sleep(10)

		print 'Rules deleted!'

		cookie_mask = initial_rules +1
		match = ofp_parser.OFPMatch(in_port=1)
		actions = [ofp_parser.OFPActionOutput(port = 3)]
		inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
							 actions)]
		mod = ofp_parser.OFPFlowMod(datapath=datapath, cookie_mask=cookie_mask, priority=1,
						match=match, instructions=inst)
		datapath.send_msg(mod)

		if initial_rules != 0:
			for k in xrange(initial_rules, 0, -1):
	
				cookie_mask = k
				i = int(k/256) + 10
				j = k % 256
				dst = '172.31.' + str(i) + '.' + str(j)
				if k == initial_rules:
					ipv4_dst_first = dst
				match = ofp_parser.OFPMatch(eth_type = 0x800, ipv4_src=ipv4_src, ipv4_dst= dst)
				actions = [ofp_parser.OFPActionOutput(port = 6)]
				inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
				req = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
								table_id, ofp.OFPFC_ADD,
								idle_timeout, hard_timeout,
								initial_priority, buffer_id,
								ofp.OFPP_ANY, ofp.OFPG_ANY,
								ofp.OFPFF_SEND_FLOW_REM,
								match, inst)    
				datapath.send_msg(req)		
				ipv4_dst = dst
			
		time.sleep(30)		


		cmd1 = 'sudo ./simplesniffer p3p1 ' + str(measure_rules) + ' 0 ' + '&'
		cmd2 = 'python pktgen-v4.py 1 ' + str (ipv4_src) + ' 45678 &'

		os.system(cmd1)
		time.sleep(1)
		os.system(cmd2)
		time.sleep(1)	

		if initial_rules != 0:
			for k in xrange(initial_rules, 0, -1):
	
				cookie_mask = k
				i = int(k/256) + 10
				j = k % 256
				dst = '172.31.' + str(i) + '.' + str(j)
				if k == initial_rules:
					ipv4_dst_first = dst
				match = ofp_parser.OFPMatch(eth_type = 0x800, ipv4_src=ipv4_src, ipv4_dst= dst)
				actions = [ofp_parser.OFPActionOutput(port = 6)]
				inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
				req = ofp_parser.OFPFlowMod(datapath, cookie, cookie_mask,
								table_id, ofp.OFPFC_DELETE,
								idle_timeout, hard_timeout,
								initial_priority, buffer_id,
								ofp.OFPP_ANY, ofp.OFPG_ANY,
								ofp.OFPFF_SEND_FLOW_REM,
								match, inst)    
				datapath.send_msg(req)
				if k == initial_rules:
					burst[ipv4_dst_first] = time.time()

		time.sleep(20)
		
		self.end_measurement()
	
	def end_measurement(self):

		global burst
		global ipv4_dst
		global ipv4_dst_first
		print 'INFO: flow mod measure finished...  Generating time log'
		print ipv4_dst
		ipv4_dst=ipv4_dst[:-1]
		w = open('Modify' + str(initial_rules) + '.txt','a')
		for k in xrange(1,measure_rules +1):
			d = ipv4_dst_first
			print str(burst[ipv4_dst_first]) + " " + d
			w.write('dst: %s sec: %f usec: %f\n' %(d, int(burst[d]), (burst[d] - int(burst[d])) * 1000000 ))
		w.close()
		print 'Time log generated. Finishing...'
		sys.exit()
	

	@set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER) 
	def switch_features_handler(self, ev): 
		print 'Handling switch features'

		datapath = ev.msg.datapath
		ofp= datapath.ofproto
		ofp_parser = datapath.ofproto_parser

		self.send_flow_mod(datapath)

