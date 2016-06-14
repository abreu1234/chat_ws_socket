import socket, select, time
from banco import log

class SocketServer:

	CONNECTION_LIST = []
	RECV_BUFFER = 4096
	PORT = 8002
	server_socket = None

	def socketStart(self):
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_socket.bind(("0.0.0.0", self.PORT))
		self.server_socket.listen(10)

		self.CONNECTION_LIST.append(self.server_socket)
		print "Servidor socket iniciado na porta: " + str(self.PORT)

		while 1:
			read_sockets,write_sockets,error_sockets = select.select(self.CONNECTION_LIST,[],[])

			for sock in read_sockets:
				#Nova conexao
				if sock == self.server_socket:
					sockfd, addr = self.server_socket.accept()
					self.CONNECTION_LIST.append(sockfd)
					print "(%s, %s) se conectou" % addr
					 
					self.sendMessage(sockfd, "[%s:%s] entrou na sala\n" % addr)

				else:
					#Envia mensagem
					try:
						data = sock.recv(self.RECV_BUFFER)
						if data:
							inicio = time.time()
							self.sendMessage(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)
							fim = time.time()
							total = (fim-inicio)
							log('socket_server', total)
							print '\nTempo: %f' % (fim-inicio)

					except:
						self.sendMessage(sock, "(%s, %s) saiu" % addr)
						print "(%s, %s) se desconectou" % addr
						sock.close()
						self.CONNECTION_LIST.remove(sock)
						continue

	def socketClose(self):
		self.server_socket.close()

	def sendMessage(self, sock, message):
		for socket in self.CONNECTION_LIST:
			if socket != self.server_socket and socket != sock :
				try :
					socket.send(message)
				except :
					# broken socket connection may be, chat client pressed ctrl+c for example
					socket.close()
					self.CONNECTION_LIST.remove(socket)

ss = SocketServer()
ss.socketStart()
ss.socketClose()