import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from config.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    email = Column(String(50))
    password = Column(String(255))

    payment_form = relationship('PaymentForm', back_populates='user')
    payment_log = relationship('PaymentLog', back_populates='user')


class PaymentForm(Base):
    __tablename__ = 'payment_forms'

    id = Column(Integer, primary_key=True, index=True)
    form_name = Column(String(100))
    description = Column(String(300)) 
    amount = Column(Integer)
    currency = Column(String(3))
    user_id = Column(Integer, ForeignKey('users.id'))
    form_url = Column(String(100))

    user = relationship('User', back_populates='payment_form')
    payment_log = relationship('PaymentLog', back_populates='payment_form')


class PaymentLog(Base):
    __tablename__ = 'payment_logs'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    form_id = Column(Integer, ForeignKey('payment_forms.id'))
    date = Column(DateTime, default=datetime.datetime.now)
    is_succeded = Column(Boolean, default=True)
    amount = Column(Integer)

    payment_form = relationship('PaymentForm', back_populates='payment_log')
    user = relationship('User', back_populates='payment_log')
