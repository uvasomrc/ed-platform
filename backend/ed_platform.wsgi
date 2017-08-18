import os
import sys

os.environ['APP_CONFIG_FILE']='/var/www/edpg/backend/config/development.py'
from ed_platform import app as application
