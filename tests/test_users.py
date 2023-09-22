import pytest
from app import schemas
from jose import jwt
from app.config import settings


# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == "Bind mount works! Great"
#     assert res.status_code == 200

    

def test_create_user(client):
    res = client.post("/users/", json={"email": "hello@gmail.com", "password": "password123"})

    new_user = schemas.UserOut(**res.json()) #Performs validation - id, email, created_at
    assert new_user.email =="hello@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    print(res.json())
    login_res = schemas.Token(**res.json())  #performs validation
    #Validating the token
    payload = jwt.decode(login_res.accessToken, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("userId")
    assert id == test_user['id']
    assert login_res.tokenType == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'john123', 403),
    ('john@gmail.com', 'asdgasdg', 403),
    ('wrongemail@gmail.com', 'asdgasdg', 403),
    (None, 'john123', 422),
    ('john@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'