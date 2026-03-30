#Nattapong 673380038-9
import socket
import threading
import sys
from config import *
from token import Token

if len(sys.argv) < 2:
    print("Usage: python node.py [ID]")
    sys.exit()

node_id = int(sys.argv[1])
MY_PORT = BASE_PORT + node_id
quantum_vault = [] 

def start_receiver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, MY_PORT))
    sock.listen(5)
    print(f" [NODE {node_id}] พร้อมรับ Quantum Token ที่พอร์ต {MY_PORT}")
    while True:
        conn, addr = sock.accept()
        data = conn.recv(BUFFER_SIZE).decode()
        if data:
            quantum_vault.append(Token(data))
            print(f"\n[ได้รับ] Token ใหม่จาก {addr}! (ตรวจสอบในเมนู 2)")
        conn.close()

threading.Thread(target=start_receiver, daemon=True).start()

print(f"--- Welcome Node {node_id} (Quantum-Inspired) ---")
while True:
    print("\n[1] ส่งข้อความลับ | [2] อ่านข้อความในตู้เซฟ | [exit] ออก")
    cmd = input("เลือกเมนู: ")

    if cmd == '1':
        target = int(input("ส่งไปพอร์ตไหน (เช่น 11001): "))
        msg = input("พิมพ์ข้อความลับ: ")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, target))
            s.sendall(msg.encode())
            s.close()
            print("ส่งพัสดุควอนตัมสำเร็จ!")
        except:
            print("ส่งไม่สำเร็จ (เพื่อนอาจยังไม่เปิดเครื่อง)")

    elif cmd == '2':
        if not quantum_vault:
            print("ไม่มีข้อความในตู้เซฟ")
        else:
            t = quantum_vault.pop(0)
            print(t.access())

    elif cmd.lower() == 'exit': break