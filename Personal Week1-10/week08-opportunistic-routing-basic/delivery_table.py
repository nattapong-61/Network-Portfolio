#Nattapong 673380038-9
class DeliveryTable:
    def __init__(self):
        self.table = {}  

    def update_probability(self, peer, prob):
        self.table[peer] = prob

    def get_probability(self, peer):
        return self.table.get(peer, 0.0)