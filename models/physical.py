from peewee import ForeignKeyField, DecimalField, BooleanField, CharField, Model
from .db import db
from .user import User
from .task import Task

class Physical(Model):
    user = ForeignKeyField(User, backref='physicals')
    temp = DecimalField()  # 固定小数点
    task = ForeignKeyField(Task, backref='physicals')
    bad_good = BooleanField(default=True)
    bad_content = CharField()
    class Meta:
        database = db
