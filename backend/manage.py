import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from ed_platform import app, db, elastic_index
from ed_manage import data_manager
from ed_manage.email_manager import manager as email_manager


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
manager.add_command('index_data', data_manager.IndexData(db, elastic_index))
#manager.add_command('send_confirmation', email_manager.Confirmation(app))

manager.add_command("email", email_manager)

if __name__ == '__main__':
    manager.run()