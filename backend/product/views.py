from rest_framework import generics, permissions, authentication
from .permissions import IsStaffPermission
from .models import Category, Product
from rest_framework.response import Response
from .serializers import CategorySerializer, ProductSerializer

class categoryList(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAdminUser,IsStaffPermission]

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'status': 'success',
            'message': 'Categories fetched successfully',
            'data': serializer.data,
        }
        return Response(data)

class categoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAdminUser,IsStaffPermission]
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {
            'status': 'success',
            'message': 'Category detail fetched successfully',
            'data': serializer.data,
        }
        return Response(data)        
       

class productList(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser,IsStaffPermission]
    
    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'status': 'success',
            'message': 'Products fetched successfully',
            'data': serializer.data,
        }
        return Response(data)

class productDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAdminUser,IsStaffPermission]
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {
            'status': 'success',
            'message': 'Product detail fetched successfully',
            'data': serializer.data,
        }
        return Response(data)   



    
        
    