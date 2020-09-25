import os
import uuid
import boto3
from application.modules.registration import (
    NewCustomerData, AccountActivationTokenData, AccountActivationData
)
from application.modules.user import UserEmailModel
from application.utils.helpers import Helper
from application.modules.user.user import User


class NewCustomers(object):

    def __init__(self):
        super().__init__()
        self.cognito = boto3.client('cognito-idp', region_name=os.getenv("AWS_REGION"))

    def register(self, data: NewCustomerData):
        """ Register a new customer"""

        # TODO: check if mail address already exist in YOUR database
        # if UserCheck:
        #   Return False

        # TODO: First add new user / customer data to YOUR database
        new_user_id = str(uuid.uuid4())
        new_customer_id = str(uuid.uuid4())
        validation_token = Helper.GenerateString(20, True)

        # Send confirmation mail to user
        mailbody = f"""Dear {data.customer_name},\r\r
            Your account has been created. To activate your new account click the below link and follow the instructions:\r
            {os.getenv("APP_URL")}/activation/{validation_token}\r\r
            {os.getenv("PROJECT_NAME")} {os.getenv("APP_URL")}"""
        # TODO: SendMail - Using SES

        return {
            "status": True,
            "msg": f"Your account has been created. Please check your e-mail for instructions.",
            "data": {
                "user_id": new_user_id,
                "customer_id": new_customer_id,
            }
        }

    def registration_status(self, data: AccountActivationTokenData) -> object:
        """ Check the status of the customer registration

        Args:
            data (AccountActivationTokenData): [description]
        """
        # TODO: getting the registration status from your database
        # Check the validation_token and user status.
        validation_status = True
        if validation_status:
            return {
                "status": True,
                "msg": "Something about status",
                "data": {
                    "user_email": "usermail.user_email"
                }
            }
        else:
            return {
                "status": False,
                "msg": "User account not found or account already active.",
            }


    def finalize_register(self, data: AccountActivationData) -> object:
        """ Complete the user / customer registration"""
        # Get and check data from token (still pending in DB)
        registration_response = self.registration_status(AccountActivationTokenData(validation_token=data.validation_token))
        if not registration_response['status'] and registration_response['msg'] != 'PENDING':
            return registration_response

        tmp_password = Helper.GenerateString(20, True)

        # Create Cognito account with a temp password
        try:
            response = self.cognito.admin_create_user(
                UserPoolId=os.getenv("COGNITO_POOL_ID"),
                Username=data.user_email,
                UserAttributes=[
                    {"Name": "email", "Value": data.user_email},
                    {"Name": "email_verified", "Value": "true"}
                ],
                TemporaryPassword=tmp_password,         # Set the password, so user needs to recieve this by mail
                MessageAction="SUPPRESS",               # AWS Cognito will not send any email.
                DesiredDeliveryMediums=['EMAIL']
            )
        except self.cognito.exceptions.UsernameExistsException as e:
            return {
                "status": False,
                "msg": "A user with this e-mail address already exists",
                "data": {"cognito": "UsernameExistsException"}
            }
        except Exception as e:
            return {
                "status": False,
                "msg": str(e),
                "data": None
            }

        # add the cognito details to YOUR database and do other stuff
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            try:

                #TODO: do cool stuff here needed for your application
                pass

            except Exception as e:
                return {
                    "status": False,
                    "msg": str(e),
                    "data": None
                }

            # Now reset the password for the created cognito account with the given user password
            password_reset = User()
            response_password_reset = password_reset.admin_set_user_password(data.user_email, data.new_password, True)

            # If success, do something
            if response_password_reset['ResponseMetadata']['HTTPStatusCode'] == 200:

                # send mail to user about account activation
                mailbody = f"""Dear user,\r\r
                    Your account has been activated and ready to use. You have setup a password to secure your account, please keep your password in a save place.\r
                    You can access anytime your account. Start here: {os.getenv("APP_URL")}/login and enter your email address and password.\r\r

                    {os.getenv("APP_URL")}"""
                # send mail

            return {
                "status": True,
                "msg": "Your account has been activated, please login using your new password!"
            }
