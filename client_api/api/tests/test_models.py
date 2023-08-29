from datetime import datetime, timedelta

from django.test import TestCase

from ..models import User, LoanedBook, Book


# models test
class UserTest(TestCase):
    def setUp(self) -> None:
        User.objects.create(email="tesy@gmail.com", first_name="Tesy", last_name="yset")

    def test_object_returns_string_nrepresentation(self) -> None:
        user = User.objects.get(id=1)
        expected_output = f"{user.first_name} {user.last_name}"
        self.assertEqual(str(user), expected_output)


class BookTest(TestCase):
    def setUp(self) -> None:
        Book.objects.create(
            title="Things fall apart",
            author="Chinua Achebe",
            publisher="mannings",
            category="tragedy",
            borrowed=False,
        )

    def test_title(self) -> None:
        book = Book.objects.get(id=1)
        self.assertEqual(str(book), book.title)


class LoanedBookTest(TestCase):
    def setUp(self) -> None:
        book = Book.objects.create(
            title="Things fall apart",
            author="Chinua Achebe",
            publisher="mannings",
            category="tragedy",
            borrowed=False,
        )
        user = User.objects.create(
            email="tesy@gmail.com", first_name="Tesy", last_name="yset"
        )
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        LoanedBook.objects.create(
            book=book, user=user, date_borrowed=today, return_date=tomorrow
        )

    def test_title_and_email_returned(self) -> None:
        loaned_book = LoanedBook.objects.get(id=1)
        expected_output = f"{loaned_book.book.title}-{loaned_book.user.email}"
        self.assertEqual(str(loaned_book), expected_output)
