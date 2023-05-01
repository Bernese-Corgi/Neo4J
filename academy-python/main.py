import dotenv

from fastapi import FastAPI


def start_server():
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    
    app = FastAPI()

    return app

app = start_server()