#!/usr/bin/python3

import serial
import config
import time

port = serial.Serial(config.SERIAL_PORT, baudrate=9600)

def read_byte():
	return port.read()

def process_measurement(identifier, value):
	iso = time.ctime()
	data = [
	{
		"measurement": config.MEASUREMENT_ID,
			"tags": {
				"location": config.LOCATION_ID
			},
			"time": iso,
			"fields": {
				identifier: value
			}
	}	
	]
	print (data)

def process_sentence(sentence):
	sender = sentence[1]
	recipient = sentence[2]
	valuetype = sentence[3]
	value = sentence[4]
	checksum = sentence[5]

	if sender in config.SENTENCE_SYSTEM:
		# Only process sentences originating from controller
		# print ("Gut: "+sentence.hex(), flush=True)

		if valuetype in config.TEMP_IDENTIFIERS:
			process_measurement(config.TEMP_IDENTIFIERS[valuetype], config.TEMP_LOOKUP[value])
			#print (str(time.ctime())+";"+config.TEMP_IDENTIFIERS[valuetype]+";"+str(config.TEMP_LOOKUP[value]))
		elif valuetype == config.TYPE_FANSPEED:
			process_measurement("FANSPEED", value)
			#print (str(time.ctime())+";FANSPEED;"+str(value))


sentence = bytearray()

while True:

	sentence += read_byte()
	length = len(sentence)

	if (
		(length == 1 and (sentence[-1] not in config.SENTENCE_START)) or
		((length == 2 or length == 3) and sentence[-1] not in config.SENTENCE_VALID_PEERS)
	   ):
		# print ("Ignored: "+sentence.hex(), flush=True)
		# TODO: Handle bytes. Eventually valid values are there with an offset, do not just throw them away
		sentence = bytearray()
	elif length >= 6:
		# sentence valid: correct start byte, syntactically correct sender and recipient
		process_sentence(sentence)
		sentence = bytearray()
