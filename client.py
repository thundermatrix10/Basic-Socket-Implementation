import socket
import tkinter as tk

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048))
    
def send_message():
    message = message_entry.get()
    if message:
        send(message)
        message_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Chat Client")

message_label = tk.Label(root, text="Type your message:")
message_label.pack()

message_entry = tk.Entry(root, width=50)
message_entry.pack()

send_button = tk.Button(root, text="Send Message", command=send_message)
send_button.pack()

root.mainloop()

