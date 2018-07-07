import os
os.environ['BASE_PATH'] = os.path.abspath(os.path.dirname(__file__))

from app import app


if __name__ == "__main__":
    app.run()
