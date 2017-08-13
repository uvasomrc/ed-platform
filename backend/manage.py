import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from ed_platform import app, db
from ed_manage import data

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('load_data', data.LoadData(db,"example_data.json"))
manager.add_command('clear_data', data.ClearData(db))

if __name__ == '__main__':
    manager.run()