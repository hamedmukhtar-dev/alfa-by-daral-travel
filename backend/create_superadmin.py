import asyncio

from app.db import AsyncSessionLocal
from app.models.user import User
from app.core.hashing import hash_password
from sqlalchemy import select


SUPERADMIN_EMAIL = "hamed.mukhtar@daral-sd.com"
SUPERADMIN_PASSWORD = "DARAL2025!"
SUPERADMIN_NAME = "Hamed Mukhtar"


async def create_or_update_superadmin():
    async with AsyncSessionLocal() as session:
        # Check if user already exists
        result = await session.execute(
            select(User).where(User.email == SUPERADMIN_EMAIL)
        )
        user = result.scalar_one_or_none()

        if user:
            # Update existing user
            user.full_name = SUPERADMIN_NAME
            user.password_hash = hash_password(SUPERADMIN_PASSWORD)
            user.is_active = True
            user.is_admin = True
            user.role = "superadmin"

            await session.commit()
            print("✅ SuperAdmin updated successfully.")

        else:
            # Create new superadmin
            admin = User(
                full_name=SUPERADMIN_NAME,
                email=SUPERADMIN_EMAIL,
                password_hash=hash_password(SUPERADMIN_PASSWORD),
                is_active=True,
                is_admin=True,
                role="superadmin",
            )

            session.add(admin)
            await session.commit()
            print("✅ SuperAdmin created successfully.")


if __name__ == "__main__":
    asyncio.run(create_or_update_superadmin())
