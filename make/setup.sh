sudo systemctl start nmbd && sudo systemctl start smbd
echo "[+] nmbd and smbd started"
sudo service apache2 start
echo "[+] apache2 started"
sudo chown -R kali:kali /var/www/html
echo "[+] normalized /var/www/html ownership"
sudo chown -R kali:kali /opt
echo "[+] normalized /opt ownership"
sudo msfdb start
echo "[+] msfdb started"
