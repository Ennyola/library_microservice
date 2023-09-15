from rest_framework import serializers

from .models import Book, User, LoanedBook


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]


class BookSerializer(serializers.ModelSerializer):
    """Serializer for the Book model."""

    class Meta:
        model = Book
        fields = "__all__"


class LoanedBookSerializer(serializers.ModelSerializer):
    """Serializer for the LoanedBook model."""

    user = serializers.StringRelatedField()
    book = serializers.StringRelatedField()

    class Meta:
        model = LoanedBook
        fields = "__all__"
