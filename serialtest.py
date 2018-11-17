#!/usr/bin/python3

import serial
import config
import time
import sys

port = serial.Serial(config.SERIAL_PORT, baudrate=9600)

def read_byte():
	return port.read()

def process_sentence(sentence):
	sender = sentence[1]
	recipient = sentence[2]
	valuetype = sentence[3]
	value = sentence[4]
	checksum = sentence[5]

	if sender in config.SENTENCE_SYSTEM:
		# Only process sentences originating from controller
		# print ("Gut: "+sentence.hex(), flush=True)

		if valuetype in config.TYPE_TEMP_OUTSIDE:
			print ("Outside Temperature: " + str(config.TEMP_LOOKUP[value]) + "°C")
			print (str(time.time())+";OUTSIDE;"+str(config.TEMP_LOOKUP[value]))
		elif valuetype in config.TYPE_TEMP_INSIDE:
			print ("Inside Temperature: " + str(config.TEMP_LOOKUP[value]) + "°C")
			print (str(time.time())+";INSIDE;"+str(config.TEMP_LOOKUP[value]))
		elif valuetype in config.TYPE_TEMP_EXHAUST:
			print ("Exhaust Temperature: " + str(config.TEMP_LOOKUP[value]) + "°C")
			print (str(time.time())+";EXHAUST;"+str(config.TEMP_LOOKUP[value]))
		elif valuetype in config.TYPE_TEMP_INCOMING:
			print ("Incoming Temperature: " + str(config.TEMP_LOOKUP[value]) + "°C")
			print (str(time.time())+";INCOMING;"+str(config.TEMP_LOOKUP[value]))
		elif valuetype in config.TYPE_FANSPEED:
			print ("Fan speed: " + str(value))
			print (str(time.time())+";FANSPEED;"+str(value))


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
