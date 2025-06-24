from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена со скидкой')
    rating = models.FloatField(verbose_name='Рейтинг')
    reviews_count = models.IntegerField(verbose_name='Количество отзывов')
    category = models.CharField(max_length=100, verbose_name='Категория')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name