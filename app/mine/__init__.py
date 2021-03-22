from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_apscheduler import APScheduler

app=Flask(__name__)
scheduler = APScheduler()

#login = LoginManager(app)
#def schedtask():
#	print('running')
#db=SQLAlchemy(app)
#migrate=Migrate(app,db)
from mine import routes

