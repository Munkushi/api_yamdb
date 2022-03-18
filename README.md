### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Munkushi/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source env/scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Используемые технологии:

```
Django REST framework
ReDoc
```

Документация проекта:

```
http://127.0.0.1:8000/redoc/
```

Автор:

```
Даниил Цыганов, Антон Николаев, Иван Сенькин
```
