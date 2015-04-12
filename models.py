from peewee import *
import datetime

db = SqliteDatabase('database.db', threadlocals=True)

class Result(Model):
  STATUS_LABELS = (
        ('Success', 'success'),
        ('Info', 'info'),
        ('Error', 'error'),
        ('Warning', 'warning'),
    )
  name = CharField()
  value = CharField()
  time = DateTimeField(default=datetime.datetime.now)
  label = CharField(choices=STATUS_LABELS)

  class Meta:
    database = db

class Object(Model):
  distance = FloatField()
  width = FloatField()
  x = FloatField()
  y = FloatField

  class Meta:
    database = db

class Robot(Model):
  x = IntegerField()
  y = IntegerField

  class Meta:
    database = db
