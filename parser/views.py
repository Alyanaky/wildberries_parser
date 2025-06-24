from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from django.db.models import Q

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        min_rating = self.request.query_params.get('min_rating')
        min_reviews = self.request.query_params.get('min_reviews')
        category = self.request.query_params.get('category')

        if min_price:
            queryset = queryset.filter(Q(price__gte=min_price) | Q(discount_price__gte=min_price))
        if max_price:
            queryset = queryset.filter(Q(price__lte=max_price) | Q(discount_price__lte=max_price))
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)
        if min_reviews:
            queryset = queryset.filter(reviews_count__gte=min_reviews)
        if category:
            queryset = queryset.filter(category__icontains=category)

        return queryset