from rest_framework import serializers
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.core.validators import EmailValidator
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=50, allow_blank=False, required=True, validators=[EmailValidator(message='Username must be a valid email address'), UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(max_length=100, allow_blank=False, required=True, validators=[validate_password], write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )

        user.set_password(validated_data['password'])
        user.save()

        return {
            'id': user.id,
            'username': user.username,
        }

    class Meta:
        model = User
        fields = ['id','username', 'password']
