from typing import Optional, Any

from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from django.http import Http404

from rest_framework import generics, status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.request import Request

from .serializers import (
    BookSerializer,
    LoanedBookSerializer,
    UserSerializer,
)
from .models import Book, User, LoanedBook


# Create your views here.
class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """API endpoint for enrolling users to the library."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class BooksViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for managing books in the library."""

    serializer_class = BookSerializer

    def get_queryset(self) -> QuerySet[Book]:
        """Return a queryset of books excluding those that are borrowed."""
        queryset: QuerySet[Book] = Book.objects.exclude(borrowed=True)
        publisher: Optional[str] = self.request.query_params.get("publisher", None)
        category: Optional[str] = self.request.query_params.get("category", None)

        if publisher is not None:
            queryset = queryset.filter(publisher__iexact=publisher)
        if category is not None:
            queryset = queryset.filter(category__iexact=category)
        return queryset


class LoanBook(generics.GenericAPIView):
    """
    API endpoint for borrowing a book from the library.

    Only available books can be borrowed. If the book is already borrowed,
    a 400 Bad Request response will be returned.
    """

    serializer_class = LoanedBookSerializer

    def get_queryset(self) -> QuerySet[Book]:
        """Return a queryset of available books."""

        queryset: QuerySet[Book] = Book.objects.exclude(borrowed=True)
        return queryset

    def post(self, request: Request, **kwargs: dict[str, Any]) -> Response:
        """
        Borrow a book from the library.

        Args:
            request: The HTTP request containing user data.
            kwargs: Additional keyword arguments containing book ID.

        Returns:
            Response: A response with details of the borrowed book.

        """

        queryset: QuerySet[Book] = self.get_queryset()

        # Return a 404 error if the user tries to borrow an unavailable book.
        try:
            book: Book = get_object_or_404(queryset, id=kwargs["id"])
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if book.borrowed:
            return Response(
                {"detail": "This book is already borrowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = LoanedBookSerializer(data=request.data)
        if serializer.is_valid():
            book.borrowed = True
            book.save()

            # Get a loanedbook object to be passed as a response
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
