import os
import requests
from application.auth.auth_models import JWKS

jwks = JWKS.parse_obj(
    requests.get(
        f"{os.getenv('COGNITO_URL')}"
        f"{os.getenv('COGNITO_POOL_ID')}/.well-known/jwks.json"
    ).json()
)
