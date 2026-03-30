#Nattapong 673380038-9
import socket
import threading
import time
import random
import sys
from config import HOST, BASE_PORT, BUFFER_SIZE, FORWARD_THRESHOLD, UPDATE_INTERVAL, PEER_PORTS
from delivery_table import DeliveryTable

if len(sys.argv) < 2:
    print("Usage: python node.py [ID]")
    sys.exit()

node_id = int(sys.argv[1])
MY_PORT = BASE_PORT + node_id
dt = DeliveryTable()
pending_msgs = [] 

def update_metrics():
    while True:
        for p in PEER_PORTS:
            if p != MY_PORT:
                new_prob = round(random.random(), 2)
                dt.update_probability(p, new_prob)
        print(f"\n [Update] ตารางโอกาสส่งถึง: {dt.table}")
        
        check_and_forward_pending()
        time.sleep(UPDATE_INTERVAL)

def check_and_forward_pending():
    global pending_msgs
    for msg in pending_msgs[:]:
        for peer_port, prob in dt.table.items():
            if prob > FORWARD_THRESHOLD:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    s.connect((HOST, peer_port))
                    s.sendall(f"[OPPORTUNISTIC] {msg}".encode())
                    s.close()
                    print(f" [SUCCESS] จังหวะดี! ส่งข้อความที่ค้างไว้ให้ {peer_port} แล้ว (Prob: {prob})")
                    pending_msgs.remove(msg)
                    break
                except: pass

def start_receiver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, MY_PORT))
    sock.listen(5)
    print(f" [NODE {node_id}] รับฟังที่พอร์ต {MY_PORT}")
    while True:
        conn, addr = sock.accept()
        data = conn.recv(BUFFER_SIZE).decode()
        if data:
            print(f"\n [ได้รับ] {data}")
        conn.close()


threading.Thread(target=update_metrics, daemon=True).start()
threading.Thread(target=start_receiver, daemon=True).start()

print(f"--- Welcome Node {node_id} (Opportunistic) ---")
while True:
    msg = input(f"Node {node_id} > พิมพ์ข้อความ: ")
    if msg.lower() == 'exit': break
    
    print(" [Queue] เก็บข้อความลงคิว รอโอกาสที่เหมาะสม (โหนดเข้าใกล้กัน)...")
    pending_msgs.append(f"จาก Node {node_id}: {msg}")