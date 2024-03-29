from http.server import HTTPServer, SimpleHTTPRequestHandler
import http.server
import socketserver
from datetime import datetime
import configparser
import threading


# Задаем порт и рабочую директорию сервера
port = 80
directory = "."

# Создаем HTTP сервер
server_address = ("", port)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

# Запускаем сервер
print(f"Starting server on port {port}...")
httpd.serve_forever()