from gui.app import launch_app
from models.database import init_db

if __name__ == "__main__":
    init_db()
    launch_app()
