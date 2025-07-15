from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from product.models import Product, Variant, ProductImage
from custom_admin.serializers import ProductSerializer, VariantSerializer, ProductImageSerializer


class ProductDetailAPI(generics.RetrieveUpdateAPIView):
    """API endpoint for getting and updating product info"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


class ProductVariantsListCreateAPI(generics.ListCreateAPIView):
    """API endpoint for listing and creating product variants"""
    serializer_class = VariantSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Variant.objects.filter(product_id=product_id)

    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.kwargs['product_id'])
        serializer.save(product=product)


class ProductVariantDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint for getting, updating, and deleting a specific variant"""
    serializer_class = VariantSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Variant.objects.filter(product_id=product_id)


class BulkUpdateVariantsAPI(generics.GenericAPIView):
    """API endpoint for bulk updating multiple variants"""
    serializer_class = VariantSerializer
    permission_classes = [IsAdminUser]

    def post(self, request, product_id):
        variants = request.data.get('variants', [])
        product = get_object_or_404(Product, pk=product_id)
        
        updated_variants = []
        for variant_data in variants:
            variant_id = variant_data.get('id')
            if variant_id:
                variant = get_object_or_404(Variant, pk=variant_id, product=product)
                serializer = self.get_serializer(variant, data=variant_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    updated_variants.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(updated_variants, status=status.HTTP_200_OK)


class ProductImagesListCreateAPI(generics.ListCreateAPIView):
    """API endpoint for listing and creating product images"""
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductImage.objects.filter(product_id=product_id)

    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.kwargs['product_id'])
        serializer.save(product=product)


class ProductImageDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint for getting, updating, and deleting a specific image"""
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductImage.objects.filter(product_id=product_id)


class BulkUpdateImagesAPI(generics.GenericAPIView):
    """API endpoint for bulk updating multiple images"""
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminUser]

    def post(self, request, product_id):
        images = request.data.get('images', [])
        product = get_object_or_404(Product, pk=product_id)
        
        updated_images = []
        for image_data in images:
            image_id = image_data.get('id')
            if image_id:
                image = get_object_or_404(ProductImage, pk=image_id, product=product)
                serializer = self.get_serializer(image, data=image_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    updated_images.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(updated_images, status=status.HTTP_200_OK)