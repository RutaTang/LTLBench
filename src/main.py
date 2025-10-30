from src.cli import app
from dotenv import find_dotenv, load_dotenv

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    app()
