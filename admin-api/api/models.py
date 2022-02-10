import requests
import datetime
from django.db import models
# Create your models here.


class GetMembersManager(models.Manager):
    def get_queryset(self):
        members = requests.get(
            "http://clientservice:8080/api/enrol-user/").json()
        for member in members:
            if super().get_queryset().filter(email=member['email']).exists():
                pass
            else:
                super().get_queryset().create(**member)
        return super().get_queryset()


class Member(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    objects = models.Manager()
    get_members = GetMembersManager()

    class Meta:
        ordering=["-id"]
        
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    year_published = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering=["-id"]
        
    def __str__(self):
        return self.title


class GetLoanedBooksManager(models.Manager):
    def get_queryset(self):
        # loaned_books = requests.get(
        #     "http://clientservice:8080/api/get-loaned-books/").json()
        # for loaned_book in loaned_books:
        #     if super().get_queryset().filter(id=loaned_book['id']).exists():
        #         pass
        #     else:
        #         book = Book.objects.filter(id=loaned_book['book']).first()
        #         user = Member.objects.filter(id=loaned_book['user']).first()
        #         duration = datetime.timedelta(
        #             days=int(loaned_book['duration'].split(" ")[0]))
        #         super().get_queryset().create(book=book, user=user,duration=duration)
        return super().get_queryset()


class BookLoaned(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    duration = models.DurationField()
    objects = models.Manager()
    get_loaned_books = GetLoanedBooksManager()
    class Meta:
        ordering=["-id"]

    def __str__(self):
        return f"{self.book.title}-{self.user.email}"
