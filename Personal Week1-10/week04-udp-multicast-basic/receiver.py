#Nattapong 673380038-9
import socket
import struct
from config import MULTICAST_GROUP, PORT, BUFFER_SIZE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


sock.bind(('', PORT))

group = socket.inet_aton(MULTICAST_GROUP)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print(f"[RECEIVER] เข้าร่วมกลุ่ม {MULTICAST_GROUP} เรียบร้อย")

try:
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        print(f"[Group Data] จาก {addr}: {data.decode()}")
except KeyboardInterrupt:
    print("\n[RECEIVER] ออกจากกลุ่ม...")
finally:
    sock.close()