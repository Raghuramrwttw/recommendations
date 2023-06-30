from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category, Product
from .recommender import Recommender
from rest_framework import generics
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.response import Response





from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Product
from .recommender import Recommender
from .serializers import CategorySerializer, ProductSerializer

class ProductListAPIView(APIView):
    def get(self, request, format=None):
        products = Product.objects.filter(available=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetailAPIView(APIView):
    def get(self, request, id, slug, format=None):
        language = request.LANGUAGE_CODE
        product = Product.objects.get(
            id=id,
            translations__language_code=language,
            translations__slug=slug,
            available=True
        )
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class RecommendedProductsAPIView(APIView):
    def post(self, request, format=None):
        product_ids = request.data.get('product_ids', [])
        products = Product.objects.filter(id__in=product_ids)
        r = Recommender()
        recommended_products = r.suggest_products_for(products, 4)
        serializer = ProductSerializer(recommended_products, many=True)
        return Response(serializer.data)

class CategoryListAPIView(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


from django.views.generic import TemplateView
from rest_framework.renderers import TemplateHTMLRenderer


class RecommendProductsAPIView(TemplateView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'C:/Users/Admin/Desktop/recommedations/myshop/shop/templates/shop/recommendation.html'

    def post(self, request, *args, **kwargs):
        product_id = request.POST('product_id')
        r = Recommender()
        products = Product.objects.filter(id=product_id)
        r.products_bought(products)  # Calculate product co-occurrence
        recommended_products = r.suggest_products_for(products, 4)
        context = {
            'products': Product.objects.all(),
            'recommended_products': recommended_products,
        }
        return self.render_to_response(context)
























def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category,
                                     translations__language_code=language,
                                     translations__slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})



def product_detail(request, id, slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product,
                                id=id,
                                translations__language_code=language,
                                translations__slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'recommended_products': recommended_products})







