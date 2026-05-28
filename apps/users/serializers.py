from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerialezer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, label='Підтвердження паролю')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Паролі не співпадають!')
        return data
    
    def create(self, validate_data):
        validate_data.pop('password2')
        user = User.objects.create_user(**validate_data)
        return user
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'avatar', 'timezone', 'date_joined')
        read_only_fields = ('date_joined',)