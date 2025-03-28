from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models
#from tests.test_users import override_get_db




#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/fastapi_test'  # postgresname:password
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
print(settings.database_name)


try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    with engine.connect() as connection:
        print("✅ Successfully connected to the database!")
except Exception as e:
    print("❌ Database connection failed:", e)



TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base.metadata.create_all(bind=engine)  # will automatically create all tables in the test database

# Dependency for database sessions
#def override_get_db():  # gives different session object (will overwrite our local DB )
#    db = TestingSessionLocal()
#    try:
#        yield db
#    finally:
#        db.close()




@pytest.fixture()
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine) 
    Base.metadata.create_all(bind=engine) 
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        # run this before we run our test
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield  TestClient(app)
    # run this code after our code finishes


@pytest.fixture
def test_user(client):
    user_data = {"email": "georgia@gmail.com",
              "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "georgia123@gmail.com",
              "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']

    },
    {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']

    }  ,
    {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']

    } ,
    {
        "title": "4th title",
        "content": "4th content",
        "owner_id": test_user2['id']

    }   ]


    def create_post_model(post):
        return models.Post(**post)


    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)

    #session.add_all([models.Post(title="first title", content="first content", owner_id =  test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id =  test_user['id'])])
    
    session.commit()

    posts = session.query(models.Post).all()

    return posts
