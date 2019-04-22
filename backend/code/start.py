from apeback import app
from apeback.consumer import controller

if __name__ == "__main__":
    app.start_consumer(controller)
