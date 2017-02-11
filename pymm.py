#!/usr/bin/env python

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.factory import ClientDecoder
from optparse import OptionParser
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import sys

#---------------------------------------------------------------------------# 
# Logging
#---------------------------------------------------------------------------# 

import logging
logging.basicConfig()
log = logging.getLogger()

#---------------------------------------------------------------------------# 
# Options
#---------------------------------------------------------------------------# 

def get_options():
	''' A helper method to parse the command line options

	:returns: The options manager
	'''
	parser = OptionParser()

	parser.add_option("-o", "--output",
		help="The resulting output file for the scrape",
		dest="output", default="datastore.pickle")

	parser.add_option("-p", "--port",
		help="The port to connect to", type='int',
		dest="port", default=502)

	parser.add_option("-a", "--address",
		help="The device-address to connect to", type='int',
		dest="address", default=1)

	parser.add_option("-s", "--server",
		help="The server to scrape",
		dest="host", default="127.0.0.1")

	parser.add_option("-r", "--range",
		help="The address range to scan",
		dest="query", default="0:10")

	parser.add_option("-v", "--verbose",
		help="Enable verbose output",
		action="store_true", dest="debug", default=False)

	parser.add_option("-f", "--format",
		help="Formatting the output",
		dest="format", default="int16")

	(opt, arg) = parser.parse_args()
	return opt


#---------------------------------------------------------------------------# 
# Main
#---------------------------------------------------------------------------# 

options = get_options()

if options.debug:
	try:
		log.setLevel(logging.DEBUG)
		logging.basicConfig()
	except Exception, ex:
		print "Logging is not supported on this system"


#---------------------------------------------------------------------------# 
# Request
#---------------------------------------------------------------------------# 

# split the query into a starting and ending range
query = [int(p) for p in options.query.split(':')]

try:  
	log.debug("Starting the client")
	client = ModbusClient(options.host, options.port)
	client.connect()

	log.debug("Reading Registers")
	rr = client.read_holding_registers(query[0], query[1]-query[0]+1)

#---------------------------------------------------------------------------# 
# Test
#---------------------------------------------------------------------------# 

	#Test for Modbus Error Code
	if rr.function_code > 0x80:
	
		log.debug("Modbus Error")
		print rr
	
	else:	

#---------------------------------------------------------------------------# 
# Output
#---------------------------------------------------------------------------# 

		log.debug("Print values")
		print '-' * 60
		
		if options.format == "int16":
			log.debug("Print Integer16 values")

			for i in range(0,query[1]-query[0]+1):
				RegText = 'Register ' + str(query[0]+i) + ':\t'
				RawText = '\tRaw: ' + '0x%04X' % rr.registers[i]
				
				print  RegText, rr.registers[i], RawText
		
		elif options.format == "float32":	
			log.debug("Print Float32 values")
		
			decoder = BinaryPayloadDecoder.fromRegisters(rr.registers, endian=Endian.Big)
			for i in range(0,len(decoder._payload)/4):
				
				#Info-Texts
				RegText = 'Register ' + str(query[0]+i*2) + ' + ' + str(query[0]+i*2+1) + ' :\t'
				RawText = '\t Raw: ' + '0x%04X' % rr.registers[i*2] + ' ' + '0x%04X' % rr.registers[i*2+1]
				
				print RegText, "%10.4f" % decoder.decode_32bit_float(), RawText 
		

		print '-' * 60 

except Exception, ex:
	print ex  



#---------------------------------------------------------------------------# 
# Close 
#---------------------------------------------------------------------------# 
log.debug("Close Connection")
client.close()



	# ['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_endian', '_payload', '_pointer', 'decode_16bit_int', 'decode_16bit_uint', 'decode_32bit_float', 'decode_32bit_int', 'decode_32bit_uint', 'decode_64bit_float', 'decode_64bit_int', 'decode_64bit_uint', 'decode_8bit_int', 'decode_8bit_uint', 'decode_bits', 'decode_string', 'fromCoils', 'fromRegisters', 'reset']


