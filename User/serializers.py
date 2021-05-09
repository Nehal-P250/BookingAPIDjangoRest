from rest_framework import serializers

from .models import Advisor,MyUser,Booking

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
        extra_kwargs = {'password': {'write_only': True}}
    
    # without this the password will not be hashed , and it will be 
    # directly stored in the database.
    def create(self, validated_data):
        """Create and return a new user."""

        # Method 1.
        # # overriding on create to hash the password 
        # password = validated_data.pop('password', None)
        # instance = self.Meta.model(**validated_data)
        # if password is not None:
        #     instance.set_password(password)
        # instance.save()
        # return instance

        # Method 2
        user = MyUser(
            email = validated_data['email'],
            name = validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class BookingSerializer(serializers.ModelSerializer):
    # https://medium.com/@gurupratap.matharu/build-a-restapi-using-nested-serializers-in-django-rest-framework-c0f6a31fd865
    advisor = AdvisorSerializer()
    class Meta:
        model = Booking
        fields =['id','time','advisor']