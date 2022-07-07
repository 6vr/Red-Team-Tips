import os,sys
import base64
import argparse
import random

default_quantity = 1000

def permutations(length):
    numbers = ["1","2","3","4","5","6","7","8","9","0"]
    #specs = ["!","@","#","$","%","^","&","*","(",")","-","_","+","=","[","]","{","}",":",";","<",">",",",".","/","?","~","`"]
    specs = ["!","@","#","$","%"] # more like human behaviour

    chars = numbers + specs
    length = int(length)

    res = []
    for i in range(default_quantity):
        for j in range(1,length+1):
            ires = random.choices(chars,k=j)
            ires = ''.join(ires)
            res.append(ires)
    return res

def writepasswords(src,dest,length,suffix,prefix):
    passwords = []

    lines = open(src, encoding="ISO-8859-1").read().splitlines()
    for line in lines:
        if len(line) >= int(length):
            passwords.append(line)
            if suffix != "0":
                perms = permutations(suffix)
                #print("[*] DEBUG")
                #print(perms)
                for perm in perms:
                    passwords.append(line+perm)

    passwords = list(set(passwords))
    with open(dest,'w') as f:
        for ipass in passwords:
            f.write("%s\n" % ipass)
    f.close()

    print('[+] password file length: %s' % str(len(passwords)))
    print('[+] password file written: %s' % (dest))
    pass

def makepasswords(src,dest,length,suffix,prefix):
    writepasswords(src,dest,length,suffix,prefix)
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--src','-s',required=True,dest='src',help='source filename')
    parser.add_argument('--len','-l',required=True,dest='length',help='target min length')
    parser.add_argument('--suffix','-u',required=False,dest='suffix',help='target min suffix length')
    parser.add_argument('--prefix','-p',required=False,dest='prefix',help='target min prefix length')
    
    args = parser.parse_args()

    src = args.src
    length = args.length
    suffix = args.suffix
    prefix = args.prefix

    dest = "o%s" % src

    if length == None:
        length = "0"
    if suffix == None:
        suffix = "0"
    if prefix == None:
        prefix = "0"

    if "/" in src:
        chunks = src.split("/")
        last = chunks[-1]
        dest = "o%s" % last

    print("[*] src: %s" % src)
    print("[*] dest (current folder): %s" % dest)
    
    makepasswords(src,dest,length,suffix,prefix)