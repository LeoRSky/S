import socket
from pathlib import Path

IP = "127.0.0.1"
PORT = 5000
LIMIT_SIZE = 1024 * 1024


def send_file(connection, file_path: Path):
    size = file_path.stat().st_size

    if size > LIMIT_SIZE:
        connection.sendall("ОШИБКА: файл слишком большой\n".encode())
        print("Размер превышает лимит")
        return

    connection.sendall(f"OK\n{file_path.name}\n".encode())

    with file_path.open("rb") as file:
        while chunk := file.read(4096):
            connection.sendall(chunk)

    print("Передача завершена")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((IP, PORT))
        server.listen()

        print("Сервер запущен. Ожидание клиента...")

        conn, address = server.accept()
        with conn:
            print("Подключился клиент:", address)

            requested_name = conn.recv(1024).decode().strip()
            print("Запрошен файл:", requested_name)

            file_path = Path(requested_name)

            if not file_path.exists():
                conn.sendall("ОШИБКА: файл не найден\n".encode())
                print("Файл не найден")
                return

            send_file(conn, file_path)


main()