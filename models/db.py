from peewee import *

# データベース接続の定義
db = SqliteDatabase('my_database.db')

class BaseModel(Model):
    """A base model that will use our Sqlite database."""
    class Meta:
        database = db

class User_tb(Model):
    user_id = IntegerField()
    username = CharField()
    age = IntegerField()
   
class Task_tb(Model):
    user_id = IntegerField()
    task_name = CharField()
    task_content = CharField()

class Physical_tb(Model):
    user_id = IntegerField()
    temp = DoubleField()
    bad_good = BooleanField(default=True)
    bad_content = CharField()

# データベース接続とテーブル作成
db.connect()
db.create_tables([User_tb])
db.create_tables([Task_tb])
db.create_tables([Physical_tb])

db.close()