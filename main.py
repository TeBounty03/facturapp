from gui.app import launch_app
from models.database import init_db
import gettext
import os

# Translation configuration
locales_dir = os.path.join(os.path.dirname(__file__), 'locales')
fr_translation = gettext.translation('fr', locales_dir, languages=['fr'])
fr_translation.install()

if __name__ == "__main__":
    init_db()
    launch_app()
