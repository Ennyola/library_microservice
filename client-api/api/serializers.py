from rest_framework import serializers
from .models import Book, Member,BookLoaned


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['email', 'first_name', 'last_name']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookLoanedSerializer(serializers.Serializer):
    email = serializers.EmailField()
    duration = serializers.IntegerField()
    
class GetLoanedBooks(serializers.ModelSerializer):
    class Meta:
        model = BookLoaned
        fields = '__all__'