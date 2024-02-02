from sqlalchemy import Integer, String, Boolean, Column, Enum
from sqlalchemy.orm import declarative_base, sessionmaker
from enum import Enum as BaseEnum
Base = declarative_base()


class Object(Base):
    __tablename__ = 'objects'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Auto(Base):
    __tablename__ = 'auto'

    id = Column(Integer, primary_key=True)
    isOOO = Column(Boolean)
    isHeavy = Column(Boolean)


class WorkType(BaseEnum):
    Master = "Мастер"
    Electrician = "Электромонтер"
    Tester = "Испытатель"
    AUR = "Аур(ИТР)"


class Workers(Base):
    __tablename__ = 'workers'

    id = Column(Integer, primary_key=True)
    work_type = Column(Enum(WorkType))
    name = Column(String)
    lastname = Column(String)
    surname = Column(String)
