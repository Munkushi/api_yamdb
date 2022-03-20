***Как запустить проект:***

Клонировать репозиторий и перейти в него в командной строке:


git clone git@github.com:Munkushi/api_yamdb.git

cd api_yamdb


**Cоздать и активировать виртуальное окружение:**


python -m venv env - для windows
python3 -m venv venv - для mac/linux

source env/scripts/activate

**Установить зависимости из файла requirements.txt:**

python3 -m pip install --upgrade pip - для mac/linux
python3 -m pip install --upgrade pip -для windows

pip install -r requirements.txt

**Выполнить миграции:**

python3 manage.py migrate - для   mac/linux
python manage.py migrate - для windows

**Запустить проект:**

python3 manage.py runserver - для   mac/linux
python manage.py migrate - для windows

**Используемые технологии:**

Django REST framework
ReDoc

**Документация проекта:**

http://127.0.0.1:8000/redoc/

**Авторы:**

Даниил Цыганов, Антон Николаев, Иван Сенькин


