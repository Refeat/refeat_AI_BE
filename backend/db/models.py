from sqlalchemy import BINARY, BigInteger, Column, Enum, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.dialects.mysql import BIT, DATETIME
from sqlalchemy.orm import relationship
from .database import Base
import datetime

metadata = Base.metadata


class EmailVerification(Base):
    __tablename__ = 'email_verification'

    id = Column(BigInteger, primary_key=True)
    code = Column(Integer)
    email = Column(String(255))
    is_verified = Column(BIT(1))
    valid_until = Column(DATETIME(fsp=6))


class UserInfo(Base):
    __tablename__ = 'user_info'

    id = Column(BigInteger, primary_key=True)
    email = Column(String(255))
    nickname = Column(String(255))
    password = Column(String(255))
    profile_image = Column(String(255))
    provider = Column(Enum('GOOGLE', 'NATIVE', 'APPLE', 'KAKAO', 'NAVER'))
    nickname = Column(String(255))


class Project(Base):
    __tablename__ = 'project'

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DATETIME(fsp=6))
    description = Column(String(255))
    name = Column(String(255))
    thumbnail = Column(String(255))
    updated_at = Column(DATETIME(fsp=6))
    user = Column(ForeignKey('user_info.id'), index=True)

    user_info = relationship('UserInfo')


class Chat(Base):
    __tablename__ = 'chat'

    id = Column(BigInteger, primary_key=True)
    content = Column(String(2048))
    content_refined = Column(String(2048))
    name = Column(String(255))
    project = Column(ForeignKey('project.id'), index=True)
    user = Column(ForeignKey('user_info.id'), index=True)
    mention = Column(String(255))
    position = Column(String(255))
    reference = Column(String(255))
    created_at = Column(DATETIME(fsp=6))
    chunk_text = Column(Text())

    project1 = relationship('Project')
    user_info = relationship('UserInfo')
    
class Reference(Base):
    __tablename__ = 'reference'

    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    document_id = Column(BINARY(16))
    chunk = Column(Text())
    chat = Column(ForeignKey('chat.id'), index=True)


class Document(Base):
    __tablename__ = 'document'

    id = Column(BINARY(16), primary_key=True)
    created_at = Column(DATETIME(fsp=6))
    favicon = Column(String(255))
    link = Column(String(255))
    name = Column(String(255))
    summary = Column(String(1000))
    type = Column(Enum('WEB', 'PDF'))
    project = Column(ForeignKey('project.id'), index=True)
    save_done = Column(Integer)
    summary_done = Column(Integer)
    embedding_done = Column(Integer)

    project1 = relationship('Project')