import datetime

from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet

from .serializers import (
    BookSerializer,
    LoanedBookSerializer,
    UserSerializer,
    GetLoanedBooks,
)
from .models import Book, User, LoanedBook


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """_summary_

    Args:
        viewsets (_type_): _description_
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class BooksViewSet(viewsets.ModelViewSet):
    """_summary_"""

    serializer_class = BookSerializer

    def get_queryset(self) -> QuerySet[Book]:
        queryset = Book.objects.exclude(borrowed=True)
        publishers: str = self.request.query_params.get("publishers", None)
        if publishers is not None:
            pass
        return queryset


class GetBooks(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.get_books.all()
        publisher = self.request.query_params.get("publisher")
        category = self.request.query_params.get("category")
        if publisher is not None:
            queryset = queryset.filter(publisher__icontains=publisher)
        if category is not None:
            queryset = queryset.filter(category__icontains=category)
        return queryset


class GetSingleBook(generics.RetrieveAPIView):
    serializer_class = BookSerializer
    queryset = Book.get_books.all()
    lookup_field = "id"


class LoanBook(APIView):
    def post(self, request, id):
        serializer = LoanedBookSerializer(data=request.data)
        if serializer.is_valid():
            email, duration = serializer.data["email"], serializer.data["duration"]
            user = User.objects.get(email=email)
            book = Book.objects.get(id=id)
            LoanedBook.objects.create(
                book=book, user=user, duration=datetime.timedelta(days=duration)
            )
            book.borrowed = True
            book.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class GetLoanedBooks(generics.ListAPIView):
    serializer_class = GetLoanedBooks
    queryset = LoanedBook.objects.all()
