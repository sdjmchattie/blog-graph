from dotenv import load_dotenv

load_dotenv()

from graph import app

if __name__ == "__main__":
    print("Welcome to BlogGraph!")
    print(app.invoke(input={}))
