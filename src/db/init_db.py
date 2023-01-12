from sqlalchemy.orm import Session

from src.db.database import Base, engine
from src.models.models import User, Role
from src.core.security import create_hashing_password


def init_db(db: Session):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    user_admin = User(
        username='admin',
        hashed_password=create_hashing_password('mypass'),
        email='admin@a.ru',
        about='Just my admin',
        rating=10
    )
    user_2 = User(
        username='Jony',
        hashed_password=create_hashing_password('mypass'),
        email='jony@a.ru',
        about='Just my profile',
        rating=3
    )

    role_1 = Role(title='Role Admin')
    role_2 = Role(title='Role Creator')

    user_admin.role.append(role_1)
    user_admin.role.append(role_2)

    db.add_all([user_admin, user_2, role_1, role_2])
    db.commit()
    db.close()
