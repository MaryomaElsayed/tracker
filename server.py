from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import sqlite3

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/habits"):
            conn = sqlite3.connect('habits.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM habits")
            rows = cur.fetchall()
            response = "".join(f"<div>{row[1]}</div>" for row in rows)
            conn.close()

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path.endswith("/add"):
            length = int(self.headers['Content-Length'])
            post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
            new_habit = post_data['habit'][0]

            conn = sqlite3.connect('habits.db')
            cur = conn.cursor()
            cur.execute("INSERT INTO habits (habit) VALUES (?)", (new_habit,))
            conn.commit()
            conn.close()

            self.send_response(303)
            self.send_header('Location', '/habits')
            self.end_headers()

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, WebServerHandler)
    print("Server running on port 8000...")
    httpd.serve_forever()
