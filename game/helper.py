import json
import platform
import os

CODER = "utf-8"


__print_added = False
def print_adv(*args):
    global __print_added
    print('\r', end= '')
    print(*args)
    __print_added = True

deb_candy = ['\\','|','/', '—']
deb_candy_pos = 0
def print_deb_candy():
    global __print_added, deb_candy_pos, deb_candy
    if __print_added:
        print('')
    
    __print_added = False
    print('\r', end= '')
    print(f" > {deb_candy[deb_candy_pos]}", end='  ')
    deb_candy_pos+=1
    deb_candy_pos = deb_candy_pos%4
    
    
def jsondumps(object):
    return json.dumps(object, separators=(',', ':') ,ensure_ascii=False)
def jsonloads(string):
    return json.loads(string)

def encodeS(str):
    return str.encode(CODER)
def decodeB(str):
    return bytes.decode(str, CODER)


def clear_console():
    if platform.system() == "Windows":
        pass
        os.system('cls')
    else:
        pass
        os.system('clear')