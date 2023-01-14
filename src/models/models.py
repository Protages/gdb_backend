from sqlalchemy import Column, Table, ForeignKey, Integer, String, Boolean, Date
from sqlalchemy.orm import relationship

from src.db.database import Base


# class Token(Base):
#     access_token = Column(String)
#     username = Column(String, uniqe=True)
#     expire = Column(String)


user_role = Table(
    'user_role',
    Base.metadata,
    Column('user_id', ForeignKey('user.id')),
    Column('role_id', ForeignKey('role.id')),
)


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    about = Column(String)
    rating = Column(Integer, default=0)
    roles = relationship('Role', secondary=user_role, back_populates='users')
    comments = relationship('Comment', back_populates='user')
    reviews = relationship('Review', back_populates='author')
    grades = relationship('Grade', back_populates='user')
    categories = relationship('Category', back_populates='user')

    def __str__(self) -> str:
        return self.username


class Role(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    users = relationship('User', secondary=user_role, back_populates='roles')

    def __str__(self) -> str:
        return self.title


game_genre = Table(
    'game_genre',
    Base.metadata,
    Column('game_id', ForeignKey('game.id')),
    Column('genre_id', ForeignKey('genre.id')),
)


game_platform = Table(
    'game_platform',
    Base.metadata,
    Column('game_id', ForeignKey('game.id')),
    Column('platform_id', ForeignKey('platform.id')),
)


game_category = Table(
    'game_category',
    Base.metadata,
    Column('game_id', ForeignKey('game.id')),
    Column('category_id', ForeignKey('category.id'))
)


class Game(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    img = Column(String)
    genres = relationship('Genre', secondary=game_genre, back_populates='games')
    platforms = relationship(
        'Platform', secondary=game_platform, back_populates='games'
    )
    description = Column(String)
    release = Column(Date)
    developer = Column(String)
    production = Column(String)
    system_requirements = Column(String)
    time_to_play = Column(Integer)
    comments = relationship('Comment', back_populates='game')
    reviews = relationship('Review', back_populates='game')
    grades = relationship('Grade', back_populates='game')
    categories = relationship(
        'Category', secondary=game_category, back_populates='games'
    )


class Review(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('user.id'))
    author = relationship('User', back_populates='reviews')
    game_id = Column(Integer, ForeignKey('game.id'))
    game = relationship('Game', back_populates='reviews')
    body = Column(String)
    likes = Column(Integer, default=0)
    rating_minus = Column(Integer)
    comments = relationship('Comment', back_populates='review')


class Genre(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    games = relationship('Game', secondary=game_genre, back_populates='genres')


class Platform(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    games = relationship('Game', secondary=game_platform, back_populates='platforms')


class Comment(Base):
    id = Column(Integer, primary_key=True, index=True)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='comments')
    game_id = Column(Integer, ForeignKey('game.id'))
    game = relationship('Game', back_populates='comments')
    review_id = Column(Integer, ForeignKey('review.id'))
    review = relationship('Review', back_populates='comments')


class Grade(Base):
    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))
    game_id = Column(Integer, ForeignKey('game.id'))
    user = relationship('User', back_populates='grades')
    game = relationship('Game', back_populates='grades')


class Category(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='categories')
    games = relationship('Game', secondary=game_category, back_populates='categories')
