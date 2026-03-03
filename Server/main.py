import socket
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

IP = "127.0.0.1"
PORT = 4000

class ChatServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((IP, PORT))
        self.server_socket.listen()

        self.clients = {}
        self.client_id_seq = 0
        self.active = True

        self.init_ui()
        threading.Thread(target=self.wait_clients, daemon=True).start()

    def init_ui(self):
        self.window = tk.Tk()
        self.window.title("Сервер чата")

        self.log_area = ScrolledText(self.window, width=65, height=20, state="disabled")
        self.log_area.pack(padx=10, pady=10)

        self.msg_input = tk.Entry(self.window, width=40)
        self.msg_input.pack(side=tk.LEFT, padx=5, pady=5)

        self.id_input = tk.Entry(self.window, width=8)
        self.id_input.insert(0, "ID")
        self.id_input.pack(side=tk.LEFT)

        tk.Button(self.window, text="Отправить", command=self.send_private).pack(side=tk.LEFT, padx=5)
        tk.Button(self.window, text="Выход", command=self.shutdown).pack(side=tk.LEFT, padx=5)

    def write_log(self, text):
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, text + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state="disabled")

    def handle_user(self, conn, uid):
        conn.sendall(f"Вы подключены как клиент №{uid}".encode())

        while self.active:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                self.write_log(f"Клиент {uid}: {data.decode()}")
            except:
                break

        conn.close()
        if uid in self.clients:
            del self.clients[uid]
        self.write_log(f"Клиент {uid} отключился")

    def wait_clients(self):
        while self.active:
            try:
                conn, addr = self.server_socket.accept()
                self.client_id_seq += 1
                self.clients[self.client_id_seq] = conn
                self.write_log(f"Подключился клиент {self.client_id_seq}")
                threading.Thread(target=self.handle_user,
                                 args=(conn, self.client_id_seq),
                                 daemon=True).start()
            except:
                break

    def send_private(self):
        message = self.msg_input.get()
        target = self.id_input.get()

        if not message or not target.isdigit():
            return

        target = int(target)

        if target in self.clients:
            try:
                self.clients[target].sendall(f"Сообщение от сервера: {message}".encode())
                self.write_log(f"Отправлено клиенту {target}: {message}")
            except:
                self.write_log("Ошибка отправки")
        else:
            self.write_log("Клиент не найден")

        self.msg_input.delete(0, tk.END)

    def shutdown(self):
        self.active = False
        for c in self.clients.values():
            try:
                c.close()
            except:
                pass
        self.server_socket.close()
        self.window.destroy()


app = ChatServer()
app.window.mainloop()