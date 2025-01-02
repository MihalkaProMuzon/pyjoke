import asyncio
import inspect
import os
import subprocess
import sys
import asyncudp
import json

#################################################################################
### CONFIG

CODER = "utf-8"
LOCAL_ADDR = ('85.192.26.114', 52600)
#LOCAL_ADDR = ('127.0.0.1', 52600)

PROJ_VERSION = "v.main.5"

PYTHON_PATH = '../../python'

COMMANDS = {
    'create_room': u"Создать комнату",
    'rooms': u"Показать все комнаты",
    'c': u'Список комманд'
}


#################################################################################
###                     ###
    ### POHG SERVER ###
print(">> pohg server <<")
###                     ###

print_added = False

def print_adv(*text):
    global print_added
    print('\r', end= '')
    print(*text)
    print_added = True

deb_candy = ['\\','|','/', '—']
deb_candy_pos = 0
def print_deb_candy():
    global print_added, deb_candy_pos, deb_candy
    if print_added:
        print('')
    
    print_added = False
    print('\r', end= '')
    print(f" > {deb_candy[deb_candy_pos]}", end='')
    deb_candy_pos+=1
    deb_candy_pos = deb_candy_pos%4

def jencodeO(object):
    return json.dumps(object, ensure_ascii=False).encode(CODER)
def encodeS(str):
    return str.encode(CODER)
def decodeB(str):
    return bytes.decode(str, CODER)


class Updater:
    def update_project(branch_name = ''):
        try:
            if branch_name != '':
                subprocess.run(['git', 'checkout', branch_name], check=True)
            subprocess.run(['git', 'pull'], check=True)
            
            print("Перезапуск программы...")
            os.execv(sys.executable, [PYTHON_PATH] + sys.argv)
            
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при обновлении: {e}")
        except Exception as e:
            print(f"Произошла ошибка при обновлении: {e}")

class GameServer:
    def __init__(self):
        pass     
        
    async def start_server(self):
        print_adv(f"{PROJ_VERSION}")
        print_adv(f"Слушаемс... {LOCAL_ADDR}")
        self.sock = await asyncudp.create_socket(local_addr= LOCAL_ADDR)
        
        asyncio.create_task(self.listen())
        
        while True:
            print_deb_candy()
            await asyncio.sleep(0.2)
        
    async def listen(self):
        while True:
            datas = await self.sock.recvfrom()
            print_adv(datas[0], datas[1])
            await self.handle( datas )
    
    
    async def handle(self, datas):
        message, addr = datas
        command = decodeB(message).split(' ')
        print_adv(f' -- {command}')
        if command[0] == 'c':
            self.sock.sendto(jencodeO(COMMANDS), addr)
            print_adv("Выслал комманды")
        if command[0] == 'update':
            Updater.update_project(command[1])
            
    


async def main():
    print_adv("Запуск сервера...")
    _gs = GameServer()
    await _gs.start_server()
    

asyncio.run(main())