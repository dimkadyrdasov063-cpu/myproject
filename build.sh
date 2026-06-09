#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='astzxc').exists():
    User.objects.create_superuser('astzxc', 'asdqweq3@gmail.com', '12345678')
"