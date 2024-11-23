"""
This file is the start file for Fast Api
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user_authentication, user_profile


app = FastAPI(
    title="Diet Plan And Management",
    version="1.0",
    description="Manages Diet Plans in a seamless manner.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(user_authentication.router, prefix="/auth",
                   tags=["Authentication"])
app.include_router(user_profile.router, prefix="/userSetUp",
                   tags=["UserManagement"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
