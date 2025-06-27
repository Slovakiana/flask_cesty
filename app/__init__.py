import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# Bezpecne nacitanie SECRET_KEY z prostredia
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret')

# Databaza - Render odporucane pouzit SQLite alebo PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///cesty.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'   # ✅ toto opravi Unauthorized
csrf = CSRFProtect(app)

from app import routes, models