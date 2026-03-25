from urllib import response
from jose import jwt
from config import settings
import schemas
import pytest
def test_root(client):
    response=client.get("/")
    print(response.json().get('message'))
    assert (response.json().get('message'))=="lets gooo!!!"
    assert response.status_code==200


def test_create_user(client):
    response=client.post("/users/",json={"email":"hello523@email.com","password":"password123"})    
    print(response.json())
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "hello523@email.com"
    assert response.status_code==201


def test_login_user(client,test_users):
    response=client.post("/login",data={"username":test_users['email'],"password":test_users['password']}) 
    login_res=schemas.Token(**response.json())
    payload=jwt.decode(login_res.acess_token,settings.secret_key,algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id==test_users['id']
    assert login_res.token_type=="bearer"
    assert response.status_code==200    
@pytest.mark.parametrize("email,password,status_code",
                         [("wrong@email.com", "some", 403),
                          ("laptop@email.com", "wrongpassword", 403),
                          ("wrong@email.com", "wrongpassword", 403),
                          (None, "some", 422),
                          ("laptop@email.com", None, 422)])
def test_failed_login(test_users,client,email,password,status_code):
    response=client.post("/login",data={"username":email,"password": \
    password})

    assert response.status_code==status_code
    

