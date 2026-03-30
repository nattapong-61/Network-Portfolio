#Nattapong 673380038-9
import time

class Token:
    def __init__(self, message):
        self.message = message
        self.read = False
        self.timestamp = time.time()

    def access(self):
        if self.read:
            return "[COLLAPSED] ข้อความนี้ถูกอ่านไปแล้วและสลายตัวแล้ว"
        
        if time.time() - self.timestamp > 10:
            return "[EXPIRED] ข้อความสลายตัวตามกาลเวลา (Quantum Decoherence)"
        
        self.read = True
        return f"[SECRET]: {self.message}"