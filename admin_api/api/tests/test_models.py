import datetime
from django.test import TestCase
from ..models import Member,BookLoaned,Book
# models test

class MemberTest(TestCase):
    def setUp(self):
        Member.objects.create(email="tesy@gmail.com",first_name="Tesy",last_name="yset")
     
    #testing the string methode in Member class   
    def test_object_name_is_last_name_comma_first_name(self):
        member = Member.objects.get(id=1)
        expected_output = f'{member.first_name} {member.last_name}'
        self.assertEqual(str(member),expected_output)
        
class BookTest(TestCase):
    def setUp(self):
        Book.objects.create(title="Things fall apart",author="Chinua Achebe",publisher="mannings", category="tragedy",year_published=1978, borrowed=False)
        
    def test_title(self):
        book=Book.objects.get(id=1)
        self.assertEqual(str(book),book.title)
        
class BookLoanedTest(TestCase):
    def setUp(self):
        book = Book.objects.create(title="Things fall apart",author="Chinua Achebe",publisher="mannings", category="tragedy",year_published=1978, borrowed=False)
        user = Member.objects.create(email="tesy@gmail.com",first_name="Tesy",last_name="yset")
        BookLoaned.objects.create(book=book,user=user,duration=datetime.timedelta(days=7))
        
        
    def test_title_and_email_returned(self):
        bookloaned=BookLoaned.objects.get(id=1)
        expected_output = f"{bookloaned.book.title}-{bookloaned.user.email}"
        self.assertEqual(str(bookloaned),expected_output)