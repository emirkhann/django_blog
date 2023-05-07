from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .utils import send_activation_code, create_activation_code

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')
    
    def validate(self, attrs: dict):
        print(attrs)
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('неверный пароль')
        return attrs

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('такая почта уже существует!')
        return email
    
    def create(self, validated_data: dict):
        user = User.objects.create_user(**validated_data)
        create_activation_code(user)
        send_activation_code(user)
        return user 

class ActivationSerializer(serializers.Serializer):
    activation_code = serializers.CharField(max_length=10)

    def validate_activation_code(self, activation_code):
        if User.objects.filter(activation_code=activation_code).exists():
            return activation_code
        raise serializers.ValidationError('неверно указан код')
    
    def activate(self):
        code = self.validated_data.get('activation_code')
        user = User.objects.get(activation_code=code)
        user.is_active = True
        user.activation_code = ''
        user.save()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate_username(self, username):
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError('неверно указан username')
        return username
    
    def validate(self, attrs):
        request = self.context.get('request')
        username = attrs.get('username')
        password = attrs.get('password')
        if username and password:
            user = authenticate(username=username, password=password, request=request)
            if not user:
                raise serializers.ValidationError('неправильно указан логин или пароль')
        else:
                raise serializers.ValidationError('логин и пароль обязательны к заполнению!')
        attrs['user'] = user
        return attrs
    


    