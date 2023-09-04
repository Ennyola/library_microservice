from datetime import datetime, timedelta
from typing import Union

from django.shortcuts import get_object_or_404

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
    # BookLoanedSerializer,
    UserSerializer,
    # UnAvailableBooksSerializer,
)
from .models import Book, User

# Create your views here.

# function to fetch all loaned books from the client api and save them if they do not exist in the database
def get_loaned_books():
    loaned_books = requests.get(
        "http://clientservice:8080/api/get-loaned-books/"
    ).json()
    return loaned_books

class BookView(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "id"

    def destroy(self, request, *args, **kwargs) -> Response:
        if not Book.objects.filter(id=kwargs["id"]).exists():
            return Response(
                {"error": "This book does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        return super().destroy(request, *args, **kwargs)


class UsersViewset(ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# List Users and Books Borrowed
# class UserBookBorrowed(generics.ListAPIView):
#     queryset = BookLoaned.objects.all()
#     serializer_class = BookLoanedSerializer

#     # Overiding the list method to call get_loaned_books
#     def list(self, request):
#         serializer = BookLoanedSerializer(get_loaned_books(), many=True)
#         return Response(serializer.data)


# List Books Borrowed and day it will be available


# class UnavailableBooks(generics.ListAPIView):
#     serializer_class = UnAvailableBooksSerializer
#     queryset = BookLoaned.objects.all()

#     # Overiding the list method to call get_loaned_books and setting the duration
#     def list(self, request):
#         books = get_loaned_books()
#         modify_books = []
#         for book in books:
#             duration = datetime.fromisoformat(book["date_borrowed"]) + timedelta(
#                 days=int(book["duration"].split(" ")[0])
#             )
#             book = book["book"]
#             modify_books.append({"book": book, "Available On": duration.date()})
#         return Response(modify_books)
