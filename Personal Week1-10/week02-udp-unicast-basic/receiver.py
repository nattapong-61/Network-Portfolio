#Nattapong 673380038-9
import socket
from config import HOST, PORT, BUFFER_SIZE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print(f"[RECEIVER] พร้อมรับข้อมูลที่พอร์ต {PORT} (UDP)")

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    raw_msg = data.decode()

    if "|" in raw_msg:
        seq, message = raw_msg.split("|", 1)
        print(f"[{addr}] ได้รับแพ็กเกจที่: {seq} | ข้อความ: {message}")
    else:
        print(f"[{addr}] ได้รับข้อมูลดิบ: {raw_msg}")

    if "exit" in raw_msg.lower(): break
sock.close()