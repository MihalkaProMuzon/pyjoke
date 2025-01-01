import socket

# Создаем сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к адресу и порту
server_address = ('', 52600)  # '' означает, что сервер будет слушать на всех доступных интерфейсах
sock.bind(server_address)

print(f"Сервер запущен {server_address}")

while True:
    data, address = sock.recvfrom(4096)
    print(f"Получено {len(data)} байт от {address}")
    print(data.decode())

    if data:
        sent = sock.sendto(data, address)
        print(f"Отправлено {sent} байт обратно {address}")