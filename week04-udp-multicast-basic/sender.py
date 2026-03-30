#Nattapong 673380038-9
import socket
from config import MULTICAST_GROUP, PORT, TTL

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)

print(f"[SENDER] กำลังส่งข้อมูลไปยังกลุ่ม {MULTICAST_GROUP}...")

while True:
    message = input("พิมพ์ข้อความส่งเข้ากลุ่ม (หรือ 'exit'): ")
    if message.lower() == 'exit':
        break

    sock.sendto(message.encode(), (MULTICAST_GROUP, PORT))

sock.close()