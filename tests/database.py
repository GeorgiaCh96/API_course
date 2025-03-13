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

#from tests.test_users import override_get_db

#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/fastapi_test'  # postgresname:password
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
print(settings.database_name)
print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

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
