import asyncio
import time
from helper import *

COMMANDS_REPEAT_TIME = 400
COMMANDS_RECHECK_TIME = 0.1

class Messanger():
    def __init__(self, sock):
        self.sock = sock
        self.process_commands = {}
        self.comm_id = 0
        self.running = True
    
        handle_response_task = asyncio.create_task( self.handle_responces() )
        handle_messages_task = asyncio.create_task( self.handle_messages() )
    
    async def handle_messages(self):
        while self.running:
            data, addr = await self.sock.recvfrom()
            comm, response = decodeB(data).split(' ', 1)
            comm_id = int(comm[1:])
            if comm_id in self.process_commands:
                self.process_commands[comm_id]['callback'](response)
                del self.process_commands[comm_id]
    
    # Повторная отправка комманд не получивших ответа
    async def handle_responces(self):
        while self.running:
            timenow = time.monotonic() * 1000
            for comm_id, comm in self.process_commands.items():
                if timenow > comm['repeat_at']:
                    #print(f" > {comm['repeat']} repeat comm {comm_id}")
                    comm['repeat'] = comm['repeat'] + 1
                    if comm['repeat'] > 30:
                        print(" [ответ от комманды не получен] ")
                        del self.process_commands[comm_id]
                    comm['push']()
                    
                    
            await asyncio.sleep(COMMANDS_RECHECK_TIME)
        
    
    def push_command(self, data, callback_handler):
        self.comm_id += 1
        if self.comm_id > 32000:
            self.comm_id = 1
        
        push_data =  encodeS( f"@{self.comm_id} {data}" )
        
        push = lambda: self.sock.sendto(push_data)
        
        self.process_commands[self.comm_id] = {
            'repeat_at': time.monotonic()*1000 + COMMANDS_REPEAT_TIME,
            'repeat': 0,
            'push': push,
            'callback': callback_handler
        }
        push()