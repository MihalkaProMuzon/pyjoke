import socket

# Создаем сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('127.0.0.1', 52600)
message = 'Это тестовое сообщение'

try:
    # Отправляем данные
    print(f"Отправка {message} на {server_address}")
    sent = sock.sendto(message.encode(), server_address)

    # Получаем ответ
    data, server = sock.recvfrom(4096)
    print(f"Получено {data.decode()}")

finally:
    print("Закрытие сокета")
    sock.close()