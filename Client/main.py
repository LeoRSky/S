import socket

HOST = '127.0.0.1'
PORT = 4000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("--- Подключено к серверу ---")
print("Ожидание сообщений...")

try:
    while True:
        data = client.recv(1024).decode('utf-8')
        if not data:
            break
        print(f"\n[Сервер]: {data}")

except KeyboardInterrupt:
    print("\nОтключение...")
finally:
    client.close()
