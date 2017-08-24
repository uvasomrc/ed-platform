import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from ed_platform import app, db
from ed_manage import data_manager


# Load the configuration
app.config.from_object('config.default')
app.config.from_pyfile('config.py')
if "APP_CONFIG_FILE" in os.environ:
    app.config.from_envvar('APP_CONFIG_FILE')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('load_data', data_manager.LoadData(db, "example_data.json"))
manager.add_command('clear_data', data_manager.ClearData(db))

if __name__ == '__main__':
    manager.run()