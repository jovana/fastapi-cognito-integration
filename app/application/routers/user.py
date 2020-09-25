""" Router for User end point """
from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel

from application.constants import auth
from application.modules.user import (
    UserEmailModel, UserLoginDataModel, UserReturnDataModel,
    UserChangePasswordModel, CognitoUserNameModel)
from application.modules.user.user import User
from application.auth.auth_models import JWTAuthorizationCredentials
import random

user_router = APIRouter()


@user_router.get("/", response_model=UserReturnDataModel)
async def user_endpoint() -> object:
    """Set warning for the default endpoint"""
    return UserReturnDataModel(
        status=False,
        msg="Please specify correct endpoint."
    )


# @user_router.get("/test", response_model=UserReturnData)
# async def user_test_endpoint() -> object:
#     # from application.modules.registration.new_customer import NewCustomers
#     from application.utils.db.models import (
#         UsersDatabaseModel, CustomersDatabaseModel
#     )

#     # customer_data = CustomersDatabaseModel.get("21c4b343-b607-4897-a9cc-04d67474ffc0")
#     # print(f"customer_data: {customer_data.customer_id}")
#     # UsersDatabaseModel.UserEmailIndex.query(registration_response['data']['user_email']).__next__()
#     import string
#     password = random.choice(string.punctuation)
#     print(f"password: {Helper.GenerateString(8,True)}")


@user_router.post("/login", response_model=UserReturnDataModel)
async def user_login(data: UserLoginDataModel, request: Request) -> object:
    """User login. Create user session"""
    # print(f"request.headers: {request.headers}")

    UserLogin = User()
    response = UserLogin.login(data, request)

    return UserReturnDataModel(
        status=response['status'],
        msg=response['msg'],
        data=response['data'] if response.get('data') else {}
    )


@user_router.post("/user_exists", response_model=UserReturnDataModel)
async def user_exists(data: UserEmailModel, response: Response) -> object:
    """ Check if email address already exists in the database
    """

    UserMail = User()
    response = UserMail.user_exists(data)
    return response


@user_router.post("/request_password", response_model=UserReturnDataModel)
async def request_user_password(data: UserEmailModel) -> object:
    """ If a user needs to request a new password.
        This function send a new temporarly password by e-mail.
    """
    UserLogin = User()
    response = UserLogin.forgot_password(data)

    return UserReturnDataModel(
        status=response['status'],
        msg=response['msg'],
    )


@user_router.put("/changepassword", response_model=UserReturnDataModel)
async def update_user_password(data: UserChangePasswordModel) -> object:
    """Change user password.
    Also use this for the first time a user login and need to force change his password
    """
    print(f"changepassword data: {data}")

    UserLogin = User()
    response = UserLogin.change_password(data)
    return UserReturnDataModel(
        status=response['status'],
        msg=response['msg'],
        data=response['data'] if response.get('data') else {}
    )

# Protected endpoints below this line
# ######################################


@user_router.get("/status", dependencies=[Depends(auth)], response_model=UserReturnDataModel)
async def read_user_status(credentials: JWTAuthorizationCredentials = Depends(auth)) -> object:
    """This returns the user status"""
    UserLogin = User()
    # print(f"credentials: {credentials}")
    response = UserLogin.user_status(credentials)
    return UserReturnDataModel(
        status=response['status'],
        msg=response['msg'],
        data=response['data'] if response.get('data') else {}
    )


@user_router.post("/sign_out", response_model=UserReturnDataModel)
async def logoff_user(data: CognitoUserNameModel) -> object:
    UserClass = User()
    response = UserClass.user_sign_out(data)

    return UserReturnDataModel(
        status=response['status'],
        msg=response['msg']
    )
