import datetime
from typing import Union

from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from django.http import Http404

from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response


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


class LoanBook(APIView):
    """_summary_"""

    serializer_class = LoanedBookSerializer

    def get_queryset(self) -> QuerySet[Book]:
        queryset: QuerySet[Book] = Book.objects.exclude(borrowed=True)
        return queryset

    # set a validation for the email input
    #

    def post(self, request, **kwargs) -> Response:
        queryset: QuerySet[Book] = self.get_queryset()
        book: Union[Book, Http404] = get_object_or_404(queryset, id=kwargs["id"])
        serializer = LoanedBookSerializer(data=request.data)
        if serializer.is_valid():
            book.borrowed = True
            book.save()
            loaned_book: LoanedBook = serializer.save(book=book)
            return Response(
                {
                    "book_id": loaned_book.book.id,
                    "book_title": loaned_book.book.title,
                    "user_email": loaned_book.user.email,
                    "date_borrowed": loaned_book.date_borrowed,
                    "return_date": loaned_book.return_date,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetLoanedBooks(generics.ListAPIView):
    serializer_class = GetLoanedBooks
    queryset = LoanedBook.objects.all()
