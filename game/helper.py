import json

CODER = "utf-8"


print_added = False
def print_adv(*args):
    global print_added
    print('\r', end= '')
    print(*args)
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
def jdecodeB(object):
    return json.loads(decodeB(object))
def encodeS(str):
    return str.encode(CODER)
def decodeB(str):
    return bytes.decode(str, CODER)