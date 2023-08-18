from datetime import date, timedelta
from typing import TypedDict

from rest_framework import serializers

from .models import Book, User, LoanedBook


class LoanedBookValidationData(TypedDict):
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


class LoanedBookSerializer(serializers.Serializer):
    email = serializers.EmailField()
    duration = serializers.IntegerField()

    def create(self, validated_data) -> LoanedBook:
        """_summary_

        Args:
            validated_data (_type_): _description_

        Returns:
            LoanedBook: _description_
        """

        print(validated_data)
        print(type(validated_data))
        today: date = date.today()

        # Adds the current date with the duration(in days) set by the user
        return_date: date = today + timedelta(days=validated_data["duration"])
        user: User = User.objects.get(email=validated_data["email"])
        loaned_book: LoanedBook = LoanedBook.objects.create(
            date_borrowed=today,
            return_date=return_date,
            user=user,
            book=validated_data["book"],
        )
        return loaned_book


class GetLoanedBooks(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="email")
    book = serializers.SlugRelatedField(read_only=True, slug_field="title")

    class Meta:
        model = LoanedBook
        fields = "__all__"
