""" Secure Router example end points """
from fastapi import APIRouter
from application.modules.registration import (NewCustomerReturnData)

secure_router = APIRouter()


@secure_router.get("/", response_model=NewCustomerReturnData)
def secure_root() -> object:
    """Warn the user nothing is here"""
    return NewCustomerReturnData(
        status=False,
        msg="Please specify correct endpoint."
    )


# Register a new customer
@secure_router.get("/list", response_model=NewCustomerReturnData)
def list_somethin_secure() -> object:
    """Example for secure access"""
    return NewCustomerReturnData(
        status=True,
        msg="If succesfull loggedin you can see this",
        data={"your_sucure_list": ["apple", "pineapple", "something"]}
    )
