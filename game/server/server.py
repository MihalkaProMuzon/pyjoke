import asyncio
import enum
import os
import subprocess
import sys
import asyncudp

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helper import *

from UDPCommands import Messanger, ServerCommands
from meeting import Room

#################################################################################
### CONFIG

#LOCAL_ADDR = ('85.192.26.114', 52600)
LOCAL_ADDR = ('127.0.0.1', 52600)
PROJ_VERSION = "v.rooms-setup.8"
PYTHON_PATH = '../../../../python'

#################################################################################
print(f"\n\n>> pohg server [{PROJ_VERSION}] <<" )
#################################################################################


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

class Client():
    _clients_uid = 0
    def get_new_uid():
        Client._clients_uid = Client._clients_uid + 1
        return Client._clients_uid
    
    def __init__(self, addr, room = None):
        self._id = Client.get_new_uid()
        self._addr = addr
        
        self.room = room
        
    def get_id(self):
        return self._id
    def get_addr(self):
        return self._addr
    def get_addr_str(self):
        return str(self._addr)
        


class GameServer:
    
    def __init__(self):
        self._rooms = {}
        self._clients = {}
        self._clients_by_addresses = {}
        
        self._sock_udp = None
        self._messanger = None
      
        
    # SERVER_INIT ****************************************************************
    
    async def start_server(self):
        clear_console()
        
        print_adv(f"Слушаемс... {LOCAL_ADDR}")
        self._sock_udp = await asyncudp.create_socket(local_addr= LOCAL_ADDR)
        self._messanger = Messanger(self._sock_udp)
        
        self._bind_command_handlers()
        
        while True:
            print_deb_candy()
            await asyncio.sleep(0.2) 
    
    # COMMAND_HANDLERS ***********************************************************
    
    def _greetings_comhandler(self, comm_body, addr, comm_id):
        print_adv(f"greetings! {addr} #{comm_id}")
        self._messanger.push_answer(f"-≡ Server [{PROJ_VERSION}]", addr, comm_id)
        
    def _test1_comhandler(self, comm_body, addr, comm_id):
        print_adv("test1")
        self._messanger.push_answer("Server response1 o-O", addr, comm_id)
        
    def _test2_comhandler(self, comm_body, addr, comm_id):
        print_adv("test2")
        self._messanger.push_answer("Response2 from server ;)", addr, comm_id)
        
    def _update_comhandler(self, comm_body, addr, comm_id):
        self._messanger.push_answer("Server confirm update command", addr, comm_id)
        
        comm_body = comm_body.split(' ')
        branch = '' if len(comm_body) < 2 else comm_body[2]
        Updater.update_project(branch)
        
    
    
    def _get_rooms_comhandler(self, comm_body, addr, comm_id):
        self._messanger.push_answer( jsondumps(self.get_free_rooms()) , addr, comm_id)        
        
    def _create_room_comhandler(self, comm_body, addr, comm_id):
        print_adv("here")
        room, client = self.create_room(addr)
        answer_data =  {
            "r": room.get_id(),
            "c": client.get_id()
        }
        print(f"> {room.get_id()}")
        print(f"")
        
        
        self._messanger.push_answer( jsondumps(answer_data) , addr, comm_id)
        print_adv(f"Создал комнату {answer_data["r"]} для клиента {answer_data["c"]}")
    
    
    def _bind_command_handlers(self):
        mssr = self._messanger
        mssr.add_handler(ServerCommands.greetings.name, self._greetings_comhandler)
        mssr.add_handler(ServerCommands.test1.name, self._test1_comhandler)
        mssr.add_handler(ServerCommands.test2.name, self._test2_comhandler)
        mssr.add_handler(ServerCommands.update.name, self._update_comhandler)
        mssr.add_handler(ServerCommands.get_rooms.name, self._get_rooms_comhandler)
        mssr.add_handler(ServerCommands.create_room.name, self._create_room_comhandler)
    
    
    
    # LOGIC **********************************************************************
        
    def get_free_rooms(self):
        return [ room for room in self._rooms if not room.full ]
        
    def create_room(self, addr):
        client1 = Client(addr)
        client1_id = client1.get_id()
        self._clients[client1_id] = client1        
        self._clients_by_addresses[client1.get_addr_str()] = client1
        
        newroom = Room(client1_id)
        newroom_id = newroom.get_id()
        self._rooms[newroom_id] = newroom
        
        print("ffd")
        
        return (newroom, client1)
    
    def del_room(self, room_id):
        room = self._rooms[room_id]
        for client_id in room.get_clients():
            del self._clients_room_mapping[client_id]
            
            client:Client = self._clients[client_id]
            del self._clients_by_addresses[client.get_addr_str()]
            
        del self._rooms[room_id]
    
    
    # def append_to_room(self, room_id):
    #     room:Room = self._rooms[room_id]
    #     if not room: 
    #         return False
    #     if room.full:
    #         return False
        
    #     client_id = GameServer.get_new_uid()
        
    #     room.add_client(client_id)
    #     self._clients_room_mapping[client_id] = room_id
    #     # # # > Отправить клиентам актуальную информацию о комнатах
    
    def get_room_by_client_id(self):
        pass
            
            
            
        
            
    #******************************************************************************


async def main():
    print_adv("Запуск сервера...")
    _gs = GameServer()
    await _gs.start_server()
    

asyncio.run(main())