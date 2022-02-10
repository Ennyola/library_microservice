from django.db import models
from django.utils import timezone
# Create your models here.


class Member(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

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
    borrowed = models.BooleanField(default=False)

    class Meta:
        ordering=["-id"]
        
    def __str__(self):
        return self.title


class BookLoaned(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    duration = models.DurationField()
    date_borrowed =  models.DateField(default=timezone.now)
    class Meta:
        ordering=["-id"]

    def __str__(self):
        return f"{self.book.title}-{self.user.email}"
