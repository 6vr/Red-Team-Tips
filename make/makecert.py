import os,sys
import base64
import argparse

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

def certutil_b64encode(src,dest):
    head = "-----BEGIN CERTIFICATE-----\n"
    tail = "-----END CERTIFICATE-----"

    if "/" in src:
        chunks = src.split("/")
        lsrc = chunks[-1]

    e = open(src,'rb')
    exebytes = e.read()
    e.close()
    exebytes_b64 = base64.b64encode(exebytes).decode()
    exebytes_b64chunks = list(chunkstring(exebytes_b64,64))

    certfilename = dest
    with open(certfilename,'w') as f:
        f.write(head)
        for chunk in exebytes_b64chunks:
            f.write(chunk + "\n")
        f.write(tail)
    f.close()
    print('[+] certutil encoded file written: %s\n' % certfilename)
    print("[+] tips to decode certutil encoded file:\n")
    print("certutil -decode .\\%s .\\%s" % (dest,lsrc))
    return certfilename
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--src','-s',required=True,dest='src',help='source filename')
    args = parser.parse_args()

    src = args.src
    dest = "c%s.txt" % src

    if "/" in src:
        chunks = src.split("/")
        last = chunks[-1]
        dest = "c%s.txt" % last

    print("[*] src: %s" % src)
    print("[*] dest (current folder): %s" % dest)
    
    certutil_b64encode(src,dest)
