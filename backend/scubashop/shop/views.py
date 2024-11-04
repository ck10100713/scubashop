from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Product, Category, ProductImage, Brand
from .serializers import ProductSerializer, CategorySerializer, ProductImageSerializer, BrandSerializer
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['categories', 'brand', 'isActive']
    permission_classes = [permissions.IsAdminUser]  # 僅限管理員用戶進行寫入操作

    def get_permissions(self):
        if self.request.method in ['POST', 'PATCH', 'DELETE']:
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAdminUser]

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAdminUser]

class ShopView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        form = ProductFilterForm(request.GET or None)
        products = Product.objects.all()

        if form.is_valid():
            category = form.cleaned_data.get('category')
            brand = form.cleaned_data.get('brand')
            sort_by = form.cleaned_data.get('sort_by')
            search = request.GET.get('search', '')  # 取得搜尋關鍵字，若無則為空字串

            if category:
                products = products.filter(categories=category)
            if brand:
                products = products.filter(brand=brand)
            if search:
                products = products.filter(name__icontains=search)  # 根據商品名稱進行搜尋
            if sort_by:
                if sort_by == 'price_asc':
                    products = products.order_by('price')
                elif sort_by == 'price_desc':
                    products = products.order_by('-price')

        # 默認排序，這裡按 ID 排序
        products = products.order_by('id')

        # 分頁設置
        paginator = Paginator(products, 9)  # 每頁顯示9個商品
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        categories = Category.objects.all()
        brands = Brand.objects.all()

        return Response({
            'page_obj': ProductSerializer(page_obj, many=True).data,  # 傳遞分頁對象
            'categories': CategorySerializer(categories, many=True).data,
            'brands': BrandSerializer(brands, many=True).data,
        }, status=status.HTTP_200_OK)

class ProductDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)

class PictureView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        images = product.images.all()
        if images.count() == 0:
            return Response({'error': 'No image found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ProductImageSerializer(images, many=True).data, status=status.HTTP_200_OK)