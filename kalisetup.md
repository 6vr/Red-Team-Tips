### set static ip on vmware fusion
```
sudo nano /Library/Preferences/VMware\ Fusion/vmnet8/dhcpd.conf
host kalilinux {
 hardware ethernet 00:0c:29:ea:9e:42;
 fixed-address 192.168.135.7;
}
```

### make kali sudo without pwd
```
sudo echo "kali    ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
```
### apache logging
```
sudo echo "CustomLog /var/log/apache2/access.log combined" >> /etc/apache2/apache2.conf
sudo service apache2 restart
sudo tail -f /var/log/apache2/access.log
```
### setup samba
```
sudo apt install samba
sudo mv /etc/samba/smb.conf /etc/samba/smb.conf.old
sudo nano /etc/samba/smb.conf

[visualstudio]
path = /home/kali/data
browseable = yes
read only = no

sudo smbpasswd -a kali

sudo systemctl start smbd
sudo systemctl start nmbd

mkdir /home/kali/data
chmod -R 777 /home/kali/data
```
### /opt repos (not complete, see optlist.txt)
```
sudo chown -R kali:kali /opt
git clone https://github.com/rvrsh3ll/FindFrontableDomains
git clone https://github.com/danielbohannon/Invoke-Obfuscation
git clone https://github.com/ajinabraham/Node.Js-Security-Course
git clone https://github.com/pwntester/ysoserial.net
git clone https://github.com/PowerShellMafia/PowerSploit
git clone https://github.com/GhostPack/SharpUp
git clone https://github.com/CiscoCXSecurity/creddump7
git clone https://github.com/411Hall/JAWS
```
### [bloodhound](https://bloodhound.readthedocs.io/en/latest/installation/linux.html)
```
mkdir /opt/BloodHound
echo "deb http://httpredir.debian.org/debian stretch-backports main" | sudo tee -a /etc/apt/sources.list.d/stretch-backports.list
sudo apt-get update
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo "deb https://debian.neo4j.com stable 4.0" | sudo tee -a /etc/apt/sources.list.d/neo4j.list
sudo apt-get update
sudo apt-get install apt-transport-https
sudo apt-get install neo4j
sudo systemctl stop neo4j
sudo /usr/bin/neo4j console
cd /opt/BloodHound
wget https://github.com/BloodHoundAD/BloodHound/releases/download/4.0.3/BloodHound-linux-x64.zip
unzip BloodHound-linux-x64.zip
mv BloodHound-linux-x64 bin
git clone https://github.com/BloodHoundAD/BloodHound
```
```
sudo neo4j console
localhost:7474
neo4j / neo4j
```
```
sudo neo4j console
sudo /opt/BloodHound/bin/BloodHound --no-sandbox
```
### python crypto
```
sudo apt-get install python-dev
wget https://ftp.dlitz.net/pub/dlitz/crypto/pycrypto/pycrypto-2.6.1.tar.gz
tar -xvzf pycrypto-2.6.1.tar.gz
cd pycrypto-2.6.1
python setup.py build
sudo python setup.py build install
```
### sublime text [sauce](https://www.sublimetext.com/docs/linux_repositories.html)
```
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
sudo apt-get install apt-transport-https
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
sudo apt-get update
sudo apt-get install sublime-text
```

### oletools [sauce](https://github.com/decalage2/oletools)
```
sudo -H pip install -U oletools
```

### covenant ([dotnet](https://docs.microsoft.com/en-us/dotnet/core/install/linux-debian))([covenant](https://github.com/cobbr/Covenant/wiki/Installation-And-Startup))([overall](https://hakin9.org/covenant-the-net-based-c2-on-kali-linux/)) (make sure to install dotnet 3.1!)
```
wget https://packages.microsoft.com/config/debian/10/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb
sudo apt-get update; \
  sudo apt-get install -y apt-transport-https && \
  sudo apt-get update && \
  sudo apt-get install -y dotnet-sdk-3.1
cd /opt/
git clone --recurse-submodules https://github.com/cobbr/Covenant
cd /opt/Covenant/Covenant
dotnet build
dotnet run
https://127.0.0.1:7443
j4ckie
```

### mono
```
sudo apt-get install mono-complete
```

### sharpshooter
```
sudo pip install jsmin
sudo cp -r /usr/local/lib/python3.9/dist-packages/jsmin* /usr/local/lib/python2.7/dist-packages
https://raw.githubusercontent.com/tikitu/jsmin/e87a6f3b1490e2643cbcdef77e41840c94f9e788/jsmin/__init__.py
sudo vi /usr/local/lib/python2.7/dist-packages/jsmin/__init__.py
import cStringIO
sudo vi /opt/SharpShooter/SharpShooter.py
ss_path = "/opt/SharpShooter/"
ctrl+f template_base
template_base = ss_path + "templates/sharpshooter."
ctrl+f templates/
harness = self.read_file(ss_path + "templates/harness.js")
mkdir output in current directory
```

### squid server
```
sudo apt-get install squid
sudo vi /etc/squid/squid.conf
http_access allow all
sudo service squid restart
sudo service squid start
sudo service squid status
netstat -antl | grep LISTEN
```
