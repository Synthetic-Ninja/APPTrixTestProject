from rest_framework import serializers

from .models import Client


class ClientRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'sex',
                  'username', 'password', 'email', 'avatar',
                  'position_latitude', 'position_longitude')

    def create(self, validated_data):
        client = self.Meta.model.objects.create_user(**validated_data)
        return client
