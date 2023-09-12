from typing import TypedDict

from rest_framework import serializers

from .models import Book, User, LoanedBook


class LoanedBookValidationData(TypedDict):
    """A TypeDict specifying data from the validation data in LoanedBookSerializer"""

    email: str
    duration: int
    book: Book


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class LoanedBookSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    book = serializers.StringRelatedField()

    class Meta:
        model = LoanedBook
        fields = "__all__"


class GetLoanedBooksSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="email")
    book = serializers.SlugRelatedField(read_only=True, slug_field="title")

    class Meta:
        model = LoanedBook
        fields = "__all__"
