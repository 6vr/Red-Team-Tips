import os,sys,re
import argparse

def nmap_fulltcp(ip,force):
    #'''
    if not os.path.exists('scans'):
        print('[+] created folder ./scans')
        os.makedirs('scans')
    if force == "0":
        if not os.path.isfile('scans/nmap-alltcp_%s.txt' % ip):
            print ('[+] enumerating ports on %s' % ip)
            os.system('nmap -Pn -p- --min-rate 10000 -oN scans/nmap-alltcp_%s.txt %s' % (ip,ip))
        else:
            dec = input('[!] ./scans/nmap-alltcp_%s.txt already exists -> continue? (y/N)' % ip)
            if dec == "y":
                os.system('nmap -Pn -p- --min-rate 10000 -oN scans/nmap-alltcp_%s.txt %s' % (ip,ip))
    if force == "1":
        print ('[+] enumerating ports on %s' % ip)
        os.system('nmap -Pn -p- --min-rate 10000 -oN scans/nmap-alltcp_%s.txt %s' % (ip,ip))

    #'''
    ports = []
    #pat = '^[0-9]{2,5}\/tcp.*$'
    with open('scans/nmap-alltcp_%s.txt' % ip,'r') as f:
        line = f.readline().rstrip()
        while line != "":
            #res = re.match(pat, line)
            if "/tcp" in line:
                p = (line.split("/tcp")[0])
                ports.append(p)
                line = f.readline()
            else:
                line = f.readline()
                #print('[DEBUG] line: %s' % line)
            #line = f.readline()
    f.close()
    ports = ','.join(ports)
    #print ('[DEBUG] ports: %s' % ports)
    #'''
    if force == "0":
        if not os.path.isfile('scans/nmap-tcpscans_%s.txt' % ip):
            os.system('nmap -Pn -v -p %s -sCV -oN scans/nmap-tcpscans_%s.txt %s' % (ports,ip,ip))
        else:
            dec = input('[!] ./scans/nmap-tcpscans_%s.txt already exists -> continue? (y/N)' % ip)
            if dec == "y":
                os.system('nmap -Pn -v -p %s -sCV -oN scans/nmap-tcpscans_%s.txt %s' % (ports,ip,ip))
    if force == "1":
        os.system('nmap -Pn -v -p %s -sCV -oN scans/nmap-tcpscans_%s.txt %s' % (ports,ip,ip))
    pass
    #'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--target','-t',required=True,dest='target',help='provide ip addresses! split by commas, e.g. 10.10.14.14, 10.14.14.15.')
    parser.add_argument('--force','-f',required=False,dest='force',help='0 or 1')
    args = parser.parse_args()

    target = args.target
    force = args.force

    if force == None:
        force = "0"
    if force != "0":
        force = "1"

    target = target.split(',')

    ip_list = target
    for ip in ip_list:
        nmap_fulltcp(ip,force)
