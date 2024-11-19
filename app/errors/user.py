from .base import CustomError


class UserAlreadyExistsError(CustomError):
    def __init__(self, email: str) -> None:
        super().__init__(f"user with email={email} already exists")
