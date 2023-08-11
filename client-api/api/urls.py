from django.urls import path, include
from .views import EnrolUsers,GetBooks, GetSingleBook,LoanBook,GetLoanedBooks,Users

app_name = "api"
urlpatterns = [
    path('books/', include([path('', GetBooks.as_view(), name="books"),
                            path('<int:id>/', GetSingleBook.as_view(), name="single-book"),
                            path('<int:id>/borrow/',LoanBook.as_view())
                            ])),
    path('enrol-user/',EnrolUsers.as_view(), name="enrol-user"),
    path('users/', Users.as_view(), name="users"),
    path('get-loaned-books/',GetLoanedBooks.as_view())
    
    
]
