from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tvojesilnetajomstvopridajsem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_cesty.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
csrf = CSRFProtect(app)

# Import routes aby boli zaregistrované
from app import routes, models

# Vytvorenie databázových tabuliek automaticky pri štarte na Render
with app.app_context():
    print("✅ Spúšťam db.create_all() pre inicializáciu tabuliek...")
    db.create_all()
