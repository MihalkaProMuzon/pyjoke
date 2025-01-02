import asyncio
import asyncudp
import json

#################################################################################
### CONFIG

CODER = "utf-8"
LOCAL_ADDR = ('', 52600)
#LOCAL_ADDR = ('127.0.0.1', 35550)


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

def jencodeO(object):
    return json.dumps(object, ensure_ascii=False).encode(CODER)
def encodeS(str):
    return str.encode(CODER)
def decodeB(str):
    return bytes.decode(str, CODER)


class GameServer:
    def __init__(self):
        pass     
        
    async def start_server(self):
        print(f"Слушаемс... {LOCAL_ADDR}")
        self.sock = await asyncudp.create_socket(local_addr= LOCAL_ADDR)
        
        asyncio.create_task(self.listen())
        
        while True:
            print("Я сервер! ЛЯЛЯЛЯЛЯ")
            await asyncio.sleep(2)
        
    async def listen(self):
        while True:
            datas = await self.sock.recvfrom()
            print(datas[0], datas[1])
            await self.handle( datas )
    
    
    async def handle(self, datas):
        print(" <-- handle")
        message, addr = datas
        command = decodeB(message).split(' ')
        print(f' -- {command}')
        if command[0] == 'c':
            self.sock.sendto(jencodeO(COMMANDS), addr)
            print("Выслал комманды")
            
    


async def main():
    print("Запуск сервера...")
    _gs = GameServer()
    await _gs.start_server()
    

asyncio.run(main())