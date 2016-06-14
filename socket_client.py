import socket, select, string, sys, time
from banco import log

class SocketClient(object):

	HOST = 'localhost'
	PORT = 8002

	def message(self):
		sys.stdout.write('# ')
		sys.stdout.flush()

	def connect(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.settimeout(2)

		try:
			self.s.connect((self.HOST, self.PORT))
		except:
			print 'Erro ao tentar conectar.'
			sys.exit()

		print 'Conectado com sucesso.'
		self.message()

		while 1:
			self.broadcast()

	def broadcast(self, message=None):
		socket_list = [sys.stdin, self.s]
		read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

		for sock in read_sockets:
			if sock == self.s:
				data = sock.recv(4096)
				if not data:
					print '\nConexo com o servidor perdida'
					sys.exit()
				else :
					sys.stdout.write(data)
					self.message()

			elif message is not None:
				self.s.send(message)
				self.message()
			else:
				message = sys.stdin.readline()
				inicio = time.time()
				self.s.send(message)
				self.message()
				fim = time.time()
				total = (fim-inicio)
				log('socket_client', total)
				print '\nTempo: %f' % total


sc = SocketClient()
sc.connect()