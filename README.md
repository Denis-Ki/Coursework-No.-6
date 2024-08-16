
Kichulkin Denis Coursework_6_Django 
В ссответствии с условиями курсовой работы № 6 (SkyPro)
Приложение Mailing ("Посылкин") - это сервис по созданию рассылок

Описание
Проект позволяет создавать рассылки, которые сервис будет автоматически отправлять заданным клиентам через определенные промежутки времени.

Используемые технологии: Django, Python, PostgreSQL, Redis. Необходимое виртуальное окружение прописано в requirements.txt.

Для запуска проекта необходимо:

1) Создать файл .env и внесите свои данные, все необходимые переменные перечислены в файле .env.sample
2) Создать и применить миграции камандами "python3 manage.py makemigrations" и "pytho3n manage.py migrate"
3) Установить и запустить Redis в отдельном терминале
4) Для старта проекта введите команду в командрой строке pycharm "python3 manage.py runserver"
5) Во втором терминале ввести команду "pycharm python3 manage.py start_scheduler" это запустит сервер рассылки 
6) Зарегистрироваться на сайте (либо командой csu), написать сообщение, добавьте клиентов, создайте рассылку
7) Для ручного запуска рассылок можно использовать команду python3 manage.py mail_start
 

Для заполнения базы данных можно использовать фикстуры blod_data.json и mailing_data.json.
Для создания суперпользователя можно использовать команду csu, для создания группы - create_groups

