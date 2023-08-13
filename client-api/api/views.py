import datetime

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from django.shortcuts import get_object_or_404

from .serializers import (
    BookSerializer,
    LoanedBookSerializer,
    UserSerializer,
    GetLoanedBooks,
)
from .models import Book, User, LoanedBook


# Create your views here.
class EnrolUsers(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class Users(APIView):
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserDetail(APIView):
    
    def get_object(self, id):
        return get_object_or_404(User, id=id)
    
    def get(self, request, id):
        user = self.get_object(id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request,id):
        user = self.get_object(id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    def delete(self, request):
        user = self.get_object(id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GetBooks(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.get_books.all()
        publisher = self.request.query_params.get("publisher")
        category = self.request.query_params.get("category")
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
        serializer = LoanedBookSerializer(data=request.data)
        if serializer.is_valid():
            email, duration = serializer.data["email"], serializer.data["duration"]
            user = User.objects.get(email=email)
            book = Book.objects.get(id=id)
            LoanedBook.objects.create(
                book=book, user=user, duration=datetime.timedelta(days=duration)
            )
            book.borrowed = True
            book.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class GetLoanedBooks(generics.ListAPIView):
    serializer_class = GetLoanedBooks
    queryset = LoanedBook.objects.all()
