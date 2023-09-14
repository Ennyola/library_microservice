from datetime import datetime, timedelta
from typing import Union

from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet

import requests
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import status

from .serializers import (
    BookSerializer,
    UserSerializer,
    LoanedBookSerializer,
    # UnAvailableBooksSerializer,
)
from .models import Book, User, LoanedBook

# Create your views here.


# function to fetch all loaned books from the client api and save them if they do not exist in the database
# def get_loaned_books():
#     loaned_books = requests.get(
#         "http://clientservice:8080/api/get-loaned-books/"
#     ).json()
#     return loaned_books


class BookViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "id"

    def destroy(self, request, *args, **kwargs) -> Response:
        if not Book.objects.filter(id=kwargs["id"]).exists():
            return Response(
                {"error": "This book does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        return super().destroy(request, *args, **kwargs)


class UsersViewset(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# List Users and Books Borrowed
class UserBookBorrowed(ListModelMixin, GenericViewSet):
    queryset = LoanedBook.objects.all()
    serializer_class = LoanedBookSerializer


# List Books Borrowed and day it will be available


class UnavailableBooks(ListModelMixin, GenericViewSet):
    serializer_class = LoanedBookSerializer

    def get_queryset(self) -> QuerySet[LoanedBook]:
        # Get the current date
        current_date = datetime.now().date()

        # Filter LoanedBook objects where return_date is greater than or equal to the current date
        queryset = LoanedBook.objects.filter(return_date__gte=current_date)
        return queryset

    def list(self, request, *args, **kwargs):
        # Get the queryset
        loaned_books = self.get_queryset()

        # Create a list to hold the modified data
        loaned_books_data = []

        # Modify the data as required
        for loaned_book in loaned_books:
            available_on = loaned_book.return_date.strftime("%d-%m-%Y")
            loaned_books_data.append(
                {"book": loaned_book.book.title, "available_on": available_on}
            )

        return Response(loaned_books_data)
