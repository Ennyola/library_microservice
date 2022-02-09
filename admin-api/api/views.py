import requests
from rest_framework import generics
from .serializers import BookSerializer, BookLoanedSerializer, UserSerializer, UnAvailableBooksSerializer
from .models import Book, Member, BookLoaned
# Create your views here.


class CreateBook(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class DeleteBook(generics.RetrieveDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class GetUsers(generics.ListAPIView):
    queryset = Member.get_members.all()
    serializer_class = UserSerializer


class UserBookBorrowed(generics.ListAPIView):
    queryset = BookLoaned.objects.all()
    serializer_class = BookLoanedSerializer


class UnavailableBooks(generics.ListAPIView):
    serializer_class = UnAvailableBooksSerializer
    queryset = BookLoaned.get_loaned_books.all()


# print(requests.get("http://host.docker.internal:8080/api/enrol-user/").json())
