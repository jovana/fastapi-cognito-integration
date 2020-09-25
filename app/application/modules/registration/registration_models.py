from pydantic import BaseModel, EmailStr
from typing import Optional

class NewCustomerData(BaseModel):
    customer_name: str
    company_name: str
    customer_email: EmailStr


class AccountActivationData(BaseModel):
    validation_token: str
    new_password: str
    confirm_new_password: str
    user_email: EmailStr


class AccountActivationTokenData(BaseModel):
    validation_token: str


class NewCustomerReturnData(BaseModel):
    status: bool
    msg: str
    data: Optional[dict] = {}

    # Below class is used in the example section on the docs.
    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "msg": "A message for you",
                "data": {
                }
            }
        }
