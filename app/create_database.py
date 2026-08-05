from app.database.base import Base
from app.database.session import engine

# تحميل جميع النماذج
from app.models import User
from app.models import Role
from app.models import Permission


def create_database():
    Base.metadata.create_all(
        bind=engine
    )

    print("Database created successfully.")


if __name__ == "__main__":
    create_database()
