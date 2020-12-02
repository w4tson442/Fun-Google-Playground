#! /bin/bash
virtualenv project_env
source project_env/bin/activate
pip3 install Django
deactivate

sudo rm /etc/apache2/sites-available/000-default.conf
sudo cp apache_config_files/000-default.conf /etc/apache2/sites-available/
sudo service apache2 restart
