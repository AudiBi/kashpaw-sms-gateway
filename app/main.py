from fastapi import FastAPI

from app.api.sms import router

from app.config import Config


app = FastAPI(

    title="KashPaw SMS Gateway",

    version="1.0.0"

)

app.include_router(

    router,

    prefix="/api",

    tags=["SMS"]

)


@app.get("/")

def home():

    return {

        "application": Config.APP_NAME,

        "version": "1.0.0",

        "status": "running"

    }