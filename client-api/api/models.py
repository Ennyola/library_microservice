import requests

from django.db import models
from django.utils import timezone

# Create your models here.


class User(models.Model):
    """Users enrolled to the library"""

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ExcludeBorrowedBookManager(models.Manager):
    """A model manager to exclude borrowed books from the queryset"""

    def get_queryset(self):
        books = requests.get("http://adminservice:8000/api/books/").json()
        for book in books:
            if super().get_queryset().filter(id=book["id"]).exists():
                pass
            else:
                super().get_queryset().create(**book)
        return super().get_queryset().exclude(borrowed=True)


class Book(models.Model):
    """Book model for gthr library"""

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    borrowed = models.BooleanField(default=False)
    objects = models.Manager()
    get_books = ExcludeBorrowedBookManager()

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class LoanedBook(models.Model):
    date_borrowed = models.DateField(auto_now_add=True)
    return_date = models.DateField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book.title}-{self.user.email}"
