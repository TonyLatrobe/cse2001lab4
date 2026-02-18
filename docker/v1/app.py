from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import requests  # Importing the requests module to make HTTP calls

# URL of the promotion server (adjust as needed)
PROMOTION_SERVER_URL = "http://promotion-server:5000/kill"  # Assuming the promotion server is running at this address

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("index.html", "rb") as f:
                self.wfile.write(f.read())
        elif self.path == "/kill":
            # Log when /kill is hit
            print("Received /kill request, calling promotion server...")
            try:
                response = requests.get(PROMOTION_SERVER_URL)
                if response.status_code == 200:
                    print("Promotion server count updated!")
                    self.wfile.write(b"Promotion server count updated!")
                else:
                    print(f"Failed to update promotion server count. Status code: {response.status_code}")
                    self.wfile.write(b"Failed to update promotion server count.")
            except Exception as e:
                print(f"Error calling promotion server: {e}")
                self.wfile.write(b"Error calling promotion server.")
    
            # Simulate crash
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Crashing pod...")
            os._exit(1)
        elif self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    print("Self-healing server v1 running on port 8080")
    server.serve_forever()
