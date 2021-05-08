from rest_framework import serializers

from .models import Advisor,MyUser

class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields =[
            'id',
            'name',
            'photo_url',
        ]

class MyUserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = MyUser
        fields = ['id','name', 'email', 'password']
    
    # def create(self, validated_data):
    #     # overriding on create to hash the password 
    #     password = validated_data('password', None)
    #     instance = self.Meta.model(**validated_data)
    #     if password is not None:
    #         instance.set_password(password)
    #     instance.save()
    #     return instance