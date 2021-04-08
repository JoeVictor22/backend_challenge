import http.server
import socketserver
import os

PORT = 8000

swagger_dir = os.path.join(os.path.dirname(__file__), 'swagger')
os.chdir(swagger_dir)

Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()