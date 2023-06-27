PROJECT MANAGEMENT OFFICE
=========================

INSTALASI
---------

Clone repo.

```
$ git clone https://<personal-access-token>@github.com/cbmdata/pmo
```

Branch `main` untuk production dan branch `develop` untuk development.

```
$ git checkout develop
```

Setup virtual environment di dalam folder `pmo`. Pastikan command `python` sudah menggunakan Python 3 terbaru. Command `python` dapat diganti dengan mengetik langsung versi python terinstall. Misal `python3.11`.

```
$ cd pmo

# windows
$ python -m venv env
$ .\env\Scripts\activate

# linux
$ virtualenv -p python3 env
$ source env/bin/activate
```

Install python package dan javascript package.

```
$ pip install -r requirements.txt
$ npm install
```

Buat database `pmo` di PostgreSQL.

```
$ psql

user=# create database pmo;
```

Buat file `core/config.py` dengan konfigurasi sebagai berikut:

```
ENGINE = 'django.db.backends.postgresql'
DB = 'pmo'
USER = '<username>'
PASS = '<password>'
HOST = '127.0.0.1'

EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''

DEBUG = True
FORCE_SCRIPT_NAME = '/'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
```

Migrate `account` app terlebih dahulu.

```
$ python manage.py makemigrations account
$ python manage.py migrate account
```

Kemudian, migrate semua app.

```
$ python manage.py migrate
```

Buat akun baru dan aktifkan.

```
$ python manage.py createsuperuser
Email: <your-email>
Password: <your-password>

$ python manage.py shell
>>> from account.models import CustomUser
>>> u = CustomUser.objects.get(email=<your-email>)
>>> u.is_active = True
>>> u.save()
```

DEVELOPMENT
-----------

Buka terminal baru. Jalankan webpack untuk menyiapkan static files (javascript) dan re-compile javascript secara real time ketika ada perubahan.

```
$ npm run watch
```

Jalankan Django

```
$ python manage.py runserver
```
