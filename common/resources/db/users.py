from sqlalchemy import create_engine, Column, Integer, String, Sequence, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from common.utils.utils import get_binary

engine = create_engine('sqlite:///../common/resources/db/tvtracker.sqlite', echo=False)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True)
    email = Column(String)
    role = Column(String, default='end_user')
    pic = Column(BLOB, default=get_binary('../common/resources/icons/default_av.png'))
    password = Column(String) # need to hash this, temporary model

    def __repr__(self):
        return f'User(username={self.username},email={self.email},role={self.role},hashed_password={self.password})'


Base.metadata.create_all(engine)
Session = sessionmaker(engine, expire_on_commit=False)
