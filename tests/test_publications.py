import pytest
import json
import requests


"""
STEPS TO RUN TEST(s) FOR `Publication` schema/table/model:
    STEP-1:
        - activate virtualenv and run the app.py (i.e flask app)

    STEP-2:
        - activate the same virtualenv in another shell/cmd window
        - run `pytest -s test_publications.py` command
        - the test result(s) will be seen on console along with response message(s)
"""

# .......base url of the App..........
base_url = "http://127.0.0.1:5000"

# .......demo user object data for the test case......
userData ={
  "email" : "change6@xyz.com",
  "password": "demoPassword"
}

demoBook= {
    "title": "The amazing Book",
    "description" : "This is my book description",
    "priority" : 3,
    "status": "Available"
}
#....... creating session to test the API ......
session = requests.Session()
session.headers.update([('Content-Type', 'application/json')])


# .......................... test cases for the Publication schema/model/table ..................... #


def test_user_login():
    """
     GIVEN the user have to authenticate first before making CRUD operation to Publication(s)
     WHEN existing user sign in
     THEN check the login response when user try to sign in with email and password
    """
    url = base_url + "/login"
    data = json.dumps(userData)
    res = session.post(url, data= data)
    print(f"\n Login response: {res.json()}\n")
    assert res.status_code == 200


@pytest.mark.skip
def test_addbook():
    """
     GIVEN a Publication model
     WHEN an authenticated user tries to insert new data record in table
     THEN check if the fields are defined/saved correctly
    """
    url = base_url + "/addbook"
    data = json.dumps(demoBook)
    res = session.post(url, data= data)
    print(f"\n Add Book response: {res.json()}\n")
    assert res.status_code == 200


@pytest.mark.skip
@pytest.mark.parametrize(
    "data,id",[({'title':'new title1'},2),({'status':'sold'},9)]
)
def test_update_book(data, id):
    """
     GIVEN a Publication model
     WHEN an authenticated user tries to update existing data record in table
     THEN check the response when user try to change existing info/column-data
    """
    url = base_url + f"/updatebook/{id}"
    res = session.put(url, data= json.dumps(data) )
    print(f"\n updated Book info: {res.json()}\n")
    assert res.status_code == 200 or 404


@pytest.mark.parametrize("id",[1,2,3,4,566,13,12,11,0])
def test_getbook(id):
    """
     GIVEN a Publication model
     WHEN an authenticated user tries to fetch an existing record from table by book/record id
     THEN check the response when user try to fetch a specific book.
    """
    url = base_url + f"/getbook/{id}"
    res = session.get(url)
    print(f"\n getBook response: {res.json()}\n")
    assert res.status_code == 200 or 404


@pytest.mark.skip
@pytest.mark.parametrize("id",[1,2,11])
def test_delete_book(id):
    """
     GIVEN a Publication model
     WHEN an authenticated user delete an existing record from table
     THEN check the response when user try to remove a book from DB.
    """
    url = base_url + f"/deletebook/{id}"
    res = session.delete(url)
    print(f"\n Book delete response: {res.json()}\n")
    assert res.status_code == 200 or 404
