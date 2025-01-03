import asyncio
import os
import sys
import asyncudp
import json

from Commands import Command

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helper import *

#################################################################################
### CLIENT CONFIG

GREETINGS_COMMAND = 'c'

CODER = "utf-8"

LOCAL_ADDR = ('', 52601)
SERVR_ADDR = ('85.192.26.114', 52600)
#SERVR_ADDR = ('127.0.0.1', 52600)


#################################################################################





class GameClient:
    def __init__(self):
        self._log_stats = {}
        self._log_text = ''
        
    # Печать статистик и всего лога
    def reprint_face(self):
        os.system('cls')
        print(self.get_stats_text())
        print()
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
    
    
    
    
    
    
    async def start_client(self):
        self.sock = await asyncudp.create_socket(remote_addr=SERVR_ADDR)
        
        #await self.do_server_greetings()
        
        asyncio.create_task(self.listen())
        await self.start_input()
    
    async def do_server_greetings(self):
        self.sock.sendto(encodeS(GREETINGS_COMMAND))
        data, addr = await self.sock.recvfrom()
        self.add_log_print(decodeB(data))
            
        
    async def start_input(self):
        while True:
            vvod = input('--> ')
            message = bytes(vvod.encode(CODER))
            self.sock.sendto(message)
            await asyncio.sleep(0.1)
            
    async def listen(self):
        while True:
            data, addr = await self.sock.recvfrom()
            self.clear_log()
            self.add_log(decodeB(data))
            self.add_log_print()


async def main():
    print("Запуск клиента...")
    _gc = GameClient()
    await _gc.start_client()
    

asyncio.run(main())