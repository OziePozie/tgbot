import datetime
from sqlalchemy import Integer, String, Boolean, Column, Enum, Date, ForeignKey, DECIMAL
from sqlalchemy.orm import declarative_base, relationship
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
    name = Column(String)
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


class Travel_orders(Base):
    __tablename__ = "traver_order"

    id = Column(Integer, primary_key=True)
    fio = Column(String)
    object_name = Column(String)
    date_from = Column(String)
    date_to = Column(String)
    from_report = Column(Integer)
    is_order = Column(Boolean)


class Chats(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    chat_description = Column(String)
    chat_link = Column(String)


class Transports(Base):
    __tablename__ = "transports"

    id = Column(Integer, primary_key=True)
    master = Column(String)
    master_id = Column(Integer)
    object_name = Column(String)
    ooo_or_ip = Column(String)
    auto = Column(String)
    city = Column(String)
    km = Column(DECIMAL)
    date_from = Column(String)

