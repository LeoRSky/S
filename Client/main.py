import socket
import time

HOST = '127.0.0.1'
PORT = 4000
RETRY_DELAY = 2

print("--- Клиент запущен и ищет сервер ---")

def connect_to_server():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, PORT))
            return client
        except ConnectionRefusedError:
            print(f"Сервер пока спит... Пробую снова через {RETRY_DELAY} сек.")
            time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
            time.sleep(RETRY_DELAY)


while True:
    client = connect_to_server()
    print("\n[OK] Подключено к серверу!")

    try:
        message = input("Вы (Клиент): ")
        if message.lower() == 'exit':
            print("Выход из программы...")
            break

        client.send(message.encode('utf-8'))

        data = client.recv(1024).decode('utf-8')
        if not data:
            print("Сервер закрыл соединение.")
        else:
            print(f"Сервер ответил: {data}")

    except (ConnectionResetError, BrokenPipeError):
        print("\n[!] Связь с сервером потеряна. Переподключаюсь...")
    except KeyboardInterrupt:
        print("\n[!] Прерывание пользователем. Выход...")
        break
    finally:
        client.close()