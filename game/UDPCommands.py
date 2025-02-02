import asyncio
import enum
import time
from helper import *

COMMANDS_RESEND_TIME = 1000
COMMANDS_TIME_OUT = 5000
COMMANDS_RECHECK_TIME = 0.9


# Комманды
@enum.unique
class ServerCommands(enum.Enum):
    greetings = 'Приветствие от сервера'
    create_room = 'Встать в очередь (arg1 = моё имя)'
    get_rooms = 'Показать свободные комнаты'
    connect_room = 'Присоедениться к игроку (arg1 = имя игрока, arg2 = моё имя)'
    get_my_room = 'Показать мою комнату (или состою ли я ваще в ней)'
    
    test1 = 'Деб проверка работы комманд 1'
    test2 = 'Деб проверка работы комманд 2'
    update = 'Обновить сервер (arg1 = имя векти на которую над переключить)'


class UDPCommand():
    def __init__(self, push_func, callback_func, is_handler = False):
        self._push_func = push_func
        self._callback_func = callback_func
        self._is_handler = is_handler
        
        if not is_handler:
            timenow = time.monotonic()*1000
            self.send_at = timenow
            self.resend_at = timenow + COMMANDS_RESEND_TIME
    
    def is_handler(self):
        return self._is_handler
    
    def push(self):
        self._push_func()
        
    def callback(self, data, *args):
        self._callback_func(data, *args)
        
        
class Messanger():
    def empty_def(data):
        print(f"!push-empty-handler! d: {data}")

    def __init__(self, sock):
        self.sock = sock
        self._process_commands = {}
        self._handlers = {}
        self._comm_id = 0
        self._running = True
    
        self._handle_response_task = asyncio.create_task( self._handle_responces() )
        self._handle_messages_task = asyncio.create_task( self._handle_messages() )
    
    # Прослушка сокета, отправка на комманды / хендлеры
    async def _handle_messages(self):
        while self._running:
            data, addr = await self.sock.recvfrom()
            splitted = decodeB(data).split(' ', 1)
            
            comm = splitted[0]
            comm_body = splitted[1]
            
            if comm[0] == '@':      # Ответы коммандам
                comm_id = int(comm[1:])
                if comm_id in self._process_commands:
                    process_comm = self._process_commands[comm_id]
                    del self._process_commands[comm_id]
                    process_comm.callback(comm_body)
            
            
            else:                   # Сообщения хендлерам
                comm_id = ''
                if comm[0] == "#":
                    comm_id = comm[1:]
                    comm = comm_body.strip()

                if comm in self._handlers.keys():
                    self._handlers[comm].callback( comm_body, addr, comm_id )
                
            
    
    # Повторная отправка комманд не получивших ответа
    async def _handle_responces(self):
        while self._running:
            timeout_comms = []
            
            timenow = time.monotonic() * 1000
            for comm_id, comm in self._process_commands.items():                    
                if timenow > comm.resend_at:
                    comm.push()
                    comm.resend_at = timenow + COMMANDS_RESEND_TIME
                    
                    # Таймаут
                    if timenow - comm.send_at > COMMANDS_TIME_OUT:
                        timeout_comms.append(comm_id)
            
            # Удаление таймаут комманд
            for comm_id in timeout_comms:
                print(f" [ответ от комманды {comm_id} не получен] ")
                del self._process_commands[comm_id]
                    
            await asyncio.sleep(COMMANDS_RECHECK_TIME)
        
    
    def push_command(self, data, callback_handler, addr = None):
        self._comm_id += 1
        if self._comm_id > 32000:
            self._comm_id = 1
        
        push_data =  encodeS( f"#{self._comm_id} {data}" )
                
        command = UDPCommand(
            lambda: self.sock.sendto(push_data, addr= addr),
            callback_handler
        )
        self._process_commands[self._comm_id] = command
        command.push()
        
    def push_answer(self, data, addr, comm_id):
        push_data =  encodeS( f"@{comm_id} {data}" )
        self.sock.sendto(push_data, addr= addr)
        
    def push_message(self, data, addr):
        self.sock.sendto(encodeS(data), addr= addr)
        
    ## Комманда Хендлер - комманда, добавленная принудительно с пометкой handler
    # не удаляется после обработки ответа
    def add_handler(self, id, callback, push = empty_def):
        self._handlers[id] = UDPCommand(push, callback, True)
        
    def call_handler(self, id, data):
        if id in self._handlers:
            self._handlers[id].push(data)
        
    def del_handler(self, id, callback):
        del self._handlers[id]