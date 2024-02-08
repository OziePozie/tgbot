import datetime
from sqlalchemy import Integer, String, Boolean, Column, Enum, Date, ForeignKey, Float, DateTime, func
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum as BaseEnum


Base = declarative_base()


class Object(Base):
    __tablename__ = 'objects'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    tg_link = Column(String)
    total_travelers = Column(Float, default=0)
    total_fuel = Column(Float, default=0)
    total_living = Column(Float, default=0)
    total_other_expenses = Column(Float, default=0)
    total_autocran = Column(Float, default=0)
    total_hours = Column(Float, default=0)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())


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
    __tablename__ = "travel_order"

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
    master_id = Column(String)
    object_name = Column(String)
    auto = Column(String)
    city = Column(String)
    km = Column(Float)
    date_from = Column(String)
    probeg_vyezd = Column(Integer, default=0)
    probeg_prized = Column(Integer, default=0)
    priezd = Column(Boolean, default=False)
    next_message = Column(String)


class PerformanceReport(Base):
    __tablename__ = 'performance_report'

    id = Column(Integer, primary_key=True)
    object_name = Column(String)
    date = Column(String)
    text = Column(String)
    photo_video = Column(String)

