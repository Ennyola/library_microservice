from datetime import datetime
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin
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
    queryset = BookLoaned.get_loaned_books.all()
    serializer_class = BookLoanedSerializer


class UnavailableBooks(generics.ListAPIView):
    serializer_class = UnAvailableBooksSerializer
    queryset = BookLoaned.get_loaned_books.all()

    def list(self, request):
        queryset = self.get_queryset()
        new_queryset = []
        for data in queryset:
            book = data.book.title
            duration = datetime.now()+data.duration
            new_queryset.append({"book":book,
                                 "Available On":duration.date()
                                 })
        return Response(new_queryset)

# print(requests.get("http://host.docker.internal:8080/api/enrol-user/").json())
