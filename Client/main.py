import socket

IP = "127.0.0.1"
PORT = 5000


def download_file(sock):
    header = sock.recv(1024).decode().splitlines()

    if not header:
        print("Нет ответа от сервера")
        return

    if header[0] != "OK":
        print("Ошибка сервера:", header[0])
        return

    filename = header[1]
    print("Начинается загрузка:", filename)

    with open(filename, "wb") as file:
        while True:
            data = sock.recv(4096)
            if not data:
                break
            file.write(data)

    print("Файл успешно получен:", filename)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((IP, PORT))
        print("Соединение с сервером установлено")

        file_name = input("Введите имя файла для загрузки: ")
        client.sendall(file_name.encode())

        download_file(client)


main()