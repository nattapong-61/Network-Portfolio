#Nattapong 673380038-9
import socket
import threading
import random
import sys
import time
from config import HOST, BASE_PORT, BUFFER_SIZE, NEIGHBORS, FORWARD_PROBABILITY, TTL

if len(sys.argv) < 2:
    print("Usage: python node.py [ID]")
    sys.exit()

node_id = int(sys.argv[1])
MY_PORT = BASE_PORT + node_id

def send_to_neighbor(target_port, message, current_ttl):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0) 
        s.connect((HOST, target_port))
        payload = f"{message}|{current_ttl}"
        s.sendall(payload.encode())
        s.close()
        return True
    except:
        return False


def handle_incoming():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((HOST, MY_PORT))
    server_sock.listen(5)
    print(f" [NODE {node_id}] พร้อมทำงานที่พอร์ต {MY_PORT}")

    while True:
        conn, addr = server_sock.accept()
        data = conn.recv(BUFFER_SIZE).decode()
        if data and "|" in data:
            msg, rcv_ttl = data.split('|')
            rcv_ttl = int(rcv_ttl)
            print(f"\n ได้รับข้อความ: '{msg}' (TTL คงเหลือ: {rcv_ttl})")

            if rcv_ttl > 0:
                if random.random() < FORWARD_PROBABILITY:
                    next_ttl = rcv_ttl - 1
                    print(f" กำลังส่งต่อให้เพื่อนบ้าน (Next TTL: {next_ttl})...")
                    for p in NEIGHBORS:
                        if p != MY_PORT:
                            if send_to_neighbor(p, msg, next_ttl):
                                print(f"ส่งต่อให้พอร์ต {p} สำเร็จ")
                else:
                    print("[Skip] รอบนี้สุ่มได้ว่าไม่ส่งต่อ")
        conn.close()

threading.Thread(target=handle_incoming, daemon=True).start()
time.sleep(0.5)

print(f"--- Welcome Node {node_id} ---")
while True:
    txt = input(f"Node {node_id} > พิมพ์ข้อความที่จะเริ่มส่ง: ")
    if txt.lower() == 'exit': break

    for p in NEIGHBORS:
        if p != MY_PORT:
            if send_to_neighbor(p, txt, TTL):
                print(f"ส่งข้อความเริ่มต้นไปที่พอร์ต {p} สำเร็จ")
            else:
                print(f"ติดต่อพอร์ต {p} ไม่ได้")