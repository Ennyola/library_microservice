from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    GetBooks,
    GetSingleBook,
    LoanBook,
    GetLoanedBooks,
    UserViewSet,
    BooksViewSet,
)


router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"books", BooksViewSet, basename="book")

app_name = "client_api"
urlpatterns = [
    # path(
    #     "books/",
    #     include(
    #         [
    #             path("", GetBooks.as_view(), name="books"),
    #             path("<int:id>/", GetSingleBook.as_view(), name="single-book"),
    #             path("<int:id>/borrow/", LoanBook.as_view()),
    #         ]
    #     ),
    # ),
    # path(
    #     "users/",
    #     include(
    #         [
    #             path("", Users.as_view(), name="enrol-user"),
    #             path("<int:id>/", UserDetail.as_view(), name="user-detail"),
    #         ]
    #     ),
    # ),
    path("get-loaned-books/", GetLoanedBooks.as_view()),
]

urlpatterns += router.urls
