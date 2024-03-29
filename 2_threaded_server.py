import socket
import threading


sock = socket.socket() 
sock.bind('', 9090)
sock.listen(0)
conn, addr = sock.accept()
print(addr)
connections_list = []

msg = ''

def proc(n):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        msg += data.decode()
        conn.send(data)

p1 = threading.Thread(target=proc, name="t1", args=["1"])
p1.start()

print(msg)

conn.close()