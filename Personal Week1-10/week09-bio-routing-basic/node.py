#Nattapong 673380038-9
import socket
import threading
import time
import sys
from config import *
from pheromone_table import PheromoneTable

if len(sys.argv) < 2:
    print("Usage: python node.py [ID]")
    sys.exit()

node_id = int(sys.argv[1])
MY_PORT = BASE_PORT + node_id
pt = PheromoneTable(INITIAL_PHEROMONE)

def pheromone_decay_worker():
    while True:
        time.sleep(UPDATE_INTERVAL)
        pt.decay(DECAY_FACTOR)
        print(f"\n[Decay] ฟีโรโมนจางลง... ตารางปัจจุบัน: {pt.table}")

def start_receiver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, MY_PORT))
    sock.listen(5)
    print(f"[NODE {node_id}] รับฟังที่พอร์ต {MY_PORT}")
    while True:
        conn, addr = sock.accept()
        data = conn.recv(BUFFER_SIZE).decode()
        if data:
            print(f"\n[ได้รับ] {data}")
        conn.close()

threading.Thread(target=pheromone_decay_worker, daemon=True).start()
threading.Thread(target=start_receiver, daemon=True).start()

print(f"--- Welcome Node {node_id} (Bio-Inspired Routing) ---")
while True:
    msg = input(f"\nNode {node_id} > พิมพ์ข้อความ: ")
    if msg.lower() == 'exit': break
    
    best_peer = pt.get_best_peer()
    if not best_peer:
        best_peer = PEER_PORTS[0] if PEER_PORTS[0] != MY_PORT else PEER_PORTS[1]

    print(f"[Ant Search] เลือกเส้นทางที่มีฟีโรโมนสูงสุด: {best_peer}")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((HOST, best_peer))
        s.sendall(f"จาก Node {node_id}: {msg}".encode())
        s.close()
        
        pt.reinforce(best_peer, REINFORCEMENT)
        print(f"[Success] ส่งสำเร็จ! เพิ่มฟีโรโมนให้ทาง {best_peer} เป็น {pt.table[best_peer]}")
    except:
        print(f"[Fail] ทาง {best_peer} ขัดข้อง! ฟีโรโมนจะลดลงตามธรรมชาติ")