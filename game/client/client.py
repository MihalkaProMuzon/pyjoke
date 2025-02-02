import asyncio
import os
import sys
import asyncudp


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helper import *
from UDPCommands import Messanger
from gamedata.Game import Game

#################################################################################
### CLIENT CONFIG

GREETINGS_COMMAND = 'greetings'

CODER = "utf-8"

LOCAL_ADDR = ('', 52601)
#SERVER_ADDR = ('85.192.26.114', 52600)
SERVER_ADDR = ('127.0.0.1', 52600)


#################################################################################

class UPDClient:
    def __init__(self):
        self._log_stats = {}
        self._log_text = ''
        
        self._messanger: Messanger = None
        self._game: Game = None
        
        self._sock = None
        self._sock_addr = None
        self._sock_port = None
        self._input_task = None
        
        self._room_id = None
        self._client_id = None
        
        self._command_callbacks = {}
        self._bind_command_callbacks()
        
    # Печать статистик и всего лога
    def reprint_face(self):
        clear_console()
        print(self.get_stats_text())
        print("________________________________________")
        print()
        print(self._log_text)
        
    # Добавить лог (без печати)
    def add_log(self, *text):
        for txt in text:
            self._log_text += txt
        self._log_text += '\n'
        
    # Добавить лог и напечатать
    def add_log_print(self, *text):
        self.add_log(*text)
        self.reprint_face()
    
    # Сформировать текст статтов
    def get_stats_text(self):
        print('  X< клиент pohg >X\n')
        txt = ''
        for k,v in self._log_stats.items():
            txt += f"{v}\n"
        return txt
            
    # Добавить стат
    def add_stat(self, stat_key, stat_value):
        self._log_stats[stat_key] = stat_value           
        self.reprint_face()
        
    # Убрать стат
    def remove_stat(self, stat_key):
        del self._log_stats[stat_key]
        self.reprint_face()
        
    # Очистить лог
    def clear_log(self):
        self._log_text = ''
        
    #******************************************************************************
    
    async def start_client(self, game):
        self._sock = await asyncudp.create_socket(remote_addr=SERVER_ADDR)
        self._sock_addr, self._sock_port = self._sock.getsockname()
        self.add_stat('sock', f"socket --E {self._sock_addr}:{self._sock_port}")
    
        self._messanger = Messanger(self._sock)
        self._game = game
    
        self.reprint_face()
        self._input_task = asyncio.create_task(self._handle_input())
        self._do_server_greetings()
        
        await self._input_task
            
    def _do_server_greetings(self):
        self._messanger.push_command(GREETINGS_COMMAND,self._default_message_callback)
        
    async def _handle_input(self):
        while True:
            await asyncio.sleep(0.25)
            #vvod = await asyncio.get_event_loop().run_in_executor(None, input, " --> ")
            vvod = ' '
            if vvod != " ":
                comm = vvod.split(' ', 1)[0]
                                
                self.clear_log()
                self.add_log_print(f" ... {comm}")
                calbak = self._command_callbacks.get(
                    comm, self._command_callbacks['_default']
                )
                self._messanger.push_command( vvod, calbak )
                
    # COMMAND_CALLBACKS ***********************************************************
    
    def _default_message_callback(self, response):
        self.clear_log()
        self.add_log_print(response)
    
    def _get_rooms_callback(self, response):
        self.clear_log()
        
        rooms = jsonloads(response)
        if len(rooms) < 1:
            self.add_log_print(f"В настоящий момент нет комнат для подключения")        
        else:
            self.add_log_print(f"Пришли комнатушки: {rooms}")
            
    def _create_room_callback(self, response):
        self.clear_log()
        
        room_data = jsonloads(response)
        if len(room_data.keys()) > 1:
            
            self._client_id = room_data["c"]
            self._room_id = room_data["r"]
            self.add_stat("client_id", f"Идентификатор клиента: {self._client_id}")
            self.add_stat("room_id", f"Команата: {self._room_id}")
            self.add_log(f"Вход в комнату №{self._room_id}")
            self.reprint_face()
        
        
    def _bind_command_callbacks(self):
        scb = {
            "_default": self._default_message_callback,
            "get_rooms": self._get_rooms_callback,
            "create_room": self._create_room_callback,
        }
        self._command_callbacks = scb

#################################################################################

async def main():
    udpclient = UPDClient()
    game = Game()
    await asyncio.gather(
        game.start_game(udpclient),
        udpclient.start_client(game)
    )

asyncio.run(main())