


class Room:
    _uid = 0
    
    def __init__(self, client_id):
        Room._uid = Room._uid + 1
        self._id = Room._uid
        
        self._full = False
        self._clients = [client_id]
        
    def get_id(self):
        return self._id
        
    def add_client(self, client2_id):
        if( self._full ):
            return False
                   
        self._clients.append(client2_id)
        self._full = True
        return True
        
    def get_clients(self):
        return tuple(self._clients)
        
    def is_full(self):
        return self._full    