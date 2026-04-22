from app.core.errors import ConflictError, NotFoundError, UnauthorizedError
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.users import UserRepository


class AuthUseCase:
    def __init__(self, users_repo: UserRepository):
        self._users_repo = users_repo

    async def register(self, email: str, password: str):
        existing_user = await self._users_repo.get_by_email(email)
        if existing_user is not None:
            raise ConflictError("Email already registered")

        password_hash = hash_password(password)
        return await self._users_repo.create(
            email=email,
            password_hash=password_hash,
            role="user",
        )

    async def login(self, email: str, password: str) -> str:
        user = await self._users_repo.get_by_email(email)
        if user is None:
            raise UnauthorizedError("Invalid email or password")

        if not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")

        return create_access_token(
            {
                "sub": str(user.id),
                "role": user.role,
            }
        )

    async def get_profile(self, user_id: int):
        user = await self._users_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")
        return user
