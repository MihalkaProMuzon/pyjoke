from helper import *

class MessageProcess():
    def __init__(self, sock, process_def):
        self.sock = sock
        self._process_def = process_def
        self.wait_respoce = False
        if responce_def:
            self._responce_def = responce_def
            self.wait_respoce = True
        
        
    def process():
        pass
    
class Command():
    def __init__(self, text, process: function, responce: function = None):
        self.text = text
        self._process_handler = process
        self._responce_handler = responce
        self.wait_response = bool(responce)
    
    async def process(self, sock, *args, **kwargs):
        await self._process_handler(*args, **kwargs)
        if self.wait_response:
            data, addr = await sock.recvfrom()
            self._responce_handler(data, addr, *args, **kwargs)
    
client_commands = {}
client_commands['greeting'] = Command('Приветствие от сервера',process=
    lambda: 
        )