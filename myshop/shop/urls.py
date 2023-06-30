from django.urls import path
from . import views

from .views import (
    ProductListAPIView,
    ProductDetailAPIView,
    RecommendedProductsAPIView,
    CategoryListAPIView,
    RecommendProductsAPIView,
)

app_name = 'shop'

urlpatterns = [
    
    path('', views.product_list, name='product_list'),
    path('product', ProductListAPIView.as_view()),

    path('products/', RecommendProductsAPIView.as_view(), name='recommend'),

    path('products/<int:id>/<slug:slug>/', ProductDetailAPIView.as_view(), name='api_product_detail'),


    path('RecommendedProductsAPIView', RecommendedProductsAPIView.as_view()),

    path('CategoryListAPIView', CategoryListAPIView.as_view()),
    path('<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
         name='product_detail'),
     
    #path('ProductRecommendationAPIView/', ProductRecommendationAPIView.as_view(), name='ProductRecommendation'),
    

]
