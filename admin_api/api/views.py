from datetime import datetime, timedelta
from typing import Union, Any

from django.db.models.query import QuerySet

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import status

from .serializers import BookSerializer, UserSerializer, LoanedBookSerializer
from .models import Book, User, LoanedBook


class BookViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    """
    A ViewSet for managing books.

    Allows creating and deleting books.

    Attributes:
        queryset (QuerySet): The queryset of books.
        serializer_class: The serializer class for books.
        lookup_field (str): The field to use for looking up books.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "id"

    def destroy(
        self, request: Request, *args: tuple, **kwargs: dict[str, Any]
    ) -> Response:
        """
        Delete a book.

        Args:
            request (Request): The HTTP request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments, including the book's id.

        Returns:
            Response: An HTTP response indicating success or failure.
        """
        if not Book.objects.filter(id=kwargs["id"]).exists():
            return Response(
                {"error": "This book does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        return super().destroy(request, *args, **kwargs)


class UsersViewset(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for viewing user information.

    Allows viewing user data.

    Attributes:
        queryset (QuerySet): The queryset of users.
        serializer_class: The serializer class for users.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserBookBorrowed(ListModelMixin, GenericViewSet):
    """
    A ViewSet for viewing books borrowed by users.

    Allows viewing books borrowed by users.

    Attributes:
        queryset (QuerySet): The queryset of loaned books.
        serializer_class: The serializer class for loaned books.
    """

    queryset = LoanedBook.objects.all()
    serializer_class = LoanedBookSerializer


class UnavailableBooks(ListModelMixin, GenericViewSet):
    """
    A ViewSet for viewing books that are currently unavailable (loaned out).

    Allows viewing books and their return dates.

    Attributes:
        serializer_class: The serializer class for loaned books.
    """

    serializer_class = LoanedBookSerializer

    def get_queryset(self) -> QuerySet[LoanedBook]:
        """
        Get a queryset of loaned books that are currently unavailable.

        Returns:
            QuerySet: A queryset of LoanedBook objects.
        """
        current_date = datetime.now().date()
        queryset = LoanedBook.objects.filter(return_date__gte=current_date)
        return queryset

    def list(
        self, request: Request, *args: tuple, **kwargs: dict[str, Any]
    ) -> Response:
        """
        List books that are currently unavailable along with their return dates.

        Args:
            request (Request): The HTTP request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: An HTTP response with a list of books that are currently unavailable,
            including book titles and return dates.
        """
        loaned_books = self.get_queryset()
        loaned_books_data = []

        for loaned_book in loaned_books:
            available_on = loaned_book.return_date.strftime("%d-%m-%Y")
            loaned_books_data.append(
                {"book": loaned_book.book.title, "available_on": available_on}
            )

        return Response(loaned_books_data)
