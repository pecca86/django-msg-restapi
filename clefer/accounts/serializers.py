from rest_framework import serializers
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=50, allow_blank=False, required=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(max_length=100, allow_blank=False, required=True, validators=[validate_password], write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        user.set_password(validated_data['password'])
        user.save()

        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }

    def delete(self, instance):
        instance.delete()

    class Meta:
        model = User
        fields = ['id','username', 'email', 'password']
