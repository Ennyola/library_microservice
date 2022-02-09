from django.contrib import admin
from .models import Book,BookLoaned,Member
# Register your models here.
admin.site.register(Book)
admin.site.register(BookLoaned)
admin.site.register(Member)