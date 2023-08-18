from datetime import date, timedelta

from rest_framework import serializers

from .models import Book, User, LoanedBook


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
        today: date = date.today()
        return_date: date = today + timedelta(days=validated_data["duration"])
        user: User = User.objects.get(email=validated_data["email"])
        loaned_book = LoanedBook.objects.create(
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
