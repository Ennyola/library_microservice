import datetime
import requests
from rest_framework import generics, status
from rest_framework.views import APIView
from .serializers import BookSerializer, BookLoanedSerializer, UserSerializer,GetLoanedBooks
from .models import Book, Member, BookLoaned
from rest_framework.response import Response
# Create your views here.


class EnrolUsers(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = Member.objects.all()


class GetBooks(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.get_books.all()
        publisher = self.request.query_params.get('publisher')
        category = self.request.query_params.get('category')
        if publisher is not None:
            queryset = queryset.filter(publisher__icontains=publisher)
        if category is not None:
            queryset = queryset.filter(category__icontains=category)
        return queryset


class GetSingleBook(generics.RetrieveAPIView):
    serializer_class = BookSerializer
    queryset = Book.get_books.all()
    lookup_field = "id"


class LoanBook(APIView):
    def post(self, request, id):
        serializer = BookLoanedSerializer(data=request.data)
        if serializer.is_valid():
            email, duration = serializer.data['email'], serializer.data['duration']
            user = Member.objects.get(email=email)
            book = Book.objects.get(id=id)
            BookLoaned.objects.create(
                book=book, user=user, duration=datetime.timedelta(days=duration))
            book.borrowed = True
            book.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class GetLoanedBooks(generics.ListAPIView):
    serializer_class = GetLoanedBooks
    queryset = BookLoaned.objects.all()