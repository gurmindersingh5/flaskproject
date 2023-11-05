#!/bin/bash

# Update and upgrade packages
sudo apt-get update
sudo apt-get upgrade -y

# Install Apache2
sudo apt-get install -y apache2

# Clone your Git repository
cd /var/www/
git clone https://github.com/gurmindersingh5/flaskproject.git

# Set up a Python virtual environment
sudo python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip3 install -r flaskproject/requirements.txt
pip install -r /var/www/flaskproject/requirements.txt

# Install mod_wsgi for Python 3
sudo apt-get install -y libapache2-mod-wsgi-py3

# Configure the Apache2 Virtual Host
sudo touch /etc/apache2/sites-available/flaskproject.conf

echo "<VirtualHost *:80>
                ServerName "public-ipv4 address here"
                ServerAdmin email@mywebsite.com
                WSGIScriptAlias / /var/www/flaskproject/flaskproject.wsgi
                <Directory /var/www/flaskproject/flask_pkg>
                        Order allow,deny
                        Allow from all
                </Directory>
                Alias /static /var/www/flaskproject/flask_pkg/static
                <Directory /var/www/flaskproject/flask_pkg/static/>
                        Order allow,deny
                        Allow from all
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>" > /etc/apache2/sites-available/flaskproject.conf

# Enable the Virtual Host
sudo a2ensite flaskproject

# Reload Apache to apply changes
sudo systemctl reload apache2

# Create and configure the WSGI script
touch /var/www/flaskproject/flaskproject.wsgi

echo "#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/flaskproject')

from flask_pkg import app as application
application.secret_key='secret123'" > /var/www/flaskproject/flaskproject.wsgi

# Restart Apache2
sudo service apache2 restart
