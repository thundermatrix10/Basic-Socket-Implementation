import socket
import threading
import tkinter as tk

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)

        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(f"[DISCONNECT] {addr} disconnected.")
            else:
                print(f"[{addr}] {msg}")
                received_messages_text.config(state=tk.NORMAL)
                received_messages_text.insert(tk.END, f"[{addr}] {msg}\n")
                received_messages_text.config(state=tk.DISABLED)

    conn.close()

def start_server():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}.")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        active_connections_label.config(text=f"Active connections: {threading.active_count() - 1}")

root = tk.Tk()
root.title("Chat Server")

received_messages_label = tk.Label(root, text="Received Messages:")
received_messages_label.pack()

received_messages_text = tk.Text(root, height=10, width=50)
received_messages_text.pack()

active_connections_label = tk.Label(root, text="Active connections: 0")
active_connections_label.pack()

server_thread = threading.Thread(target=start_server)
server_thread.start()

root.mainloop()
