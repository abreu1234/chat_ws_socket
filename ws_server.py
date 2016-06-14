import tornado.ioloop
import tornado.web
import tornado.websocket
import time
import json
from banco import log

clients = []

class IndexHandler(tornado.web.RequestHandler):
  @tornado.web.asynchronous
  def get(request):
    request.render("index.html")

class WebSocketChatHandler(tornado.websocket.WebSocketHandler):
  def check_origin(self, origin):
    return True

  def open(self, *args):
    print("open", "WebSocketChatHandler")
    clients.append(self)

  def on_message(self, message):        
    print message
    message_json = json.loads(message)

    if message_json['type'] == 'message':
      inicio=time.time()

      for client in clients:
    		client.write_message(message)

      fim=time.time()
      log('ws_server', (fim-inicio))
      print '\nTempo: %f' % (fim-inicio)
    elif message_json['type'] == 'log':
      log('ws_client', message_json['time'])
        
  def on_close(self):
  	clients.remove(self)

app = tornado.web.Application([(r'/chat', WebSocketChatHandler), (r'/', IndexHandler)])

app.listen(8080)
tornado.ioloop.IOLoop.instance().start()