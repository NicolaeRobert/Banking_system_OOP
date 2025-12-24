from dotenv import load_dotenv
from main import App

load_dotenv()


if __name__=="__main__":
    app=App()
    app.run()