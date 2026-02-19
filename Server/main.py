import socket
import threading

HOST = '127.0.0.1'
PORT = 4000

clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print("--- Сервер запущен ---")
print("Ожидание подключений...")

def handle_client(client_socket, address):
    print(f"[OK] Клиент {address} подключился.")
    clients.append(client_socket)

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
    except:
        pass
    finally:
        print(f"[!] Клиент {address} отключился.")
        clients.remove(client_socket)
        client_socket.close()

def send_messages():
    while True:
        message = input("Сообщение для всех клиентов: ")
        for client in clients:
            try:
                client.send(message.encode('utf-8'))
            except:
                pass

threading.Thread(target=send_messages, daemon=True).start()

try:
    while True:
        client_socket, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()

except KeyboardInterrupt:
    print("\nСервер остановлен.")
finally:
    server.close()