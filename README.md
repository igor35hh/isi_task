# isi_task

installation process for ubuntu 16.04

virtualenv -p python myproject
source myproject/bin/activate
cd myproject

pip install -r requirements.txt
git clone https://github.com/igor35hh/isi_task

cd isi_task_api

python manage.py makemigrations

python manage.py migrate

python manage.py runserver or python manage.py test