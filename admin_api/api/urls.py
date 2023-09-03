from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    BookView,
    UsersViewset,
    # UserBookBorrowed,
    # UnavailableBooks,
)


router = DefaultRouter()
router.register(r"books", BookView)
router.register(r"users", UsersViewset)

urlpatterns = [
    # path(
    #     "books/",
    #     include(
    #         [
    #             path("", CreateBook.as_view(), name="create-book"),
    #             path("<int:pk>/", DeleteBook.as_view(), name="delete-book"),
    #         ]
    #     ),
    # ),
    # path("users/", GetUsers.as_view(), name="get-users"),
    # path("user-books-borrowed/", UserBookBorrowed.as_view()),
    # path("unavailable-books/", UnavailableBooks.as_view()),
]

urlpatterns += router.urls
