import os
from flask_script import Manager
from flask_migrate import MigrateCommand
from app import create_app

# 获取应用实例
app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
# 创建manger，可以通过shell操作app
manager = Manager(app)
# 添加shell命令
# python manage.py db init/migrate/upgrade/downgrade
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
