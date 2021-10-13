# vimeo-coursetool
Vimeo based online course system
developed by N.Kawaguchi (2021)

This tool is used for TMI, Nagoya University

This is Django based vimeo online media course tool.

## Install
install python (> 3.8)

pip install -r requirements.txt

## Starting Development Server
python3 manage.py makemigration
python3 manage.py migrate

### port 3000 by nginx reverse proxy
python3 manage.py runserver 3000
