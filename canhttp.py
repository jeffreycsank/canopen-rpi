#!/usr/bin/python3
# TODO: support multiple CAN busses.
# Due to PCB layout error, can0 is connected to bus 1 and can1 to bus 0
# so, telemetry is hard-coded with receiving on can0, although can1 is used
import CAN
from array import array
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from os import path
import signal
from socketserver import ThreadingMixIn
import socket
import struct
import sys
from time import sleep
import traceback
from urllib.parse import parse_qs, urlparse

DEFAULT_CAN_DEVICE = "can1"
WWW_DIR = path.dirname(path.realpath(__file__))

def sigterm_handler(signum, frame):
    sys.exit()

def parse_request(request):
    id = request.get('id')
    if id == None:
      raise BadRequest("id not specified")
    id = int(id[0])
    data = request.get('data[]') # POST
    if data == None:
        data = request.get('data') # GET
        if data == None:
            #raise BadRequest("data not specified")
            data = [] # parse_url removes data field if empty array
        else:
            data = data[0].strip('[]').split(',')
    if len(data) == 1:
      if data[0] == '':
        data = []
    data = list(map(int, data))
    frame = CAN.Frame(id, data)
    return frame

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class BadRequest(BaseException):
    def __init__(self, arg):
        self.args = arg

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)

        try:
            # Command
            if parsed_path.query != '':
                frame = parse_request(parse_qs(parsed_path.query))
                bus = CAN.Bus(DEFAULT_CAN_DEVICE)
                bus.send(frame)
                self.send_response(204);
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers();
                return

            # Telemetry
            if parsed_path.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/event-stream')
                self.send_header('Cache-control', 'no-cache')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()

                bus = CAN.Bus(DEFAULT_CAN_DEVICE)
                while True:
                    try:
                        frame = bus.recv()
                    except CAN.BusDown:
                        self.wfile.write(bytes('event: error' + "\n" + 'data: ' + DEFAULT_CAN_DEVICE + ' is down.' + "\n\n", 'utf-8'))
                        sleep(1)
                        continue
                    except SystemExit:
                        # This doesn't get called. Find a way if possible
                        self.wfile.write(bytes('event: error' + "\n" + 'data: System is shutting down.' + "\n\n", 'utf-8'))
                        raise
                    id = frame.id
                    data = frame.data
                    data = ",".join(map(str, data))
                    self.wfile.write(bytes('data: {"bus":"can0","id":' + str(id) + ',"data":[' + data + '],"ts":"' + datetime.now().isoformat() + '"}' + "\n\n", 'utf8'))

            # File
            filepath = WWW_DIR + self.path
            if path.isfile(filepath):
                f = open(filepath)
                self.send_response(200)
                if self.path.endswith(".html"):
                    self.send_header('Content-type', 'text/html')
                elif self.path.endswith(".js"):
                    self.send_header('Content-type', 'text/javascript')
                elif self.path.endswith(".css"):
                  self.send_header('Content-type', 'text/css')
                self.end_headers()
                self.wfile.write(bytes(f.read(), 'UTF-8'))
                f.close()
                return

            self.send_response(404)
            self.end_headers()

        except BadRequest as e:
            self.send_response(400)
            self.send_error(400, 'Bad Request: %s' % str(e.args))
        except BrokenPipeError:
            print('Connection closed.')
        except IOError:
            self.send_response(500)
            print("\n*** do_GET except ***")
            print("Unexpected error:", sys.exc_info()[0])
            traceback.print_exc()

    def do_POST(self):
        try:
            content_len = int(self.headers.get('content-length', 0)) # access POST body
            post_body = self.rfile.read(content_len) # read POST body
            post_body = post_body.decode('utf8')
            frame = parse_request(parse_qs(post_body))
            self.send_response(204)
            self.end_headers()

        # do_POST try except clause
        except BadRequest as e:
            self.send_response(400)
            self.send_error(400, 'Bad Request: %s' % str(e.args))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            traceback.print_exc()

    def log_message(self, format, *args):
        return # Suppress logging

signal.signal(signal.SIGTERM, sigterm_handler)
srvr = ThreadedHTTPServer(('', 8000), RequestHandler)
srvr.serve_forever()
