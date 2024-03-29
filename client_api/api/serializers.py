from datetime import date, timedelta

from rest_framework import serializers

from .models import Book, User, LoanedBook
from .typed_dicts import LoanedBookValidationData



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

    def create(self, validated_data: LoanedBookValidationData) -> LoanedBook:
        """_summary_

        Args:
            validated_data (LoanedBookValidationData): The validated data from a valid serializer

        Returns:
            LoanedBook: A Loanbook object
        """
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

    def validate_email(self, value: str) -> str:
        """Check that user is already a member(email exists in db)

        Args:
            value (str): the email of a particular user
        """

        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email not registered in the Db. User does not exist"
            )
        return value
