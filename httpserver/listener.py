# -*- coding: utf-8 -*-
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import urlparse
import threading
import argparse
import json
import time

import config
config.init_path()
from es.basic import BasicPeeker
from readfiles import Bilibili


basicpeeker = BasicPeeker(config.EsCfg.hosts)
bili = Bilibili('httpserver/rumors/fengqingyang.txt')

class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        return self.do_GET()

    def do_GET(self):
        begin_at = time.time()
        code = 403
        resp = {}
        splited_path = urlparse.urlparse(self.path).path.split('/')
        if len(splited_path) == 5 and splited_path[-4] == 'dumpeek':
            bid = splited_path[-3]
            date = splited_path[-2]
            key = splited_path[-1]
            code = 200
            # params = dict([(k, v[0]) for k, v in urlparse.parse_qs(urlparse.urlparse(self.path).query).items()])
            resp['rumor'] = bili.pick()
            resp['latency'] = round(time.time()-begin_at, 3)
            resp['dumps'+key] = basicpeeker.search(bid, date, key)
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        if code == 200:
            self.wfile.write(json.dumps(resp))
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True

    def shutdown(self):
        self.socket.close()
        HTTPServer.shutdown(self)


class SimpleHttpServer():
    def __init__(self, ip, port):
        self.server = ThreadedHTTPServer((ip, port), HTTPRequestHandler)

    def start(self):
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def waitForThread(self):
        self.server_thread.join()

    def stop(self):
        self.server.shutdown()
        self.waitForThread()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HTTP Server')
    parser.add_argument('port', type=int, help='Listening port for HTTP Server')
    parser.add_argument('ip', help='HTTP Server IP')
    args = parser.parse_args()
    server = SimpleHttpServer(args.ip, args.port)
    print 'server run...'
    server.start()
    server.waitForThread()
