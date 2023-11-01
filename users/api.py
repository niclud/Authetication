from .models import Users
from rest_framework import viewsets, permissions, generics, authentication, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from django.contrib.auth.hashers import make_password

from .serializers import UserSerializer, AuthTokenSerializer

class CreateUserView(generics.CreateAPIView):
    # queryset = Users.objects.all()
    serializer_class = UserSerializer

    # permission_classes = [permissions.IsAdminUser]


class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    

# token que se utiliza para autenticarse en el sistema
class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    # renderer_classes = ('rest_framework.renderers.JSONRenderer',)

class LogoutView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Obten el token de acceso del usuario autenticado
        token = request.auth
        if token:
            # Invalida el token (elimina la relación entre el token y el usuario)
            token.delete()
            return Response({'detail': 'Sesión cerrada exitosamente.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No se encontró un token de acceso.'}, status=status.HTTP_400_BAD_REQUEST)
