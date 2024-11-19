from passlib.context import CryptContext

crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return crypto_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return crypto_context.verify(password, password_hash)
