#Nattapong 673380038-9
import socket
import threading
from datetime import datetime
from config import HOST, PORT, BUFFER_SIZE

def handle_client(conn, addr):
    print(f"[{datetime.now()}] [NEW CONNECTION] {addr} connected.")
    try:
        data = conn.recv(BUFFER_SIZE)
        if data:
            msg = data.decode()
            print(f"[{datetime.now()}] [RECEIVED from {addr}]: {msg}")
            reply = f"ACK: '{msg}' received at {datetime.now()}"
            conn.sendall(reply.encode())
    finally:
        conn.close()
        print(f"[{datetime.now()}] [DISCONNECTED] {addr}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"[SERVER STARTED] Listening on {HOST}:{PORT}...")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()