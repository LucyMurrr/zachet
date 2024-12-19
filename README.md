# zachet
Промежуточная аттестация

ER в .pdf в папке ER

git clone git@github.com:LucyMurrr/zachet.git

    cd zachet

активация виртуального окружения:

    python3 -m venv myenv

    source myenv/bin/activate


Установка зависимостей:

    pip install -r requirements.txt


Внести изменения в database/config.py.

    'user': '<user>',
    
    'password': '<password>',
    
    'host': '<host>',
    
    'port': '<port>'

    
Создание и наполнение базы данных:

    cd zachet/database

    python3 _init_.py

Сообщение в консоли: "База данных 'materials_db' успешно создана."


Проверка наличия БД.

    psql -U <пользователь>

    <password>
  
    \list

    exit


Запуск скриптов на создание таблиц и их наполнение (текущая директория: zachet/database): 

    python3 create_tables.py

    python3 insert_data.py

    python3 import_tables.py


    сd ..


Запуск приложения:

    python3 main.py
