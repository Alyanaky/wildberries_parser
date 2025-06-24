# parser/parser_script.py
import requests
import sys
import os
import django
from datetime import datetime
from bs4 import BeautifulSoup
from django.db import transaction
import time
import random
from fake_useragent import UserAgent

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wildberries_parser.settings')
    django.setup()

from parser.models import Product

def parse_wildberries(category, max_pages=3):
    ua = UserAgent()
    session = requests.Session()
    headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }
    base_url = 'https://www.wildberries.ru'
    search_url = f'{base_url}/catalog/0/search.aspx?search={category.replace(" ", "+")}'

    for page in range(1, max_pages + 1):
        try:
            url = f'{search_url}&page={page}' if page > 1 else search_url
            response = session.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            products = soup.find_all('div', class_='product-card')
            if not products:
                print(f'Нет товаров на странице {page}')
                break

            with transaction.atomic():
                for product in products:
                    try:
                        name_elem = product.find('span', class_='goods-name')
                        name = name_elem.text.strip() if name_elem else 'Не указано'

                        price_elem = product.find('ins', class_='price__lower-price')
                        price = float(price_elem.text.replace('₽', '').replace(' ', '').strip()) if price_elem else 0.0

                        discount_price_elem = product.find('del')
                        discount_price = float(discount_price_elem.text.replace('₽', '').replace(' ', '').strip()) if discount_price_elem else None

                        rating_elem = product.find('span', class_='product-card__rating')
                        rating = float(rating_elem.text.strip()) if rating_elem else 0.0

                        reviews_elem = product.find('span', class_='product-card__count')
                        reviews_count = int(reviews_elem.text.strip()) if reviews_elem else 0

                        Product.objects.update_or_create(
                            name=name,
                            category=category,
                            defaults={
                                'price': price,
                                'discount_price': discount_price,
                                'rating': rating,
                                'reviews_count': reviews_count,
                            }
                        )
                    except Exception as e:
                        print(f'Ошибка при обработке товара: {e}')
                        continue

            print(f'Страница {page} обработана')
            headers['User-Agent'] = ua.random
            time.sleep(random.uniform(3, 7))

        except requests.exceptions.HTTPError as e:
            print(f'Ошибка HTTP при загрузке страницы {page}: {e}')
            break
        except Exception as e:
            print(f'Общая ошибка при загрузке страницы {page}: {e}')
            break

if __name__ == '__main__':
    category = input('Введите категорию для парсинга (например, смартфоны): ')
    parse_wildberries(category)