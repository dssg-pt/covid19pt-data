#!/usr/bin/env python3
"""
Simple HTTP server to run the COVID-19 spiral visualization.
This is needed to properly load the CSV files due to CORS restrictions.
"""

import http.server
import socketserver
import webbrowser
import os

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def main():
    # Change to the script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    Handler = MyHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"╔══════════════════════════════════════════════════════════════╗")
        print(f"║  COVID-19 Portugal: A Spiral Journey                        ║")
        print(f"╠══════════════════════════════════════════════════════════════╣")
        print(f"║  Server running at: http://localhost:{PORT}                    ║")
        print(f"║  Visualization URL: http://localhost:{PORT}/spiral_viz.html    ║")
        print(f"╠══════════════════════════════════════════════════════════════╣")
        print(f"║  Press Ctrl+C to stop the server                             ║")
        print(f"╚══════════════════════════════════════════════════════════════╝")

        # Open browser automatically
        webbrowser.open(f'http://localhost:{PORT}/spiral_viz.html')

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Server stopped.")

if __name__ == '__main__':
    main()
