Парсер товаров Wildberries
Этот проект представляет собой Django-приложение для парсинга данных о товарах с сайта Wildberries и предоставления API для доступа к этим данным с поддержкой фильтрации.
Описание
Проект состоит из:

Парсера: Скрипт, собирающий данные о товарах (название, цена, цена со скидкой, рейтинг, количество отзывов, категория) с сайта Wildberries.
API: Эндпоинт /api/products/ с фильтрацией по цене, рейтингу, количеству отзывов и категории.
Базы данных: SQLite для хранения данных о товарах (можно заменить на другую БД в настройках).

Требования

Python 3.8+
Django 5.1.2
Django REST Framework 3.15.2
requests 2.32.3
beautifulsoup4 4.12.3
fake-useragent 1.5.1

Установка

Клонируйте репозиторий (или создайте структуру проекта вручную):
git clone <repository_url>
cd wildberries_parser


Создайте виртуальное окружение (рекомендуется):
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows


Установите зависимости:
pip install -r requirements.txt


Настройте базу данных:
python manage.py makemigrations
python manage.py migrate


Создайте суперпользователя (для доступа к админ-панели):
python manage.py createsuperuser

Использование

Запустите скрипт парсинга:
python parser/parser_script.py


Введите категорию для парсинга (например, смартфоны).
Скрипт собирает данные о товарах и сохраняет их в базу данных. Для избежания блокировки используются ротация User-Agent и случайные задержки.


Запуск сервера

python manage.py runserver

API доступен по адресу: http://127.0.0.1:8000/api/products/


Примеры API-запросов

Получить все товары:
curl http://127.0.0.1:8000/api/products/


Фильтрация по минимальной цене и рейтингу:
curl "http://127.0.0.1:8000/api/products/?min_price=5000&min_rating=4"


Фильтрация по категории и количеству отзывов:
curl "http://127.0.0.1:8000/api/products/?category=смартфоны&min_reviews=100"


Комбинированная фильтрация:
curl "http://127.0.0.1:8000/api/products/?min_price=1000&max_price=10000&min_rating=3.5&min_reviews=50"



Админ-панель
Доступна по адресу http://127.0.0.1:8000/admin/ после входа с учетной записью суперпользователя. Позволяет просматривать и редактировать данные о товарах.
Возможные проблемы

Ошибка 498 Client Error:

Причина: Wildberries блокирует запросы из-за антибот-защиты.
Решение:
Проверьте сайт в браузере (https://www.wildberries.ru/catalog/0/search.aspx?search=смартфоны).


Лицензия
MIT License
