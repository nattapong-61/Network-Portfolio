#Nattapong 673380038-9
import socket
import threading
import sys
from config import HOST, BASE_PORT, BUFFER_SIZE

if len(sys.argv) < 2:
    print("กรุณาใส่ ID ของ Peer ด้วย (เช่น: python peer.py 1)")
    sys.exit()

peer_id = int(sys.argv[1])
MY_PORT = BASE_PORT + peer_id


def listen_for_peers():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((HOST, MY_PORT))
    server_sock.listen(5)
    print(f"[PEER {peer_id}] เริ่มต้น Server ที่พอร์ต {MY_PORT}")

    while True:
        conn, addr = server_sock.accept()
        data = conn.recv(BUFFER_SIZE)
        if data:
            print(f"\n[ข้อความเข้าจาก {addr}]: {data.decode()}")
            print(f"[PEER {peer_id}] ป้อน ID เพื่อนที่ต้องการคุยด้วย: ", end="", flush=True)
        conn.close()


listener_thread = threading.Thread(target=listen_for_peers, daemon=True)
listener_thread.start()


print(f"--- ยินดีต้อนรับ Peer {peer_id} (Sirirat 673380060-6) ---")
try:
    while True:
        target_id = input(f"[PEER {peer_id}] ป้อน ID เพื่อนที่ต้องการคุยด้วย: ")
        if target_id.lower() == 'exit': break
        
        target_port = BASE_PORT + int(target_id)
        msg = input("พิมพ์ข้อความ: ")
        
        try:
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_sock.connect((HOST, target_port))
            client_sock.sendall(f"จาก Peer {peer_id}: {msg}".encode())
            client_sock.close()
            print(f"ส่งหา Peer {target_id} สำเร็จ")
        except:
            print(f"ไม่สามารถติดต่อ Peer {target_id}")

except KeyboardInterrupt:
    print("\nปิดโปรแกรม")