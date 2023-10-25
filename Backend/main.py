from fastapi import FastAPI
import uvicorn
from Auth.auth_api import router as auth_api
from Admin.role_api import router as role_api
from Pathways.pathways_api import router as pathways_api

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(auth_api, prefix="/Auth")
app.include_router(role_api, prefix="/Admin")
app.include_router(pathways_api, prefix="/Pathway")

origins = [
    "http://localhost:5173",  # Add the URL of your frontend application
    "http://localhost:8000",  # You might want to include the FastAPI server's own origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)