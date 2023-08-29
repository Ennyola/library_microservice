from django.db import models
from django.db.models.query import QuerySet

import requests


class User(models.Model):
    """Model representing users enrolled in the library."""

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        """Return a string representation of the user."""
        return f"{self.first_name} {self.last_name}"


class ExcludeBorrowedBookManager(models.Manager):
    """A custom model manager to exclude borrowed books from the queryset."""

    def get_queryset(self) -> QuerySet:
        """Get a queryset excluding borrowed books from the library."""
        # Fetch book data from the admin service
        books = requests.get("http://adminservice:8000/api/books/").json()

        # Update the local database with fetched book data
        for book in books:
            if not super().get_queryset().filter(id=book["id"]).exists():
                super().get_queryset().create(**book)

        # Return a queryset excluding borrowed books
        return super().get_queryset().exclude(borrowed=True)


class Book(models.Model):
    """Model representing books available in the library."""

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    borrowed = models.BooleanField(default=False)
    objects = models.Manager()
    get_books = ExcludeBorrowedBookManager()

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        """Return a string representation of the book."""
        return self.title


class LoanedBook(models.Model):
    """Model representing books that have been loaned."""

    date_borrowed = models.DateField(auto_now_add=True)
    return_date = models.DateField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return a string representation of the loaned book."""
        return f"{self.book.title} - {self.user.email}"
