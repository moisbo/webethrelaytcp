#!/usr/bin/env python
#Moises Sacal
#Example of web app controller for the
#ETH8020 - 20 Relays at 16A, 8 Analogue Inputs

import time
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import sqlite3
import logging
import os
import sys
import socket
import json
from struct import *

#This application details
WEB_PORT=4000
LOG_FILE='flie.log'

#Ethernet relay board details
TCP_IP = '131.181.46.226'
TCP_PORT = 17494
BUFFER_SIZE = 3072

############################################################################################################
#Tornado Web Server
# Tornado options note: Set --logging=none to see all Tornado logging messages

# Monkey Patch so APY is happy with stock Tornado
tornado.ioloop.IOLoop.timefunc = time.time
# Monkey Patch so Tornado does NOT autoreload the python modules in debug mode,
# because it messes up snapconnect, and we really just want JS/Template reloads.

import tornado.autoreload
tornado.autoreload.start = lambda x=None, y=None: (x,y)
from tornado.options import define, options

define("port", default=WEB_PORT, help="run on the given port", type=int)

log = logging.getLogger('main')

# Local system overrides for development/test
try:
    from local_overrides import *
except:
    pass

def _execute(query):
        connection = sqlite3.connect(DB_PATH)
        cursorobj = connection.cursor()
        try:
                cursorobj.execute(query)
                result = cursorobj.fetchall()
                connection.commit()
                id = cursorobj.lastrowid
        except Exception:
                raise
        connection.close()
        return (result, id)

#Your Message handlers for the web app
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/sendMessage",SendMessageHandler)
                    ]
        settings = dict(
            cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            template_path=os.path.join(os.path.dirname(sys.argv[0]), "templates"),
            static_path=os.path.join(os.path.dirname(sys.argv[0]), "static"),
            xsrf_cookies=True,
            autoescape=None,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

#Loads first page
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.xsrf_token
        self.render("index.html")

#Message Definition Class
class SendMessageHandler(tornado.web.RequestHandler):
   @tornado.web.asynchronous
   def post(self):
        error = False
        response = ''
        m1 = self.get_argument("m1")
        m2 = self.get_argument("m2")
        m3 = self.get_argument("m3")
        #first command is password ff since its disabled
        thmsg = '\xff'+ m1.decode('hex') + m2.decode('hex') + m3.decode('hex')
        #Example command: http://www.robot-electronics.co.uk/htm/eth8020tech.htm
        #0x20 - turn the relay on command
        #0x03 - relay 3
        #0x32 (50) - 5 seconds (50 * 100ms)
        #Board will return 0 for success, 1 for failure
        #Note - All bytes in a command must be sent in one TCP/IP packet.
        #thmsg = '\xff\x20\x03\x32'

        try:
           s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           s.connect((TCP_IP, TCP_PORT))
           s.send(thmsg)
           messg = s.recv(BUFFER_SIZE)
           response = messg
           s.close()
        except Exception, e:
            error = True
            response = str(e)
            pass
        self.finish({'data': response.encode('hex'), 'error':error})

############################################################################################################

def main():
    global webApp
    import logging

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s %(levelname)-8s %(name)-8s %(message)s')
    #logging.basicConfig(filename=LOGFILE, format='%(asctime)-15s %(levelname)-8s %(name)-8s %(message)s', filemode='a', level=logging.WARNING)
    log.info("***** Begin Console Log *****")

    tornado.options.parse_command_line()
    tornado.options.logging = logging.DEBUG
    log.setLevel(logging.DEBUG)

    webApp = Application()
    webApp.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
