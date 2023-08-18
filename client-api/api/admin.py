from django.contrib import admin

from .models import Book, LoanedBook, User

# Register your models here.
admin.site.register(Book)
admin.site.register(LoanedBook)
admin.site.register(User)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publisher", "category", "borrowed")
