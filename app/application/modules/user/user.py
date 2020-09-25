import os
import boto3
import datetime
from application.modules.user import (
    UserLoginDataModel, UserEmailModel, UserChangePasswordModel,
    CognitoUserNameModel)
from application.utils.helpers import Helper
from application.auth.auth_models import JWTAuthorizationCredentials


class User(object):

    def __init__(self):
        super().__init__()
        self.cognito = boto3.client(
            'cognito-idp', region_name=os.getenv("AWS_REGION"))

    def login(self, data: UserLoginDataModel, request) -> object:
        """ Used for validate the user"""
        secret_hash = Helper.get_secret_hash(data.user_email, os.getenv(
            "COGNITO_CLIENT_ID"), os.getenv("COGNITO_CLIENT_SECRET"))

        try:
            response = self.cognito.admin_initiate_auth(
                UserPoolId=os.getenv("COGNITO_POOL_ID"),
                ClientId=os.getenv("COGNITO_CLIENT_ID"),
                AuthFlow='ADMIN_NO_SRP_AUTH',
                AuthParameters={
                    'USERNAME': data.user_email,
                    'SECRET_HASH': secret_hash,
                    'PASSWORD': data.user_password
                }
            )

        except self.cognito.exceptions.NotAuthorizedException as e:
            print(f"Error on login: {e}")
            # return {"status": False, "msg": "The username or password is incorrect"}
            error = e.__str__()

            if error.find("Temporary password has expired and must be reset by an administrator.") > 0:
                return {
                    "status": False,
                    "msg": "Temporary password has expired and must be reset by an administrator."
                }

            if error.find("Incorrect username or password") > 0:
                return {
                    "status": False,
                    "msg": "Incorrect username or password. Please try again or request a new password."
                }
            else:
                return {
                    "status": False,
                    "msg": f"Unknown error while login: {e.__str__()}"
                }

        except self.cognito.exceptions.UserNotConfirmedException:
            return {"status": False, "msg": "User is not confirmed"}
        except self.cognito.exceptions.UserNotFoundException:
            return {"status": False, "msg": "The username or password is incorrect"}
        except Exception as e:
            return {"status": False, "msg": e.__str__()}

        if response.get("AuthenticationResult"):
            remote_addr = f"{request.headers.get('forwarded')} === {request.headers.get('X-Forwarded-For')}"
            user_agent = request.headers['user-agent']

            # Send mail notification for succes login
            mailbody = f"""
                Dear user,\r\r
                This is to notify you of a successful login attempt to your account.\r
                Login Time: {datetime.datetime.now()}\r
                IP Address: {remote_addr}\r
                User agent: {user_agent}\r\r
                {os.getenv("APP_URL")}"""
            # TODO: send mail

            return {
                'msg': "You are successfully logged in",
                "status": True,
                "data": {
                    "id_token": response["AuthenticationResult"]["IdToken"],
                    "refresh_token": response["AuthenticationResult"]["RefreshToken"],
                    "access_token": response["AuthenticationResult"]["AccessToken"],
                    "expires_in": response["AuthenticationResult"]["ExpiresIn"],
                    "token_type": response["AuthenticationResult"]["TokenType"]
                }
            }

        if response.get("ChallengeName") and response["ChallengeName"] == 'NEW_PASSWORD_REQUIRED':
            return {
                "status": False,
                "msg": "Please change your password",
                "data": {
                    "ChallengeName": "NEW_PASSWORD_REQUIRED",
                    "Session": response['Session'],
                    "USER_ID_FOR_SRP": response["ChallengeParameters"]['USER_ID_FOR_SRP']
                }
            }

    def change_password(self, data: UserChangePasswordModel) -> object:
        """ If password change is required ChallengeName has been set.

        Args:
            data (UserChangePasswordModel): [description]
        """

        if data.data is not None and data.data.ChallengeName == 'NEW_PASSWORD_REQUIRED':
            response = self.__admin_respond_to_auth_challenge(data)
        else:
            response = self.__change_password(data)

        if response.get("AuthenticationResult"):
            return {
                'msg': "Your password has been changed!",
                "status": True,
                "data": {
                    "id_token": response["AuthenticationResult"]["IdToken"],
                    "refresh_token": response["AuthenticationResult"]["RefreshToken"],
                    "access_token": response["AuthenticationResult"]["AccessToken"],
                    "expires_in": response["AuthenticationResult"]["ExpiresIn"],
                    "token_type": response["AuthenticationResult"]["TokenType"]
                }
            }

        return response

    def forgot_password(self, data: UserEmailModel) -> object:
        """
        If a user needs to request a new password.
        This function send a new temporarly password by email (not the Cognito token).

        Args:
            data (UserEmail): [description]
        """
        tmp_password = Helper.GenerateString(10, True)
        try:
            response = self.admin_set_user_password(
                data.user_email, tmp_password)

            # Send e-mail with password reset instructions
            mailbody = f"""
                Dear user,\r\r
                You have request a password reset. Below is a new password for you.
                This is a temporarly password and need to change right after you have been logged in.\r
                Temporarly password: {tmp_password}\r\r
                {os.getenv("APP_URL")}"""

            # TODO: sendmail

        except Exception as e:
            return {
                "status": False,
                "msg": f"Error in forgot_password {e.__str__()} "
            }

        return {
            "status": True,
            "msg": "Please check your e-mail for instructions"
        }

    def user_status(self, credentials: JWTAuthorizationCredentials) -> object:
        """This function returned the user authentication status

        Args:
            credentials (JWTAuthorizationCredentials): [description]
        """

        return {
            "status": True,
            "msg": "",
            "data": {
                "username": credentials.claims['username'],
                "client_id": credentials.claims['client_id'],
                "jwt_token": credentials.jwt_token,
                "authenticated": True,
            }
        }

    def user_exists(self, data: UserEmailModel) -> object:
        """This function returned True if email address already exists

        Args:
            data (UserEmail): [User email address]

        Returns:
            object: [True if exists, Fals if not exists]
        """
        # TODO: create function to check if user / email is aldready in database
        user_exists = False

        try:
            if user_exists:
                return {
                    "status": True,
                    "msg": "Mail address already exists. Use the request password function.",
                    "data": {"email_exists": True}
                }
            else:
                return {
                    "status": True,
                    "msg": "Mail address does not exists.",
                    "data": {"email_exists": False}
                }

        except Exception as e:
            return {
                "status": False,
                "msg": f"Error in user_exists: {e.__str__()}"
            }

    def user_sign_out(self, data: CognitoUserNameModel) -> object:
        """ Destroy the user tokens and sessions

        Args:
            data (CognitoUserNameModel): [description]
        """
        try:
            response = self.cognito.admin_user_global_sign_out(
                UserPoolId=os.getenv("COGNITO_POOL_ID"),
                Username=data.username
            )

        except Exception as e:
            return {
                "status": False,
                "msg": f"Unknown error in user_sign_out {e.__str__()}"
            }

        return {
            "status": True,
            "msg": f"User session has been terminated",
        }

    def admin_set_user_password(self, p_UserName: str, p_TempPassword: str, p_Permanent=False) -> object:
        """ Admin function to set a new password for a user on cognito

        Args:
            p_UserName (str): [description]
            p_TempPassword (str): [description]
            p_Permanent (bool, optional): [description]. Defaults to False.
        """
        try:
            response = self.cognito.admin_set_user_password(
                UserPoolId=os.getenv("COGNITO_POOL_ID"),
                Username=p_UserName,
                Password=p_TempPassword,
                Permanent=p_Permanent         # False: User will forced to change passwor
            )
        except Exception as e:
            return {
                "status": False,
                "msg": f"Unknown error in admin_set_user_password {e.__str__()}"
            }

        return response

    def __admin_respond_to_auth_challenge(self, data: UserChangePasswordModel) -> object:
        """Private function for using if Changenge responses other the authenticated

        Args:
            data (UserChangePassword): [description]
        """
        try:
            response = self.cognito.admin_respond_to_auth_challenge(
                UserPoolId=os.getenv("COGNITO_POOL_ID"),
                ClientId=os.getenv("COGNITO_CLIENT_ID"),
                # ChallengeName='SMS_MFA'|'SOFTWARE_TOKEN_MFA'|'SELECT_MFA_TYPE'|'MFA_SETUP'|'PASSWORD_VERIFIER'|'CUSTOM_CHALLENGE'|'DEVICE_SRP_AUTH'|'DEVICE_PASSWORD_VERIFIER'|'ADMIN_NO_SRP_AUTH'|'NEW_PASSWORD_REQUIRED',
                ChallengeName=data.data.ChallengeName,
                ChallengeResponses={
                    'NEW_PASSWORD': data.new_password,
                    'USERNAME': data.data.USER_ID_FOR_SRP,  # data.USER_ID_FOR_SRP,
                    "SECRET_HASH": Helper.get_secret_hash(data.data.USER_ID_FOR_SRP, os.getenv("COGNITO_CLIENT_ID"), os.getenv("COGNITO_CLIENT_SECRET"))
                },
                Session=data.data.Session,
            )
        except self.cognito.exceptions.NotAuthorizedException as e:
            return {
                "status": False,
                "msg": "Your session has expired."
            }
        except Exception as e:
            return {
                "status": False,
                "msg": f"Unknown error in __admin_respond_to_auth_challenge {e.__str__()}"
            }

        return response

    def __change_password(self, p_CurrentPassword, p_NewPassword, p_SessionToken) -> object:
        """Change the password for the current user.

        Args:
            p_CurrentPassword ([type]): [description]
            p_NewPassword ([type]): [description]
            p_SessionToken ([type]): [description]

        Returns:
            object: [description]
        """
        response = self.cognito.change_password(
            PreviousPassword=p_CurrentPassword,
            ProposedPassword=p_NewPassword,
            AccessToken=p_SessionToken
        )
        return response
