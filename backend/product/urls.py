from django.urls import path
from .views import categoryList, categoryDetail, productList, productDetail

urlpatterns = [
    path('categories/', categoryList.as_view()),
    path('categories/<int:pk>/', categoryDetail.as_view()),
    path('products/', productList.as_view()),
    path('products/<int:pk>/', productDetail.as_view()),
]