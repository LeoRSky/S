import socket
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

IP = "127.0.0.1"
PORT = 4000

class ChatClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((IP, PORT))

        self.active = True

        self.init_ui()
        threading.Thread(target=self.listen_server, daemon=True).start()

    def init_ui(self):
        self.window = tk.Tk()
        self.window.title("Клиент чата")

        self.chat_box = ScrolledText(self.window, width=55, height=20, state="disabled")
        self.chat_box.pack(padx=10, pady=10)

        self.input_field = tk.Entry(self.window, width=40)
        self.input_field.pack(side=tk.LEFT, padx=10, pady=5)
        self.input_field.bind("<Return>", self.send_message)

        tk.Button(self.window, text="Отправить", command=self.send_message).pack(side=tk.LEFT, padx=5)
        tk.Button(self.window, text="Выход", command=self.close).pack(side=tk.LEFT, padx=5)

        self.window.protocol("WM_DELETE_WINDOW", self.close)

    def add_message(self, text):
        self.chat_box.config(state="normal")
        self.chat_box.insert(tk.END, text + "\n")
        self.chat_box.see(tk.END)
        self.chat_box.config(state="disabled")

    def listen_server(self):
        while self.active:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                self.add_message(data.decode())
            except:
                break

    def send_message(self, event=None):
        msg = self.input_field.get()
        if msg:
            try:
                self.sock.sendall(msg.encode())
                self.add_message(f"Вы: {msg}")
                self.input_field.delete(0, tk.END)
            except:
                self.add_message("Ошибка отправки")

    def close(self):
        self.active = False
        try:
            self.sock.close()
        except:
            pass
        self.window.destroy()


client_app = ChatClient()
client_app.window.mainloop()