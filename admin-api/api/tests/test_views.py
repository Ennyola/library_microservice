import imp
from django.test import TestCase,Client
from ..views import UnavailableBooks,UserBookBorrowed, get_loaned_books
# views test

class TestViews(TestCase):
    def test_get_loaned_books(self):
        pass