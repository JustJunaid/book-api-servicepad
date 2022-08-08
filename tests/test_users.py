import pytest
import json
import requests


"""
STEPS TO RUN TEST(s) FOR `User` schema/table/model:
    STEP-1:
        - start virtualenv and run the app.py (i.e flask app)

    STEP-2:
        - activate the same virtualenv in another shell/cmd window
        - run `pytest -s test_users.py` command
        - the test result(s) will be seen on console with response message(s)
"""

# .......base url of the App..........
base_url = "http://127.0.0.1:5000"

# .......demo user object data for the test case......
userData ={
  "username": "demoName",
  "email" : "mydemoEmail@xyz.com",
  "password": "demoPassword"
}

#....... creating session to test the API ......
session = requests.Session()
session.headers.update([('Content-Type', 'application/json')])


# .......................... test cases for the user schema/model/table ..................... #

# @pytest.mark.skip
def test_user_signup():
   """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, email and password fields are defined/saved correctly
   """
   url = base_url + "/signup"
   data = json.dumps(userData)
   res = session.post(url, data= data)
   print(f"\nSign up response: {res.json()}\n")
   assert res.status_code == 200


def test_user_login():
    """
     GIVEN a User model
     WHEN existing user sign in
     THEN check the login response when user try to sign in with email and password
    """
    url = base_url + "/login"
    data = json.dumps({"email":userData['email'], "password": userData['password']})
    res = session.post(url, data= data)
    print(f"\n Login response: {res.json()}\n")
    assert res.status_code == 200


# @pytest.mark.skip
def test_user_info():
    """
     GIVEN a User model
     WHEN existing user's information is asked
     THEN check the response when user ask for self information
    """
    url = base_url + "/user"
    res = session.get(url)
    print(f"\n User info response: {res.json()}\n")
    assert res.status_code == 200


@pytest.mark.skip
@pytest.mark.parametrize(
    "data",
    [
      {"username": "username2"},
      {"username": "username3", "password": "password2"},
    ]
)
def test_update_user_info(data):
    """
     GIVEN a User model
     WHEN existing user's information is updated
     THEN check the response when user try to change existing info/column-data
    """
    url = base_url + "/update-user-info"
    res = session.put(url, data= json.dumps(data) )
    print(f"\n updated info: {res.json()}\n")
    assert res.status_code == 200


@pytest.mark.skip
def test_update_user_dp():
    """
     GIVEN a User model
     WHEN existing user try to update its profile picture
     THEN check the response when user try to update/change DP
    """
    image_path = r"C:\Users\91868\Pictures\Screenshots\a.png" #change this to target image
    with open(image_path,'rb') as img:
        new_image= img
        url = base_url + "/update-dp"
        files = {'image': new_image}
        res = session.put(url, files= files)
    print(f"\n updated DP info: {res.json()}\n")
    assert res.status_code == 200


#........keep/call this function at last delete demo user after test ended....
def test_delete_user():
    """
     GIVEN a User model
     WHEN existing user try to delete account
     THEN check the response when user tries to delete account
    """
    url = base_url + "/delete-user"
    res = session.delete(url)
    print(f"\n User delete response: {res.json()}\n")
    assert res.status_code == 200
