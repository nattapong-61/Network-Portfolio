#Nattapong 673380038-9
import socket
from config import PORT, BUFFER_SIZE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(("", PORT)) 

print(f"[LISTENER] เปิดหูรอฟังการตะโกนที่พอร์ต {PORT}...")

try:
    while True:
       
        data, addr = sock.recvfrom(BUFFER_SIZE)
        message = data.decode()
        print(f"ข้อความจาก {addr}: {message}")

       
        if message == "DISCOVER_SERVER_BY_SIRIRAT":
            reply = "I_AM_HERE_673380060-6"
            sock.sendto(reply.encode(), addr)
            print(f"ตอบกลับไปยัง {addr} ")

except KeyboardInterrupt:
    print("\n[LISTENER] หยุดการทำงาน")
finally:
    sock.close()