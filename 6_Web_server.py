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


class MyHandler(http.server.SimpleHTTPRequestHandler):
    # Задание 1: Отправка основных заголовков
    def end_headers(self):
        self.send_header('Date', datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT'))
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Server', 'MyCustomServer')
        self.send_header('Connection', 'close')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    # Задание 3: Отправка ошибки 404 при отсутствии файла
    def do_GET(self):
        try:
            f = open(self.translate_path(self.path), 'rb')
        except FileNotFoundError:
            self.send_error(404, "File Not Found")
            return
        http.server.SimpleHTTPRequestHandler.do_GET(self)

    # Задание 4: Многопоточный режим работы сервера
    def handle(self):
        http.server.SimpleHTTPRequestHandler.handle(self)

    # Задание 5: Логирование запросов
    def log_message(self, format, *args):
        with open("server.log", "a") as log_file:
            log_file.write("%s - %s [%s] %s\n" %
                            (self.client_address[0], self.log_date_time_string(),
                             self.requestline, format%args))

    # Задание 6: Поддержка определенных типов файлов
    allowed_extensions = ['.html', '.css', '.js']

    def do_GET(self):
        if not any(self.path.endswith(ext) for ext in self.allowed_extensions):
            self.send_error(403, "Forbidden")
            return
        http.server.SimpleHTTPRequestHandler.do_GET(self)

    # Задание 7: Поддержка постоянного соединения
    protocol_version = 'HTTP/1.1'

    def end_headers(self):
        self.send_header('Connection', 'keep-alive')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    # Задание 8: Поддержка бинарных типов данных
    binary_extensions = ['.jpg', '.jpeg', '.png', '.gif']

    def do_GET(self):
        if any(self.path.endswith(ext) for ext in self.binary_extensions):
            self.send_header('Content-Type', 'image/jpeg')  
        http.server.SimpleHTTPRequestHandler.do_GET(self)

# Задание 2: Чтение конфигурационного файла и запуск сервера
config = configparser.ConfigParser()
config.read('server_config.ini')

port = int(config['port']['port_number'])
work_directory = config['directories']['work_directory']
max_request_size = int(config['settings']['max_request_size'])

with socketserver.ThreadingTCPServer(("", port), MyHandler) as httpd:
    print("Server running at port", port)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    server_thread.join()