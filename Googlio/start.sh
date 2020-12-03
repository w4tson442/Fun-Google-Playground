#! /bin/bash
sudo mysql -e "create database isekai;"
sudo mysql -e "create user 'isekai'@'localhost' identified by 'test123';"
sudo mysql -e "grant all privileges on isekai.* to 'isekai'@'localhost';"
sudo mysql -e "flush privileges;"

virtualenv project_env
source project_env/bin/activate
pip3 install Django
sudo apt-get install -y libmysqlclient-dev
sudo apt-get install -y libssl-dev
pip3 install mysqlclient
deactivate

sudo rm /etc/apache2/sites-available/000-default.conf
sudo cp apache_config_files/000-default.conf /etc/apache2/sites-available/
sudo service apache2 restart
