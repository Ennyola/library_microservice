
from django.contrib import admin

from .models import Book,LoanedBook,User

# Register your models here.
admin.site.register(Book)
admin.site.register(LoanedBook)
admin.site.register(User)