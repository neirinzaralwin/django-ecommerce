from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework import status
from .serializers import UserSerializer
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        return Response({"status" : "success", "message": "Registered successfully", "token" : token ,"user" :serializer.data})

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

        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {"status" : "success", "message": "Logined successfully", "token" : token,"user" :data}

        return response    

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
    queryset = User.objects.all().filter(is_staff=False, is_superuser=False)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-id')
    
    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'status': 'success',
            'message': 'All users fetched successfully',
            'data': serializer.data,
        }
        return Response(data)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            raise NotFound('User not found.')
        

    def get(self, request, user_id):
        try:
            user = self.get_object()
            serializer = self.serializer_class(user)
            data = {
                'status': 'success',
                'message': 'User fetched successfully',
                'data': serializer.data,
            }
            return Response(data)
        except NotFound as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            if request.user.id != user.id:
                return Response({"status": "error", "message": "You don't have permission to update this user."}, status=status.HTTP_403_FORBIDDEN)
            serializer = self.serializer_class(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                data = {
                    'status': 'success',
                    'message': 'User updated successfully',
                    'data': serializer.data,
                }
                return Response(data)
            return Response({
                    'status': 'error','message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_404_NOT_FOUND)            
             
    def delete(self, request, user_id):
        try:
            user = self.get_object()
            user.delete()
            data = {
                'status': 'success',
                'message': 'User deleted successfully',
            }
            return Response(data)
        except NotFound as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_404_NOT_FOUND)

  
