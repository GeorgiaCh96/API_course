from app import schemas
import pytest
from jose import jwt
from app.config import settings


#def test_root(client):
#    res = client.get("/")
#    print(res.json().get('message'))
#    assert res.json().get('message') == "Welcome to my NEW API! Bind mount works"
#    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json())  # checks if schema properties are included


    assert new_user.email =="hello123@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload =  jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])  # decode token using SECRET_KEY and ALGORITHM
    id = payload.get("user_id")  # extract id
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200



#@pytest.mark.parametrize("email, password, status_code", [
#    (
#        ('wrongemail@gmail.com', 'password123', 403),
#        ('sanjeev@gmail.com', 'wrongpassword', 403),
#        ('wrongemail@gmail.com', 'wrongpassword', 403),
#        (None, 'password123', 422)
#    )
#])
@pytest.mark.parametrize("data, status_code", [
    ({"email": "wrongemail@gmail.com", "password": "password123"}, 403),
    ({"password": "password123"}, 422)  # Missing email key instead of None
])
def test_incorrect_login( client, data, status_code):
    res = client.post("/login", json=data)

    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid credentials'