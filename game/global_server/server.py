import asyncio
import enum
import os
import subprocess
import sys
import asyncudp

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helper import *

#################################################################################
### CONFIG

LOCAL_ADDR = ('85.192.26.114', 52600)
#LOCAL_ADDR = ('127.0.0.1', 52600)
PROJ_VERSION = "v.commands-upgrade.2"
PYTHON_PATH = '../../../../python'

#################################################################################
print(f"\n\n>> pohg server [{PROJ_VERSION}] <<" )
#################################################################################


# Комманды, высылаемые клиенту
@enum.unique
class Commands(enum.Enum):
    greetings = 'Приветствие от сервера'
    create_room = 'Встать в очередь (arg1 = моё имя)'
    get_rooms = 'Показать очередь'
    connect_room = 'Присоедениться к игроку (arg1 = имя игрока, arg2 = моё имя)'
    test1 = 'Проверка связи 1'
    test2 = 'Проверка связи 2'
    update = 'Обновить сервер'


class Updater:
    def update_project(branch_name = ''):
        try:
            subprocess.run(['git', 'pull'], check=True)
            if branch_name != '':
                subprocess.run(['git', 'checkout', branch_name], check=True)
            
            print("Перезапуск программы...")
            os.execv(sys.executable, [PYTHON_PATH] + sys.argv)
            
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при обновлении: {e}")
        except Exception as e:
            print(f"Произошла ошибка при обновлении: {e}")



class GameServer:
    def __init__(self):
        self.rooms = {}
        self.uid = 1
    
    ### Инициализация сервера    
    async def start_server(self):
        print_adv(f"Слушаемс... {LOCAL_ADDR}")
        self.sock_udp = await asyncudp.create_socket(local_addr= LOCAL_ADDR)
        
        asyncio.create_task(self.listen())
        
        while True:
            print_deb_candy()
            await asyncio.sleep(0.2)
        
    ### Корутина прослушки сокета
    async def listen(self):
        while True:
            datas = await self.sock_udp.recvfrom()
            print_adv(datas[0], datas[1])
            self.handle( datas )
    
    ### Обработка комманд
    def handle(self, datas):
        message, addr = datas
        command = decodeB(message).split(' ')
        print_adv(f' ---> {command}')
        
        # Комманды, ждущие ответ
        if command[0][0] == "@":
            comm_id = int(command[0][1:])
            comm_message = command[1]
            
            def answer(message):
                self.sock_udp.sendto( encodeS( f"{command[0]} {message}" ), addr)
            
            # Приветсвие от сервера
            if comm_message == Commands.greetings.name:
                print("greetings!")
                answer(f"-≡ Server [{PROJ_VERSION}]")
        
            # Проверка связи
            if comm_message == Commands.test1.name:
                print("test1")
                answer("Server response1 o-O")
            if comm_message == Commands.test2.name:
                print("test2")
                answer("Response2 from server ;)")
                
            if comm_message == Commands.update.name:
                answer("server confirm update command")
                branch = ''
                if len(command) > 2:
                    branch = command[2]
                Updater.update_project(branch)
                
                
            
        
            
    #******************************************************************************


async def main():
    print_adv("Запуск сервера...")
    _gs = GameServer()
    await _gs.start_server()
    

asyncio.run(main())