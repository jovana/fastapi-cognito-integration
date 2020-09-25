from fastapi import APIRouter, Depends
from dotenv import load_dotenv

# TODO: fix Circular Dependency on routers
load_dotenv()

# JWT Authentication
from application.auth.jwks import jwks
from application.auth.JWTBearer import JWTBearer

auth = JWTBearer(jwks)

from application.routers import registration, user, secure
api_router = APIRouter()

# Below router have no protection, is some case protetion is manage on the function it self
api_router.include_router(registration.reg_router, prefix="/registration", tags=["Registration endpoint"])
api_router.include_router(user.user_router, prefix="/user", tags=["User endpoint (Partially protected)"])

# Below is an example of protecting the whole end point.
api_router.include_router(secure.secure_router, prefix="/secure", dependencies=[Depends(auth)], tags=["Secure endpoint (Protected)"])
