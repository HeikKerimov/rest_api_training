from api.service import *
from helpers.randomizer import get_random_value


def test_login_with_valid_data():
    """ This test checks an ability to login with valid data. """

    url = "{0}/login".format(HOST)

    # Send GET REST API request with basic auth:
    result = requests.get(url, auth=HTTPBasicAuth(USER, PASSWORD))
    data = result.json()

    # Verify that server returns some auth cookie:
    assert check_auth_cookie(data["auth_cookie"])
    assert result.status_code == 200


def test_login_with_invalid_data():
    """ This test checks that an user is not able to login with invalid data. """

    url = "{0}/login".format(HOST)

    # Send GET request with invalid data:
    result = requests.get(url, auth=HTTPBasicAuth(get_random_value(), get_random_value()))

    # Verify that server returns 401 status code:
    assert result.status_code == 401


def test_add_book():
    """ This test checks that an user is able to add a book. """

    url = "{0}/add_book".format(HOST)
    book = {"title": get_random_value(), "author": get_random_value()}

    # Send POST request to add a book:
    result = requests.post(url, data=book, cookies=auth_cookie())
    data = result.json()

    # Get id of created book:
    book["id"] = data["id"]

    # Get a list of books:
    books = get_books()

    # Verify that the book is present in the list:
    assert book in books
    assert result.status_code == 200


def test_add_book_without_data():
    """ This test checks that an user is able to add a book without a title and an author. """

    url = "{0}/add_book".format(HOST)

    # Send POST request without body to add a book:
    result = requests.post(url, cookies=auth_cookie())
    data = result.json()

    # Get id of created book:
    book = data

    # Get a list of books:
    books = get_books()

    # Verify that the book is present in the list:
    assert book in books
    assert result.status_code == 200


def test_add_book_with_upper_data():
    """ This test checks the case-sensitivity when creating a book. """

    url = "{0}/add_book".format(HOST)
    book = {"TITLE": get_random_value(), "AuThoR": get_random_value()}

    # Send POST request with invalid (UPPER parameters) data:
    result = requests.post(url, data=book, cookies=auth_cookie())
    data = result.json()

    # Get id of created book:
    book["id"] = data["id"]

    # Get a list of books:
    books = get_books()

    # Verify that the book is present in the list:
    assert book in books
    assert result.status_code == 200
    # TODO: BUG -- For now the method's parameters are case-sensitive


def test_add_book_with_int_data():
    """ This test checks a creating a book with integer data. """

    url = "{0}/add_book".format(HOST)
    book = {"title": get_random_value(numbers=True), "author": get_random_value(numbers=True)}

    # Send POST request with invalid (integer values) data:
    result = requests.post(url, data=book, cookies=auth_cookie())
    data = result.json()

    # Get id of created book:
    book["id"] = data["id"]

    # Get a list of books:
    books = get_books()

    # Verify that the book is present in the list:
    assert book in books
    assert result.status_code == 200
    # TODO: BUG -- The method doesn't support integer data. I guess it should change integer to string ( str(integer) )


def test_add_book_with_swapped_parameters():
    """ This test checks that method works correct with swapped data. """

    url = "{0}/add_book".format(HOST)
    book = {"author": get_random_value(), "title": get_random_value()}

    # Send POST request with swapped parameters:
    result = requests.post(url, data=book, cookies=auth_cookie())
    data = result.json()

    # Get id of created book:
    book["id"] = data["id"]

    # Get a list of books:
    books = get_books()

    # Verify that the book is present in the list:
    assert book in books
    assert result.status_code == 200


def test_delete_book():
    """ This test checks that an user is able to delete a book. """

    url = "{0}/add_book".format(HOST)
    book = {"title": get_random_value(), "author": get_random_value()}

    # Send POST request to add a book:
    result = requests.post(url, data=book, cookies=auth_cookie())
    data = result.json()

    # Get id of created book:
    book["id"] = data["id"]

    # Set new url with the book's ID
    url = "{0}/books/{1}".format(HOST, book["id"])

    # Send DELETE request to delete the book
    result = requests.delete(url, cookies=auth_cookie())

    # Get a list of books:
    books = get_books()

    # Verify that the book is not present in the list:
    assert book not in books
    assert result.status_code == 200


def test_delete_book_with_incorrect_id():
    """ This test checks correct error message if there is no a book with given ID. """

    # Set new url with the book's ID
    url = "{0}/books/{1}".format(HOST, get_random_value())

    # Send DELETE request to delete the book
    result = requests.delete(url, cookies=auth_cookie())

    # TODO: Expected result: the method returns some error message
    #  Now the method returns status code 200. I am not sure it is ok.


def test_get_book_method():
    """ This test checks that user is able to get a book by ID. """

    url = "{0}/add_book".format(HOST)
    book = {"title": get_random_value(), "author": get_random_value()}

    # Send POST request to add a book:
    result = requests.post(url, data=book, cookies=auth_cookie())
    data = result.json()

    # Get id of created book:
    book["id"] = data["id"]

    # Send GET request to get the book
    url = "{0}/books/{1}".format(HOST, book["id"])
    result = requests.get(url, cookies=auth_cookie())
    received_book = result.json()

    # Verify that books are equal:
    assert book == received_book
    assert result.status_code == 200


def test_get_book_with_incorrect_id():
    """ This test checks correct error message if there is no a book with given ID. """

    # Set new url with the book's ID
    id = get_random_value(numbers=True)
    url = "{0}/books/{1}".format(HOST, id)

    # Send GET request to get the book
    result = requests.get(url, cookies=auth_cookie())
    received_book = result.json()

    # TODO: Expected result: the method returns some error message.
    # Now the method returns status code 200 and empty body.


def test_get_book_with_not_auth_user():
    """ This test checks that user is not able to get a book by ID if he is not authorized. """

    url = "{0}/add_book".format(HOST)
    book = {"title": get_random_value(), "author": get_random_value()}

    # Send POST request to add a book:
    result = requests.post(url, data=book, cookies=auth_cookie())
    data = result.json()

    # Get id of created book:
    book["id"] = data["id"]

    # Send GET request to get the book
    url = "{0}/books/{1}".format(HOST, book["id"])
    result = requests.get(url)

    # TODO: Expected result: the method returns some error message.
    # Now the method returns status code 500.


def test_get_books():
    """ This test checks that user is able to get all books. """

    url = "{0}/add_book".format(HOST)
    book = {"title": get_random_value(), "author": get_random_value()}

    # Send POST request to add a book:
    result = requests.post(url, data=book, cookies=auth_cookie())
    data = result.json()

    # Get id of created book:
    book["id"] = data["id"]

    url = "{0}/books".format(HOST)

    # Send GET request to get all books
    result = requests.get(url, cookies=auth_cookie())

    books = result.json()

    # Verify that the book in a list of books:
    assert book in books
    assert result.status_code == 200


def test_sort_of_get_books():
    """ This test check that is user is able to sort a list of books by title. """

    # Check that a list of books is not empty
    if list_is_empty():
        for i in range(get_random_value(numbers=True, length=1)):
            add_book()

    # Get all books:
    books = get_books()

    # Sort books by title:
    books = [book['title'] for book in books]
    books = sorted(books)

    url = "{0}/books?sort=by_title".format(HOST)

    # Send GET request to get all books sorted by title:
    result = requests.get(url, cookies=auth_cookie())
    received_books = result.json()
    received_books = [book['title'] for book in received_books]

    # Verify that lists of books are equal:
    assert books == received_books
    assert result.status_code == 200


def test_limit_of_get_books():
    """ This test checks that user gets limited list of books"""

    limit = 1

    # Check that a list of books is not empty
    if list_is_empty():
        for i in range(get_random_value(numbers=True, length=1)):
            add_book()

    # Get all books:
    books = get_books()

    # Get limited list of books:
    books = books[:limit]

    url = "{0}/books?limit={1}".format(HOST, limit)

    # Send GET request to get limited books:
    result = requests.get(url, cookies=auth_cookie())
    received_books = result.json()

    # Verify that lists of books are equal:
    assert books == received_books
    assert result.status_code == 200


