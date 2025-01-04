import asyncio
import time
from helper import *

COMMANDS_RESEND_TIME = 1000
COMMANDS_TIME_OUT = 5000
COMMANDS_RECHECK_TIME = 0.9


class Command():
    def __init__(self, push, callback):
        self.push = push
        self.callback = callback
        
        timenow = time.monotonic()*1000
        self.send_at = timenow
        self.resend_at = timenow + COMMANDS_RESEND_TIME
    
    def push(self):
        self.push()
        
    def callback(self, data):
        self.callback(data)
    

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
                self.process_commands[comm_id].callback(response)
                del self.process_commands[comm_id]
    
    # Повторная отправка комманд не получивших ответа
    async def handle_responces(self):
        while self.running:
            timeout_comms = []
            
            timenow = time.monotonic() * 1000
            for comm_id, comm in self.process_commands.items():
                if timenow > comm.resend_at:
                    comm.push()
                    comm.resend_at = timenow + COMMANDS_RESEND_TIME
                    
                    # Таймаут
                    if timenow - comm.send_at > COMMANDS_TIME_OUT:
                        timeout_comms.append(comm_id)
            
            # Удаление таймаут комманд
            for comm_id in timeout_comms:
                print(f" [ответ от комманды {comm_id} не получен] ")
                del self.process_commands[comm_id]
                    
            await asyncio.sleep(COMMANDS_RECHECK_TIME)
        
    
    def push_command(self, data, callback_handler):
        self.comm_id += 1
        if self.comm_id > 32000:
            self.comm_id = 1
        
        push_data =  encodeS( f"@{self.comm_id} {data}" )
                
        command = Command(
            lambda: self.sock.sendto(push_data),
            callback_handler
        )
        self.process_commands[self.comm_id] = command
        command.push()