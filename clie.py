import asyncio
import asyncudp
import json

#################################################################################
### CLIENT CONFIG

COMMANDS_MESSAGE = 'c'

CODER = "utf-8"

LOCAL_ADDR = ('127.0.0.1', 35551)
SERVR_ADDR = ('10.66.66.1', 52500)
#SERVR_ADDR = ('127.0.0.1', 35550)


#################################################################################

def jencodeO(object):
    return json.dumps(object).encode(CODER)
def encodeS(str):
    return str.encode(CODER)

def jdecodeB(object):
    return json.loads(decodeB(object))
def decodeB(str):
    return bytes.decode(str, CODER)


class GameClient:
    def __init__(self):
        pass
    
    async def start_client(self):
        self.sock = await asyncudp.create_socket(local_addr= LOCAL_ADDR,remote_addr= SERVR_ADDR)  
        
        print("Запущен")
        await self.request_commands()
        
        asyncio.create_task(self.listen())
        await self.start_spam()
    
    async def request_commands(self):
        self.sock.sendto(encodeS(COMMANDS_MESSAGE))
        data, addr = await self.sock.recvfrom()
        data = jdecodeB(data)
        for k, v in data.items():
            print(f"  ~ {k} - {v}")
        print()
            
        
    async def start_spam(self):
        while True:
            vvod = input('--> ')
            message = bytes(vvod.encode(CODER))
            self.sock.sendto(message)
            await asyncio.sleep(0.5)
            
    async def listen(self):
        while True:
            data, addr = await self.sock.recvfrom()
            print(decodeB(data))


async def main():
    print("Запуск клиента...")
    _gc = GameClient()
    await _gc.start_client()
    

asyncio.run(main())