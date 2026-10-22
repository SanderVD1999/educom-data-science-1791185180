import hashlib
import math
# voorbeeld van hashlib: s = hashlib.sha256(b"Emil").hexdigest()... geeft code van 64 karakters, zowel letters als cijfers.
# Bloomfilter neemt set van elementen en maakt een bit array van grootte m. Het gebruikt k hash functies om de bits te zetten. Bij het toevoegen van een element worden de bits op de posities van de hash functies gezet. Bij het controleren of een element aanwezig is, worden de bits op de posities van de hash functies gecontroleerd. Als alle bits 1 zijn, is het element waarschijnlijk aanwezig, anders is het zeker niet aanwezig.
# size = 1000, hashes zijn er 4, bits hebben we 6236 nodig voor een fp van 5%
class BloomFilter:
    def __init__(self, size, hashess):
        self.size = size
        self.hashess = hashess
        self.bits = [0] * int((size * 6.236))
    def positions(self, ticket_no):
        positions = []
        for i in range(self.hashess):
            hash_value = hashlib.sha256((str(i) + ticket_no).encode()).hexdigest()
            position = int(hash_value, 16) % len(self.bits)
            positions.append(position)
        return positions
    def add(self, ticket_no):
        for p in self.positions(ticket_no):
            self.bits[p] = 1
    def check(self, ticket_no):
        for p in self.positions(ticket_no):
            if self.bits[p] == 0:
                return False
        return True

bloom_filter = BloomFilter(size=1000, hashess=4)

while True:
    ticket_no = input("Enter your ticket number or stop the execution by typing 'Stop': ")
    if ticket_no.lower() == 'stop':
        print("Execution stopped.")
        break
    if len(ticket_no) < 5:
        print("Ticket is invalid. Please enter a valid ticket number.")
    elif bloom_filter.check(ticket_no):
        print(f"{ticket_no} is invalid.")
    else:
        print(f"{ticket_no} is valid and registered.")
        bloom_filter.add(ticket_no)


    

