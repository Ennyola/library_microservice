""" A python module containing typed dictionaries for our application """

from typing import TypedDict
from datetime import date

from .models import Book


class LoanedBookEventData(TypedDict):
    """A TypeDict specifying data sent to the worker in the signal handler"""

    date_borrowed: date
    return_date: date
    book_id: int
    user_id: int


class LoanedBookValidationData(TypedDict):
    """A TypeDict specifying data from the validation data in LoanedBookSerializer"""

    email: str
    duration: int
    book: Book
