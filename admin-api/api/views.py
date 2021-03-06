import requests
from datetime import datetime,timedelta
from rest_framework import generics
from rest_framework.response import Response
from .serializers import BookSerializer, BookLoanedSerializer, UserSerializer, UnAvailableBooksSerializer
from .models import Book, Member, BookLoaned
# Create your views here.

# function to fetch all loaned books from the client api and save them if they do not exist in the database


def get_loaned_books():
    loaned_books = requests.get(
        "http://clientservice:8080/api/get-loaned-books/").json()
    return loaned_books

# create book view


class CreateBook(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# delete book view


class DeleteBook(generics.RetrieveDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Fetch/List Users view


class GetUsers(generics.ListAPIView):
    queryset = Member.objects.all()
    serializer_class = UserSerializer

    # Overiding the list method to allow fetching of all users from client-api and saving them if they do not exist alredy
    def list(self, request):
        members = requests.get(
            "http://clientservice:8080/api/enrol-user/").json()
        serializer = UserSerializer(members, many=True)
        return Response(serializer.data)


# List Users and Books Borrowed
class UserBookBorrowed(generics.ListAPIView):
    queryset = BookLoaned.objects.all()
    serializer_class = BookLoanedSerializer

    # Overiding the list method to call get_loaned_books
    def list(self, request):
        serializer = BookLoanedSerializer(get_loaned_books(), many=True)
        return Response(serializer.data)

# List Books Borrowed and day it will be available


class UnavailableBooks(generics.ListAPIView):
    serializer_class = UnAvailableBooksSerializer
    queryset = BookLoaned.objects.all()

    # Overiding the list method to call get_loaned_books and setting the duration
    def list(self, request):
        books = get_loaned_books()
        modify_books = []
        for book in books:
            duration = datetime.fromisoformat(book['date_borrowed'])+timedelta(days=int(book['duration'].split(" ")[0]))
            book = book['book']
            modify_books.append({"book": book,
                                "Available On": duration.date()
                                 })
        return Response(modify_books)
