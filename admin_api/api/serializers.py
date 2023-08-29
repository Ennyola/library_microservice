from rest_framework import serializers

from .models import Book


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)



class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookLoanedSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=200)
    book = serializers.CharField(max_length=200)



class UnAvailableBooksSerializer(serializers.Serializer):
    book = serializers.CharField(max_length=200)
    duration = serializers.CharField(max_length=300)

