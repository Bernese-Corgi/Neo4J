from typing import Union

from fastapi import FastAPI


def start_server():
    app = FastAPI()

    return app

app = start_server()