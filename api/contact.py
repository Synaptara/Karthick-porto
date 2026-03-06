from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import os


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read the incoming JSON from your frontend
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            name = data.get("name", "Unknown")
            email = data.get("email", "No Email provided")
            message = data.get("message", "")

            # Fetch the API key from Vercel environment variables
            api_key = os.environ.get("RESEND_API_KEY")

            # Resend requires you to use their onboarding email until you add a custom domain
            payload = json.dumps(
                {
                    "from": "Portfolio <onboarding@resend.dev>",
                    "to": "karthick.aidev@gmail.com",
                    "subject": f"New Portfolio Message from {name}",
                    "text": f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                }
            ).encode("utf-8")

            # Make the request to Resend
            req = urllib.request.Request(
                "https://api.resend.com/emails", data=payload, method="POST"
            )
            req.add_header("Authorization", f"Bearer {api_key}")
            req.add_header("Content-Type", "application/json")

            urllib.request.urlopen(req)

            # Send success response back to the frontend
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode("utf-8"))

        except Exception as e:
            # Send error response
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
