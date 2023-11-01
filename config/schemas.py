from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    email: str
    password: str


class CURRENCY(str, Enum):
    USD = 'usd'
    AUD = 'aud'
    RUB = 'rub'
    SAR = 'sar'

class PaymentFormSchema(BaseModel):
    form_name: str
    description: str
    amount: int
    currency: CURRENCY
    user_id: int

    class Config:
       use_enum_values = True


class PaymentLogSchema(BaseModel):
    user_id: int
    form_id: int
    date: datetime = datetime.now
    is_succeded: bool
    amount: int


class MailSchema(BaseModel):
    to: List[str]
    subject: str
    body: str
