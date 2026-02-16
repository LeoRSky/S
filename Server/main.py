import socket
import sys

HOST = '127.0.0.1'
PORT = 4000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

print("--- Сервер чата запущен ---")
print("Ожидание подключения клиента...")

try:
    while True:
        client_socket, address = server.accept()
        print(f"[OK] Клиент {address} подключился.")

        with client_socket:
            while True:
                try:
                    data = client_socket.recv(1024).decode('utf-8')
                    if not data:
                        print(f"Клиент {address} отключился.")
                        break

                    print(f"\n[Клиент {address}]: {data}")
                    reply = input("Ваш ответ (Сервер): ")
                    client_socket.send(reply.encode('utf-8'))

                except (ConnectionResetError, BrokenPipeError):
                    print(f"\nСвязь с клиентом {address} потеряна.")
                    break
                except Exception as e:
                    print(f"Произошла ошибка: {e}")
                    break

except KeyboardInterrupt:
    print("\nСервер остановлен пользователем.")
finally:
    server.close()
    sys.exit(0)