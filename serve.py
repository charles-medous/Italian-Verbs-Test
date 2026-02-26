# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 13:46:08 2025

@author: cmedous
"""

# serve.py
import http.server
import socketserver
import os

WEB_ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(WEB_ROOT)
PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
