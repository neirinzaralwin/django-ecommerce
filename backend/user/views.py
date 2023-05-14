from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework import status
from .serializers import UserSerializer
from .models import User

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status" : "success", "message": "Registered successfully", "user" :serializer.data})

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({"status": "error", "message": f"User with email: {email} not found"}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({"status": "error", "message": "Password is incorrect"}, status=status.HTTP_401_UNAUTHORIZED)

        data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
        }
        return Response({"status" : "success", "message": "Logined successfully", "user" :data})    

class DeleteView(APIView):
    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"status": "success", "message": "User deleted successfully."})
        except User.DoesNotExist:
            return Response({"status": "error", "message": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-id')
    
    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'status': 'success',
            'message': 'Categories fetched successfully',
            'data': serializer.data,
        }
        return Response(data)
