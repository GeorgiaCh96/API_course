from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# encrypt passwords (hashing)
def hash(password: str):
    return pwd_context.hash(password)


# verify if hashed(plain_password) == hashed_password
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)   