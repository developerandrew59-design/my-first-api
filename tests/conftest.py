from fastapi.testclient import TestClient
from ahh import app
import models
from oauth2 import create_access_token
import schemas
from config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database import get_db,Base
import pytest

#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/fastapi_test"
SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine=create_engine(SQLALCHEMY_DATABASE_URL)
TestingsessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)


@pytest.fixture()
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingsessionLocal() 
    try:
        yield db         
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        yield session
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
@pytest.fixture()
def test_users(client):
    user_data={"email":"laptop@email.com",
               "password":"some"}
    response=client.post("/users/",json=user_data)
    new_user=response.json()
    new_user['password']=user_data["password"]
    assert response.status_code==201
    return new_user

@pytest.fixture()
def test_users2(client):
    user_data={"email":"laptop123@email.com",
               "password":"some"}
    response=client.post("/users/",json=user_data)
    new_user=response.json()
    new_user['password']=user_data["password"]
    assert response.status_code==201
    return new_user

@pytest.fixture()
def test_token(test_users):
    return create_access_token({"user_id": test_users['id']})

@pytest.fixture()
def authorization(client,test_token):
    client.headers={
        **client.headers,
        "Authorization": f"Bearer {test_token}"
    }
    return client
    
@pytest.fixture()
def test_posts_andy(test_users,session,test_users2):
        posts_data = [
        {"title": "first title", "content": "first content", "account_id": test_users['id']},
        {"title": "second title", "content": "second content", "account_id": test_users['id']},
        {"title": "third title", "content": "third content", "account_id": test_users['id']},
        {"title": "fouth title", "content": "fourth content", "account_id": test_users2['id']}]


        def create_test_post_model(post):
            return models.Post(**post)

        postmap=map(create_test_post_model,posts_data)
        posts=list(postmap)  


        session.add_all(posts) 

#        session.add_all([
#    models.Post(title="first title", content="first content", owner_id=test_users['id']),
#    models.Post(title="second title", content="second content", owner_id=test_users['id']),
#    models.Post(title="third title", content="third content", owner_id=test_users['id']),
#])
        session.commit()

        posts=session.query(models.Post).all()
        return posts

        

        


        
