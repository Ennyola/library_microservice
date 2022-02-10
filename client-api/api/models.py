import requests
from django.db import models
# Create your models here.


class Member(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class ExcludeBorrowedBookManager(models.Manager):
    def get_queryset(self):
        books = requests.get("http://adminservice:8000/api/books/").json()
        for book in books:
            if super().get_queryset().filter(id=book['id']).exists():
                pass
            else:
                super().get_queryset().create(**book)
        return super().get_queryset().exclude(borrowed=True)


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    year_published = models.IntegerField(blank=True, null=True)
    borrowed = models.BooleanField(default=False)
    objects = models.Manager()
    get_books = ExcludeBorrowedBookManager()

    class Meta:
        ordering=["-id"]
        
    def __str__(self):
        return self.title


class BookLoaned(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    duration = models.DurationField()

    def __str__(self):
        return f"{self.book.title}-{self.user.email}"
