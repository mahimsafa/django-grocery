from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .models import Product
from .serializers import ProductSerializer

class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        query = self.request.query_params.get('q')
        if query:
            search_vector = SearchVector('name', 'description')  # add more fields as needed
            search_query = SearchQuery(query)

            return Product.objects.annotate(
                rank=SearchRank(search_vector, search_query)
            ).filter(
                rank__gte=0.1  # adjust threshold if needed
            ).order_by('-rank')
        return Product.objects.all()

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    pagination_class = ProductPagination
