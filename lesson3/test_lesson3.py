import pytest
from api.utils import *


@pytest.fixture(scope='function')
def create_books():
    """ This fixture create three books """

    # Get the list of books:
    all_books = get_all_books()

    # If the list is empty then create some books:
    if len(all_books) == 0:
        add_book({'title': 'Python', 'author': 'Gogol'})
        add_book({'title': 'QA', 'author': 'Heik'})
        add_book({'title': 'Ali', 'author': 'Ali'})


def test_login():
    """ This test checks that user is able to login """

    # Login and get auth_cookie:
    cookies = auth()

    # Verify that auth_cookie is correct:
    assert validate_uuid4(cookies.get('my_cookie'))


@pytest.mark.parametrize('title', ['', 'some test', u'тест', '&^#*@(', 'a'*1000000])
@pytest.mark.parametrize('author', ['', 'Some Author', u'Хэйк', '@*&$^@%', 'b'*1000000])
def test_create_book(title, author):
    """ This test checks that user is able to add a book """

    # Create new book:
    book = {'title': title, 'author': author}
    new_book = add_book(book)

    # Get the list of books:
    all_books = get_all_books()

    # Verify that new book is present in the list of books:
    assert new_book in all_books


def test_delete_book():
    """ This test checks that user is able to delete a book """

    # Create new book:
    book = {'title': 'some title', 'author': 'some author'}
    new_book = add_book(book)

    # Delete this book:
    delete_book(book_id=new_book['id'])

    # Get the list of books:
    all_books = get_all_books()

    # Verify that deleted book is not present in the list of books:
    assert new_book not in all_books


@pytest.mark.parametrize('title', ['', 'some test', u'тест', '&^#*@(', 'a'*1000000])
@pytest.mark.parametrize('author', ['', 'Some Author', u'Хэйк', '@*&$^@%', 'b'*1000000])
def test_update_book(title, author):
    """ This test checks that user is able to update a book """

    # Create a book:
    new_book = add_book({'title': '', 'author': ''})
    book_id = new_book['id']

    # Update book attributes:
    update_book(book_id, {'title': title, 'author': author})

    # Get info about this book:
    book = get_book(book_id)

    # Verify that changes were applied correctly:
    assert book['title'] == title
    assert book['author'] == author


def test_get_book(title, author):
    """ This test checks that user is able to get a book by ID """

    # Create a book:
    new_book = add_book({'title': title, 'author': author})

    # Get book by ID:
    book = get_book(book_id=new_book['id'])

    # Verify that books are equal
    assert new_book == book


def test_get_all_books(create_books):
    """ This test checks that user is able to get all books """

    # Get the list of all books:
    all_books = get_all_books()

    # Check that every book in the list has all required attributes:
    for book in all_books:
        assert 'title' in book
        assert 'author' in book
        assert validate_uuid4(book['id'])

    # Make sure that the list has at least 2 books:
    assert len(all_books) >= 2


def test_sort(create_books):
    """ This test checks that user is able to get sorted list of books """

    # Get sorted list of all books:
    sorted_books = get_all_books(sort='by_title')

    # Get the list of books:
    books = get_all_books()

    # Sort these books:
    books = sorted(books, key=lambda x: x['title'])

    # Verify that lists are equal:
    assert sorted_books == books


@pytest.mark.parametrize('limit', [0, 1, 1000000])
def test_limit(create_books, limit):
    """ This test checks that user is able to get limite list of books """

    # Get limited list of books:
    limited_books = get_all_books(limit=limit)

    # Get the list of books:
    books = get_all_books()

    # Limit this list:
    books = books[:limit]

    # Verify that lists are equal:
    assert limited_books == books


def test_limit_and_sort(create_books):
    """ This test checks combination of sort and limit options """

    limit = 2

    # Get sorted and limited list of books:
    filtered_books = get_all_books(sort="by_title", limit=limit)

    # Get the list of books:
    books = get_all_books()

    # Filter this list:
    books = sorted(books, key=lambda x: x['title'])
    books = books[:limit]

    # Verify that lists are equal:
    assert filtered_books == books