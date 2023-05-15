from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'name' ,'email', 'password']
        extra_kwargs = {'password': {'write_only': True}} # we won't show password to the client

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save() 
        return instance

    def update(self, instance, validated_data):
        # Update the user fields with the validated data
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)

        # If a password is provided, update the password
        password = validated_data.get('password', None)
        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance  

    
