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
        queryset: QuerySet[Book] = Book.objects.exclude(borrowed=True)
        publisher: str = self.request.query_params.get("publisher", None)
        category: str = self.request.query_params.get("category", None)
        if publisher is not None:
            queryset = queryset.filter(publisher__iexact=publisher)
        if category is not None:
            queryset = queryset.filter(category__iexact=category)
        return queryset


class LoanBook(generics.CreateAPIView):
    """_summary_"""

    serializer_class = LoanedBookSerializer

    def get_queryset(self) -> QuerySet[Book]:
        queryset: QuerySet[Book] = Book.objects.exclude(borrowed=True)
        return queryset

    def post(self, request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        book = get_object_or_404(queryset, id=kwargs["id"])
        serializer = LoanedBookSerializer(data=request.data)
        if serializer.is_valid():
            loaned_book: LoanedBook = serializer.save(book=book)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    # def post(self, request, id):
    #     serializer = LoanedBookSerializer(data=request.data)
    #     if serializer.is_valid():
    #         email, duration = serializer.data["email"], serializer.data["duration"]
    #         user = User.objects.get(email=email)
    #         book = Book.objects.get(id=id)
    #         LoanedBook.objects.create(
    #             book=book, user=user, duration=datetime.timedelta(days=duration)
    #         )
    #         book.borrowed = True
    #         book.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors)


class GetLoanedBooks(generics.ListAPIView):
    serializer_class = GetLoanedBooks
    queryset = LoanedBook.objects.all()
