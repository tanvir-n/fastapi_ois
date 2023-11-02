from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str

    
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

    class Config:
       use_enum_values = True


class PaymentLogSchema(BaseModel):
    user_id: int
    form_id: int
    date: datetime
    is_succeded: bool
    amount: int


class MailSchema(BaseModel):
    to: List[str]
    subject: str
    body: str
