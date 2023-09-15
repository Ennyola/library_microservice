from rest_framework.routers import DefaultRouter

from .views import BookViewSet, UsersViewset, UserBookBorrowed, UnavailableBooks


router = DefaultRouter()
router.register(r"books", BookViewSet)
router.register(r"users", UsersViewset)
router.register(r"user-books-borrowed", UserBookBorrowed, basename="user-books")
router.register(r"unavailable-books/", UnavailableBooks, basename="unavailable-books")

urlpatterns = []

urlpatterns += router.urls
