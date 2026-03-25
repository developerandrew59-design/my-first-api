from urllib import response

from fastapi.testclient import TestClient
from ahh import app
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
    


##this page only exiscts for reference, everything exicts within conftest.py

