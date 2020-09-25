""" Router for Registration end point """
from fastapi import APIRouter
from application.modules.registration import (
    NewCustomerData, NewCustomerReturnData,
    AccountActivationData, AccountActivationTokenData
)
from application.modules.registration.new_customer import NewCustomers

reg_router = APIRouter()


@reg_router.get("/", response_model=NewCustomerReturnData)
def registration_root() -> object:
    """Warn the user nothing is here"""
    return NewCustomerReturnData(
        status=False,
        msg="Please specify correct endpoint."
    )


# Register a new customer
@reg_router.post("/new_customer", response_model=NewCustomerReturnData)
def register_new_customer(data: NewCustomerData) -> object:
    """Register a new customer into the system"""
    NewCustomer = NewCustomers()
    response = NewCustomer.register(data)
    return NewCustomerReturnData(
        status=response['status'],
        msg=response['msg'],
        data=response['data'] if response.get('data') else {}
    )


# Activate a new customer account
@reg_router.post("/activate", response_model=NewCustomerReturnData)
def account_activate(data: AccountActivationData) -> object:
    """Activate a new customer account"""
    NewCustomer = NewCustomers()
    response = NewCustomer.finalize_register(data)
    return NewCustomerReturnData(
        status=response['status'],
        msg=response['msg'],
        data=response['data'] if response.get('data') else {}
    )


# Check the registration status
@reg_router.get("/registration_status/{validation_token}", response_model=NewCustomerReturnData)
def registration_status(validation_token: str) -> object:
    """Check the registration status"""
    NewCustomer = NewCustomers()
    response = NewCustomer.registration_status(
        AccountActivationTokenData(validation_token=validation_token))
    return NewCustomerReturnData(
        status=response['status'],
        msg=response['msg'],
        data=response['data'] if response.get('data') else {}
    )
