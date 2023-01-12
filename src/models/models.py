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
    role = relationship('Role', secondary=user_role, back_populates='users')

    def __str__(self) -> str:
        return self.username


class Role(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    users = relationship('User', secondary=user_role, back_populates='role')

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
    # comments = 


class Genre(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    games = relationship('Game', secondary=game_genre, back_populates='genres')


class Platform(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    games = relationship('Game', secondary=game_platform, back_populates='platforms')
