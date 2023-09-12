from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    LoanBook,
    UserViewSet,
    BooksViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"books", BooksViewSet, basename="book")

app_name = "client_api"
urlpatterns = [
    path("books/<int:id>/borrow/", LoanBook.as_view(), name="book-loan"),
]

urlpatterns += router.urls
