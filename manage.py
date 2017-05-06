from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db

app = create_app('development')
manager = Manager(app)
migrate = Migrate(app, db)

'''add command python manage.py shell'''
def make_shell_context():
    return dict(app=app)

manager.add_command('shell', Shell(make_context=make_shell_context))

'''add command python manage.py db ..'''
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
