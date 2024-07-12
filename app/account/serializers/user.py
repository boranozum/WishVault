from rest_framework import serializers

from account.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'email',
            'is_superuser',
            'is_active',
            'date_joined',
            'last_login',
            'password',
            'confirm_password',
        ]
        read_only_fields = [
            'is_active',
            'is_superuser',
            'date_joined',
            'last_login',
        ]

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError('Passwords do not match')
        attrs.pop('confirm_password')
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class BriefUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'is_superuser',
        ]


