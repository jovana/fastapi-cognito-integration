from pydantic import BaseModel, EmailStr
from typing import Optional


class CognitoUserNameModel(BaseModel):
    username: str
    access_token: Optional[str]


class UserLoginDataModel(BaseModel):
    user_email: EmailStr
    user_password: str


class UserEmailModel(BaseModel):
    user_email: EmailStr


class UserReturnDataModel(BaseModel):
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


class UserRequiredChangePasswordModel(BaseModel):
    """ This items comes direct from Cognito if password change is required

    Args:
        BaseModel ([type]): [description]
    """
    Session: str
    USER_ID_FOR_SRP: str
    ChallengeName: str


class UserChangePasswordModel(BaseModel):
    current_password: str
    new_password: str
    confirm_new_password: str
    data: Optional[UserRequiredChangePasswordModel] = None
