import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from ed_platform import app, db
from ed_manage import data

app.config.from_envvar('APP_CONFIG_FILE')
# Load the configuration from the instance folder
app.config.from_pyfile('config.py')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('load_data', data.LoadData(db,"example_data.json"))
manager.add_command('clear_data', data.ClearData(db))

if __name__ == '__main__':
    manager.run()