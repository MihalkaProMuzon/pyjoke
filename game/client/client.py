import asyncio
import os
import sys
import asyncudp


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helper import *
from Commands import Messanger
from gamedata.Game import Game

#################################################################################
### CLIENT CONFIG

GREETINGS_COMMAND = 'greetings'

CODER = "utf-8"

LOCAL_ADDR = ('', 52601)
SERVER_ADDR = ('85.192.26.114', 52600)
#SERVER_ADDR = ('127.0.0.1', 52600)


#################################################################################

class UPDClient:
    def __init__(self):
        self._log_stats = {}
        self._log_text = ''
        self.messanger: Messanger = None
        
    # Печать статистик и всего лога
    def reprint_face(self):
        os.system('cls')
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
    
    async def start_client(self):
        self.sock = await asyncudp.create_socket(remote_addr=SERVER_ADDR)
        self.sock_addr, self.sock_port = self.sock.getsockname()
        self.add_stat('sock', f"socket --E {self.sock_addr}:{self.sock_port}")
    
    
        self.messanger = Messanger(self.sock)
    
        self.reprint_face()
        self.input_task = asyncio.create_task(self.handle_input())
        self.do_server_greetings()
        
        await self.input_task
            
    def do_server_greetings(self):
        self.messanger.push_command(GREETINGS_COMMAND,self.simple_message_callback)
        
    async def handle_input(self):
        while True:
            await asyncio.sleep(0.25)
            vvod = await asyncio.get_event_loop().run_in_executor(None, input, " --> ") + ' '
            if vvod != '' and vvod != ' ':
                self.clear_log()
                self.add_log_print(' ... ')
                self.messanger.push_command( vvod, self.simple_message_callback )
                
    #******************************************************************************

    def simple_message_callback(self, response):
        self.clear_log()
        self.add_log_print(response)

#################################################################################

async def main():
    udpclient = UPDClient()
    game = Game()
    await asyncio.gather(
        game.start_game(),
        udpclient.start_client()
    )

asyncio.run(main())