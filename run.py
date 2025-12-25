from dotenv import load_dotenv
from app import App

#Load the environment variables
load_dotenv()

#Create the app object and run the app
if __name__=="__main__":
    app=App()
    app.run()