from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from v1.constants import API_VERSION
from v1.router import v1__router


app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://www.footwedge.io",
    "https://www.footwedge.io/",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(v1__router, prefix=f"/{API_VERSION}", tags=[API_VERSION])
