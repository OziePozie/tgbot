from sqlalchemy import Integer, String, Boolean, Column, Enum
from sqlalchemy.orm import declarative_base
from enum import Enum as BaseEnum


Base = declarative_base()


class Object(Base):
    __tablename__ = 'objects'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    tg_link = Column(String)


class Auto(Base):
    __tablename__ = 'auto'

    id = Column(Integer, primary_key=True)
    isOOO = Column(Boolean)
    isHeavy = Column(Boolean)
    tg_link = Column(String)


class WorkType(BaseEnum):
    Master = "master"
    Electrician = "electrician"
    Tester = "tester"
    AUR = "aur"

    @classmethod
    def get_by_value(cls, value):
        for enum_item in cls:
            if enum_item.value == value:
                return enum_item
        raise ValueError(f"'{value}' is not among the defined enum values.")


class Workers(Base):
    __tablename__ = 'workers'

    id = Column(Integer, primary_key=True)
    work_type = Column(Enum(WorkType))
    name = Column(String)
