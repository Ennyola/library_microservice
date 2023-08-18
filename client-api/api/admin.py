from django.contrib import admin

from .models import Book, LoanedBook, User

# Register your models here.
admin.site.register(LoanedBook)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publisher", "category", "borrowed")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name")
