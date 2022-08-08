
# Book Publication - Flask API
This API is developed by using python flask. The key features of this API are :



## Features

- Built with pure python | [Flask](https://flask.palletsprojects.com/en/2.2.x/)
- User authentication
- CRUD operations for book(s) & user(s)
- Test implementation  with python's [pytest](https://docs.pytest.org/en/7.1.x/)
- In-Built [Swagger](https://flask-restplus.readthedocs.io/en/0.9.0/swagger.html) Documentation



## API Reference

### User operation(s)

```https
  POST /signup
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required*. Username |
| `email` | `string` | **Required*. Email-id |
| `password` | `string` | **Required*. Password |

```https
  POST /login
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `email` | `string` | **Required*. Email-id |
| `password` | `string` | **Required*. Password |

```https
  PUT /update-dp
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `image` | `string($binary)` | **Required*. Image |


```https
  PUT /update-user-info
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Optional*. Username |
| `email` | `string` | **Optional*. Email-id |
| `password` | `string` | *Optional*. Password |

```http
  GET /user
```

  _*get current logged in user account info from DB._

```http
  DELETE /delete-user
```
   _*Deletes current logged in user account/info from DB._
   **Returns** (example):
   ```http
   {
  "status": 200,
  "userInfo": {
    "authenticated": true,
    "email": "shah@john.com",
    "image": "tony1.jpg",
    "password": "shah",
    "username": "john snow"
  }
}
   
   ```

```http
  GET /logout
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `None`      | `None` | log out current user


### Book Publication operation(s)

```http
  POST /addbook
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `title`      | `string` | **Required* Title of the book |
| `description`      | `string` | **Required* Description of the book |
| `priority`      | `number` | **Required* Priority of the book |
| `status`      | `string` | **Required* Current status of the book |

```http
  PUT /updatebook/{id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `title`      | `string` | **Required* Title of the book |
| `description`      | `string` | **Required* Description of the book |
| `priority`      | `number` | **Required* Priority of the book |
| `status`      | `string` | **Required* Current status of the book |

```http
  GET /getbook/{id}
```
**Returns** (example):
```http
{
  "created_at": "2022-08-08 07:50:36.556437",
  "description": "my book description",
  "id": 14,
  "priority": "2",
  "status": "Available",
  "time_since_published": "1:00:47.154837",
  "title": "The gret title",
  "updated_at": "2022-08-08 07:51:46.677554",
  "user": "shah@john.com"
}
```
```http
  DELETE /deletebook/{id}
```

 _*Deletes the book from DB (after permission check)._




## Swagger Documentation

The Swagger API docs for the app can be accessed via
```http
  /api/docs
```
All the available features can be accessed at Swagge docs.
## Running Tests via Pytest
The `test_users.py` & `test_publishers.py` files contains all available unit tests

To run tests, use the following steps

- #### Steps to run test(s) FOR `User` and `Publication` methods/routes:

```bash
    STEP-1:
        - start virtualenv and run the app.py (i.e flask app)

    STEP-2:
        - activate the same virtualenv in another shell/cmd window
        - run `pytest -s test_users.py` command
        - the test result(s) will be seen on console with response message(s)
```

