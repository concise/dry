#!/usr/bin/env python3

import http.server
import json
import os

__DIR__ = os.path.dirname(os.path.abspath(__file__))

class MyWebServer(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        path = self.path
        if path == '/':
            self.send_response(200)
            self.end_headers()
            with open(__DIR__ + '/index.html', 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        path = self.path
        body = json.loads(
            self.rfile.read(int(self.headers['Content-Length'])).decode()
        )

        stdout, stderr, retcode = SYSTEM(['/usr/local/bin/attack'] + body)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'ok')

def SYSTEM(command, stdin=None):
    from subprocess import Popen, PIPE
    proc = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = proc.communicate(stdin)
    return stdout, stderr, proc.returncode

def main():
    webserver = http.server.HTTPServer(('', 8888), MyWebServer)
    webserver.serve_forever()

if __name__ == '__main__':
    main()

