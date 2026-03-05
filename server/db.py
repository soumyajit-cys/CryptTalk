from sqlalchemy import create_engine, Column, String, LargeBinary, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///securechat.db"  # change to PostgreSQL in prod

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True)
    password_hash = Column(String)
    identity_key = Column(LargeBinary)
    signed_prekey = Column(LargeBinary)
    spk_signature = Column(LargeBinary)


class OneTimePreKey(Base):
    __tablename__ = "one_time_prekeys"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    prekey = Column(LargeBinary)


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String)
    recipient = Column(String)
    ciphertext = Column(LargeBinary)
    nonce = Column(LargeBinary)