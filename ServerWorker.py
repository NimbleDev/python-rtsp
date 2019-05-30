__author__ = 'Dengbo'

import time
import threading
from Database import Database
from Log import Log


class ServerWorker:
	OPTIONS = 'OPTIONS'
	DESCRIBE = 'DESCRIBE'

	clientInfo = {}
	logging = {}
	t = {}

	def __init__(self, clientInfo):
		self.clientInfo = clientInfo
		log = Log()
		self.logging = log.GetLogging()

	def run(self):
		self.clientInfo['event'] = threading.Event()
		self.t = threading.Thread(target=self.recvRtspRequest)
		self.t.start()
		self.t.join(2)
		# print('rtsp runing')
	def recvRtspRequest(self):
		"""Receive RTSP request from the client."""
		connSocket = self.clientInfo['rtspSocket'][0]
		while True:
			data = connSocket.recv(1024) .decode("utf-8") ###
			if data:
				# print ('-'*60 + "\nData received:\n" + '-'*60)
				# rtsp request is text
				# convert bytes to string 
				# data = data.decode("utf-8")
				result = self.processRtspRequest(data)
				if result:
					print('break connSocket')
					break
			elif len(data) < 1:
				print('len = 0')
				break
		self.clientInfo['event'].set()
		connSocket.close()
		self.logging.info("server success response")
	def processRtspRequest(self, data):
		"""Process RTSP request sent from the client."""
		# Get the request type
		print("Data received: data ==> ", data)
		# logging.info("Data received: data ==> " + data)
		request = data.split('\n')
		line1 = request[0].split(' ')
		# print("line1:", line1)
		requestType = line1[0]
		# Get the media file name
		#filename = line1[1]
		# Get the RTSP sequence number
		seq = request[3].split(' ')
		# print('-'*60 + "\nrequest: " + str(request) + "\n" + '-'*60)
		seq = (seq[1] if(len(seq) > 1) else '0')
		print('-' * 60 + "\nseq :" + str(seq) + "\n" + '-' * 60)
		# Process OPTION request
		if requestType == self.OPTIONS:
			self.logging.info("OPTION Request received")
			# print("OPTION Request received\n")
			nowDate = time.strftime("%a %b %d %Y %H:%M:%S", time.localtime())
			reply = 'RTSP/1.0 200 OK\r\nCSeq: ' + seq + 'Date: ' +  nowDate + ' GMT + 8\r\nPublic: OPTIONS, DESCRIBE, SETUP, TEARDOWN, PLAY, PAUSE, GET_PARAMETER, SET_PARAMETER\r\n\r\n'
			print(reply)
			# logging.info("server send: " + reply)
			reply = reply.encode("utf-8")
			connSocket = self.clientInfo['rtspSocket'][0]
			connSocket.send(reply)
			return False
		# -> REDIRECT 301
		elif requestType == self.DESCRIBE:
			self.logging.info("DESCRIBE Request received")
			print("DESCRIBE Request received\n")
			if len(line1[1].split('/')) > 3 :
				camera_stream_id = line1[1].split('/')[3]
				self.logging.info("camera_stream_id: " + camera_stream_id)
				db = Database()
				sql = "select local_rtsp from camera_stream where id = %s"
				param = camera_stream_id
				uri = db.self_sql(sql, param)
				if uri == -1:
					self.logging.error('mysql select error...')
					return True
				reply = 'RTSP/1.0 301 Moved\r\nCSeq: ' + seq + '\r\nLocation: ' + uri + '\r\n\r\n'
				# logging.info("server send: " + reply)
				print(reply)
				reply = reply.encode("utf-8")
				connSocket = self.clientInfo['rtspSocket'][0]
				connSocket.send(reply)
				self.logging.info("--> Redirect 301 Location: " + uri)
			else:
				self.logging.error("Invalid camera uid")
			return True
		else:
			return True
