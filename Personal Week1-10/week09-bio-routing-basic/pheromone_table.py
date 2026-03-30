#Nattapong 673380038-9
class PheromoneTable:
    def __init__(self, initial_value):
        self.table = {}
        self.initial_value = initial_value

    def reinforce(self, peer, amount):
        current = self.table.get(peer, self.initial_value)
        self.table[peer] = current + amount

    def decay(self, factor):
        for peer in self.table:
            self.table[peer] *= factor

    def get_best_peer(self):
        if not self.table: return None
        return max(self.table, key=self.table.get)