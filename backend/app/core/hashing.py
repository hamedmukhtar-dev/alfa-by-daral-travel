from passlib.context import CryptContext

# Password hashing context with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash:
    """
    Clean hashing handler for password operations.
    """

    @staticmethod
    def bcrypt(password: str) -> str:
        """
        Hash a password using bcrypt.
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        """
        Verify a password against a hashed version.
        """
        return pwd_context.verify(plain_password, hashed_password)
