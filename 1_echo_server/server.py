import socket
import logging

# Настройки логирования
logging.basicConfig(
    format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
    handlers=[logging.FileHandler("server.log", 'w', 'utf-8'), logging.StreamHandler()],
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

sock = socket.socket()

port_input = input("Введите номер порта для сервера -> ")
ip_input = input("Введите IP для сервера -> ")

port = int(input('Введите омер порта для проверки ->'))

password = str(input('Введите пароль - > '))


sock.bind((ip_input, int(port_input)))
sock.listen(0)
conn, addr = sock.accept()
print(addr)

msg = ''

while True:
 data = conn.recv(1024)
 if not data:
  break
 msg += data.decode()
 logging.info(f"Передача данных ")
 conn.send(data)

print(msg)

conn.close()
