import datetime

from sqlalchemy.orm import Session

from src.db.database import Base, engine
from src.models.models import (
    User, 
    Role, 
    Genre, 
    Platform,
    Game, 
    Review, 
    Comment, 
    Grade, 
    Category
)
from src.core.security import create_hashing_password


def init_db(db: Session):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    user_admin = User(
        username='admin',
        hashed_password=create_hashing_password('mypass'),
        email='admin@a.ru',
        about='Just my admin',
        rating=10,
        is_superuser=True
    )
    user_2 = User(
        username='Jony',
        hashed_password=create_hashing_password('mypass'),
        email='jony@a.ru',
        about='Just my profile',
        rating=3
    )
    user_3 = User(
        username='Dany',
        hashed_password=create_hashing_password('mypass'),
        email='dany@a.ru',
        about='Just my profile',
        rating=5
    )

    role_1 = Role(title='Role Admin')
    role_2 = Role(title='Role Creator')

    genre_1 = Genre(title='Strategy')
    genre_2 = Genre(title='Adventure')

    platform_1 = Platform(title='PC')
    platform_2 = Platform(title='PlayStation 4')

    game_1 = Game(
        title='GTA 5',
        description='GTA 5 the best game!',
        release=datetime.date(2017, 9, 11),
        developer='Rockstar Game',
        production='Rockstar Game',
        system_requirements='Minimal: some_req\nRecomendation: some_req',
        time_to_play=50
    )
    game_2 = Game(
        title='Battlefield 4',
        description='Battlefield the best game!',
        release=datetime.date(2015, 10, 11),
        developer='EA DICE',
        production='EA',
        system_requirements='Minimal: some_req\nRecomendation: some_req',
        time_to_play=60
    )

    grade_1 = Grade(user=user_admin, game=game_1, score=9)
    grade_2 = Grade(user=user_admin, game=game_2, score=8)

    review_1 = Review(
        title='Review on GTA 5',
        author=user_admin,
        game=game_1,
        body='My review on GTA 5',
        likes=5
    )
    review_2 = Review(
        title='Review on BATTLEFIEL 4',
        author=user_admin,
        game=game_2,
        body='My review on BATTLEFIEL 4',
        likes=3
    )

    comment_1 = Comment(user=user_admin, game_id=1, body='My comment 1 on GTA 5')
    comment_2 = Comment(user=user_admin, review_id=1, body='My comment 1 on Review on GTA 5')
    comment_3 = Comment(user=user_2, game_id=2, body='My comment 2 on GTA 5')
    comment_4 = Comment(user=user_2, review_id=2, body='My comment 2 on Review on GTA 5')

    category_1 = Category(title='My category 1', user=user_admin)
    category_2 = Category(title='My category 2', user=user_admin)

    game_1.genres.append(genre_1)
    game_1.genres.append(genre_2)
    game_1.platforms.append(platform_1)
    game_1.platforms.append(platform_2)

    game_2.genres.append(genre_1)
    game_2.platforms.append(platform_1)

    category_1.games.append(game_1)
    category_1.games.append(game_2)

    user_admin.roles.append(role_1)
    user_admin.roles.append(role_2)

    db.add_all([
        user_admin, user_2, user_3, 
        role_1, role_2,
        genre_1, genre_2,
        platform_1, platform_2,
        game_1, game_2,
        grade_1, grade_2,
        review_1, review_2,
        comment_1, comment_2, comment_3, comment_4,
        category_1, category_2
    ])
    db.commit()
    db.close()
