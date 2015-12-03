#!/usr/bin/env bash
# Provisioning File for Vagrant
# Installs everything needed for the HiveManagement App
#

#Start with everything updated
sudo apt-get update

#Install Python3 with Pip
sudo apt-get -y install python3-pip

#Setup a virtual environment
# - Make Folder
cd /vagrant/
mkdir /vagrant/venv
# - Install Virtual Environment
sudo -H pip3 install virtualenv
# - Configure Virtual Environment to use Python3
sudo -H virtualenv /vagrant/venv -p python3
# Begin using the virtual environment 
source /vagrant/venv/bin/activate


#Install django
pip install django

#Psycopg2 is a tool that lets Python talk to PostgreSQL
# - First, install its dependencies
sudo apt-get -y install libpq-dev python-dev
# - Install Psycopg2
pip install psycopg2

#Install REST API
pip install djangorestframework

#Install PostgreSQL
sudo apt-get install -y postgresql postgresql-contrib postgresql-9.3-postgis-scripts

sudo -u postgres psql

ALTER USER postgres PASSWORD 'password';
\q

sudo -u postgres createdb BeeManagement


#Install its GEO-Library 
sudo apt-get install -y PostGIS

#Configure this Django superuser
cd /vagrant/

# Install GIT
sudo apt-get -y install git

#Pull the latest project
git clone https://github.com/aadee92/HiveManagement.git

cd ./HiveManagement

python manage.py migrate

python manage.py createsuperuser
 #admin
 #password

python manage.py runserver 0.0.0.0:8000 --noreload


