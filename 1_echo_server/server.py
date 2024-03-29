import socket
import logging
from typing import Any
import json
from typing import Tuple, Union

import yaml

# Настройки логирования 5 номер
logging.basicConfig(
    format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
    handlers=[logging.FileHandler("server.log", 'w', 'utf-8'), logging.StreamHandler()],
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

sock = socket.socket()

port_input = input("Введите номер порта для сервера -> ")
ip_input = input("Введите IP для сервера -> ")

port = int(input('Введите номер порта для проверки ->'))

password = str(input('Введите пароль - > '))


def user_processing(self):                                      # 2 номер
        """Обработка ввода сообщений пользователя"""

        while True:
            msg = input()
            # Если сообщение exit
            if msg == "exit":
                break

            self.send_message(msg)

def port_validation(value: Any, check_open: bool = False) -> bool:          # 4 номер
    """Проверка на корректность порта"""
    try:
        # Проверка на число
        value = int(value)
        # Проверка на диапазон
        if 1 <= value <= 65535:
            # Проверка то, занят ли порт
            if check_open:
                return check_port_open(value)
            print(f"Корректный порт {value}")
            return True

        print(f"Некорректное значение {value} для порта")
        return False

    except ValueError:
        print(f"Значение {value} не является числом!")
        return False
    
def check_port_open(port: int) -> bool:                             # 6 номер
    """
    Проверка на свободный порт port

    Является частью логики port_validation
    """
    try:
        sock = socket.socket()
        sock.bind(("", port))
        sock.close()
        print(f"Порт {port} свободен")
        return True
    except OSError:
        print(f"Порт {port} занят")
        return False
    
def ip_validation(address: str) -> bool:
    """Проверка на корректность ip-адреса (v4)"""
    error_message = f"Некорректный ip-адрес {address}"
    ok_message = f"Корректный ip-адрес {address}"
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            print(error_message)
            return False
        return address.count(".") == 3
    except socket.error:  # not a valid address
        print(error_message)
        return False
    
def reg_logic(self, conn, addr):                                                                
        """
        Логика регистрации пользователя
        """
        data = json.loads(conn.recv(1024).decode())
        newuser_password, newuser_username = hash(data["password"]), data["username"]
        newuser_ip = addr[0]
        self.database.user_reg(newuser_ip, newuser_password, newuser_username)
        logger.info(f"Клиент {newuser_ip} -> регистрация прошла успешно")
        data = {"result": True}
        if newuser_ip in self.reg_list:
            self.reg_list.remove(newuser_ip)
            logging.info(f"Удалили клиента {newuser_ip} из списка регистрации")

        self.send_message(conn, data, newuser_ip)
        logger.info(f"Клиент {newuser_ip}. Отправили данные о результате регистрации")

class DataProcessing:                                               # 7 номер
    """Класс для работы с коллекцией пользователей в yaml"""

    def __init__(self) -> None:
        self.file_path = "./data/users.yml"
        self.data = []
        self.read_collection()

    def read_collection(self):
        """Чтение данных с файла в self.data"""
        with open(self.file_path, "r") as stream:
            data = yaml.safe_load(stream)
            if data is None:
                data = []
            self.data = data

    def write_collection(self):
        """Запись данных с self.data в файл"""
        with open(self.file_path, "w") as stream:
            yaml.dump(self.data, stream)

    def user_auth(self, ip: str, password: str) -> Tuple[int, Union[str, None]]:
        """
        Метод авторизации пользователя в системе

        1 - авторизация прошла успешно
        0 - авторизация неудачная
        -1 - необходима регистрация пользователя
        """
        for user in self.data:
            if user["ip_addr"] == ip and user["password"] == password:
                return 1, user["username"]

        for user in self.data:
            if user["ip_addr"] == ip:
                return 0, None

        return -1, None

    def user_reg(self, ip: str, password: str, username: str) -> None:
        """Метод регистрации пользователей"""
        self.data.append({"ip_addr": ip, "password": password, "username": username})
        self.write_collection()
    
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
