```
sudo echo "CustomLog /var/log/apache2/access.log combined" >> /etc/apache2/apache2.conf
sudo service apache2 restart
sudo tail -f /var/log/apache2/access.log
```
