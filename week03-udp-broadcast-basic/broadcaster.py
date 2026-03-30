#Nattapong 673380038-9
import socket
import time
from config import BROADCAST_IP, PORT, BUFFER_SIZE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


sock.settimeout(2.0)

print(f"[BROADCASTER] กำลังส่งข้อความกระจายเสียงไปยังพอร์ต {PORT}...")

try:
    message = "DISCOVER_SERVER_BY_SIRIRAT"
    print(f"📣 ส่งข้อความ: {message}")
    
   
    sock.sendto(message.encode(), (BROADCAST_IP, PORT))

    
    print("รอการตอบกลับ")
    while True:
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            print(f" พบเครื่องตอบกลับจาก {addr}: {data.decode()}")
        except socket.timeout:
            print("หมดเวลา")
            break

finally:
    sock.close()
    print("[BROADCASTER] ปิดการทำงาน")