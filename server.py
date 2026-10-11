import http.server
import json

spawns = []


class Handler(http.server.BaseHTTPRequestHandler):

  def do_POST(self):
    global spawns
    length = int(self.headers.get("content-length", 0))
    data = self.rfile.read(length).decode("utf-8")
    try:
      parsed = json.loads(data)
      spawns.append(parsed)
      if len(spawns) > 30:
        spawns.pop(0)
      self.send_response(200)
      self.end_headers()
      self.wfile.write(b"OK")
    except:
      self.send_response(400)
      self.end_headers()

  def do_GET(self):
    global spawns
    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()
    self.wfile.write(json.dumps(spawns).encode("utf-8"))

  def log_message(self, format, *args):
    return


server = http.server.HTTPServer(("localhost", 8000), Handler)
print("Сервер запущено!")
server.serve_forever()