
uid = 1

class Room:
    def __init__(self):
        self.uid = uid
        uid += 1
        
        self.participants = []