import os
from fastapi import FastAPI
from application.constants import api_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# below origins needed to enable CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app = FastAPI(title=os.getenv("PROJECT_NAME"),
              openapi_url="/api/v1/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
@app.get("/", tags=["Default root endpoint"])
def read_root() -> object:
    """ Default endpoint"""
    json_response = {}
    json_response['status'] = False
    json_response['msg'] = 'UNAUTHORIZED ACCESS TO THIS WEBSITE IS PROHIBITED, You must have explicit, authorized permission to access this webapi. Unauthorized attempts and actions to access or use this system may result in civil and/or criminal penalties. All activities performed on this server are logged and monitored.'
    return json_response


app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
