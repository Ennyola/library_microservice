from rest_framework import serializers

from .models import Book, User, LoanedBook

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","email", "first_name", "last_name"]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class LoanedBookSerializer(serializers.Serializer):
    email = serializers.EmailField()
    duration = serializers.IntegerField()


class GetLoanedBooks(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="email")
    book = serializers.SlugRelatedField(read_only=True, slug_field="title")

    class Meta:
        model = LoanedBook
        fields = "__all__"
