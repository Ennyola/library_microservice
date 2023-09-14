from django.contrib import admin

from .models import Book, LoanedBook, User

# Register your models here.


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publisher", "category", "borrowed")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name")


@admin.register(LoanedBook)
class LoanedBookAdmin(admin.ModelAdmin):
    list_display = ("get_user", "get_book", "date_borrowed", "return_date")

    def get_user(self, obj: LoanedBook) -> str:
        """Returns the email of the user loaning a book

        Args:
            obj (LoanedBook): An instance of LoanedBook

        Returns:
            str: The User email
        """
        return obj.user.email

    def get_book(self, obj: LoanedBook) -> str:
        """Returns the book title being loaned

        Args:
            obj (LoanedBook): An instance of LoanedBook

        Returns:
            str: The Loaned book title
        """
        return obj.book.title
