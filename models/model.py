from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, Float, Date, String, Text, DateTime
from sqlalchemy import ForeignKey 
import datetime


class Base(DeclarativeBase):
    pass


class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    token = Column(String)
    endpoint = Column(String)   
    location = Column(String)
    measurement_interval = Column(Integer)
    send_interval = Column(Integer)    
    measurements = relationship("Measurement", back_populates="device")


class Measurement(Base):
    __tablename__ = 'measurement'
    id = Column(Integer, primary_key=True)
    value = Column(Float)
    p1 = Column(Float)
    p2 = Column(Float)
    p3 = Column(Float)
    p4 = Column(Float)
    p5 = Column(Float)
    p6 = Column(Float)
    p7 = Column(Float)
    p8 = Column(Float)
    p9 = Column(Float)
    p10 = Column(Float)
    p11 = Column(Float)
    p12 = Column(Float)
    p13 = Column(Float)
    p14 = Column(Float)
    p15 = Column(Float)
    p16 = Column(Float)
    counter1 = Column(Integer)
    counter2 = Column(Integer)
    date = Column(Date)
    device_id = Column(Integer, ForeignKey('devices.id'))
    device = relationship("Device", back_populates="measurements")

# class LogRecord(Base):
#     __tablename__ = 'logs'
#     id = Column(Integer, primary_key=True)
#     timestamp = Column(DateTime, default=datetime.datetime.utcnow)
#     name = Column(String)
#     level = Column(String)
#     message = Column(Text)