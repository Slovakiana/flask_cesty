from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meno = db.Column(db.String(120), nullable=False)
    priezvisko = db.Column(db.String(120), nullable=False)
    spolucestujuci = db.Column(db.String(120))
    odkial = db.Column(db.String(120), nullable=False)
    kam = db.Column(db.String(120), nullable=False)
    od_datum = db.Column(db.Date, nullable=False)
    do_datum = db.Column(db.Date, nullable=False)
    miesto = db.Column(db.String(120), nullable=False)
    poznamka = db.Column(db.Text)

    fiori_zadane = db.Column(db.Boolean, default=False)
    ziadanka_fiori = db.Column(db.Boolean, default=False)
    ubytovanie_objednane = db.Column(db.Boolean, default=False)
    dochadzka = db.Column(db.Boolean, default=False)
    tabulka_G = db.Column(db.Boolean, default=False)
    vyuctovanie_fiori = db.Column(db.Boolean, default=False)
    sprava_z_cesty = db.Column(db.Boolean, default=False)

    def stav(self):
        dnes = date.today()
        checkboxy = [
            self.fiori_zadane, self.ziadanka_fiori, self.ubytovanie_objednane,
            self.dochadzka, self.tabulka_G, self.vyuctovanie_fiori, self.sprava_z_cesty
        ]
        if all(checkboxy) and dnes > self.do_datum:
            return "Ukončená"
        elif self.od_datum <= dnes <= self.do_datum:
            return "Prebiehajúca"
        elif any(checkboxy):
            return "Rozpracovaná"
        else:
            return "Vytvorená"
