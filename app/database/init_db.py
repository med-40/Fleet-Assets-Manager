from app.database.session import engine
from app.database.base import Base

# تحميل جميع النماذج
from app import models


def create_database():

    Base.metadata.create_all(
        bind=engine
    )

    print("Database created successfully")


if __name__ == "__main__":

    create_database()
