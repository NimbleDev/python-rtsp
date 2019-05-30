## python3 env
__author__ = 'Dengbo'
import sys, socket, os, logging, ssl

from ServerWorker import ServerWorker
class Server:

	def main(self):
		logging.basicConfig(level=logging.DEBUG,
							format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
							datefmt='%a, %d %b %Y %H:%M:%S', filename="rtsp.log", filemode='a')
		try:
			SERVER_PORT = int(sys.argv[1])
		except:
			logging.error('Usage: Server.py Server_port')
		# 生成SSL上下文
		# context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
		# 加载服务器所用证书和私钥
		# context.load_cert_chain('/etc/stunnel/test.pem', '/etc/stunnel/test.key')
		rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		rtspSocket.bind(('', SERVER_PORT))
		logging.info("RTSPserver bind prot: " + str(SERVER_PORT))
		logging.info("RTSP Listing incoming request...")
		rtspSocket.listen(5)

		# Receive client info (address,port) through RTSP/TCP session
		# 将socket打包成SSL socket
		# with context.wrap_socket(rtspSocket, server_side=True) as ssock:
		while True:
			clientInfo = {}
			clientInfo['rtspSocket'] = rtspSocket.accept()   # this accept {SockID,tuple object},tuple object = {clinet_addr,intNum}!!!
			ServerWorker(clientInfo).run()
	def writePid(self):
		pid = str(os.getpid()) + "\n"
		f = open('rtsp.pid', 'w')
		f.write(pid)
		f.close()
# Program Start Point
if __name__ == "__main__":
	(Server()).writePid()
	(Server()).main()


