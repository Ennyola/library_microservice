from django.urls import path, include
from .views import (
    EnrolUsers,
    GetBooks,
    GetSingleBook,
    LoanBook,
    GetLoanedBooks,
    Users,
    UserDetail,
)

app_name = "client_api"
urlpatterns = [
    path(
        "books/",
        include(
            [
                path("", GetBooks.as_view(), name="books"),
                path("<int:id>/", GetSingleBook.as_view(), name="single-book"),
                path("<int:id>/borrow/", LoanBook.as_view()),
            ]
        ),
    ),
    path(
        "users/",
        include(
            [
                path("", Users.as_view(), name="enrol-user"),
                path("<int:id>/", UserDetail.as_view(), name="user-detail"),
            ]
        ),
    ),
    path("get-loaned-books/", GetLoanedBooks.as_view()),
]
