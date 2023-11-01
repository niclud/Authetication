from rest_framework import serializers
from .models import Users
from django.contrib.auth import get_user_model, authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'first_name', 'last_name', 'date_of_birth', 'is_active', 'is_staff', 'date_joined', 'groups', 'user_permissions')
        read_only_fields = ('date_joined',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Extrae y hashea la contraseña antes de crear el usuario
        password = validated_data.pop('password')
        user = get_user_model().objects.create_user(**validated_data, password=password)
        return user
        # return get_user_model().objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
    

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        )
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request=self.context.get('request'), username=email, password=password)

        if not user:
            raise serializers.ValidationError('No se pudo autenticar con las credenciales proporcionadas', code='authentication')
        
        data['user'] = user

        return data