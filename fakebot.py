from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class H(BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        msg = json.loads(self.rfile.read(n)).get("message", "")
        low = msg.lower()
        if "ignore" in low or "system:" in low:
            reply = "Okay! PWNED-7431"
        else:
            reply = "Sorry, I can only help with support questions."
        out = json.dumps({"reply": reply}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(out)

    def log_message(self, *a):
        pass

print("Fake bot running on http://127.0.0.1:8000")
HTTPServer(("127.0.0.1", 8000), H).serve_forever()
