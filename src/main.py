from src.facturapp.gui.app import launch_app
from src.facturapp.utils.database import init_db

if __name__ == "__main__":
    init_db()
    launch_app()
