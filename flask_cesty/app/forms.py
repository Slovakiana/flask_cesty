from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField

class TripDetailForm(FlaskForm):
    fiori_zadane = BooleanField('Fiori zadané')
    ziadanka_fiori = BooleanField('Žiadanka Fiori')
    ubytovanie_objednane = BooleanField('Ubytovanie objednané')
    dochadzka = BooleanField('Dochádzka')
    tabulka_G = BooleanField('Tabuľka G')
    vyuctovanie_fiori = BooleanField('Vyúčtovanie Fiori')
    sprava_z_cesty = BooleanField('Správa z cesty')
    submit = SubmitField('Uložiť')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Heslo', validators=[DataRequired()])
    submit = SubmitField('Prihlásiť sa')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Heslo', validators=[DataRequired()])
    confirm_password = PasswordField('Potvrď heslo', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrovať')

class TripForm(FlaskForm):
    meno = StringField('Meno', validators=[DataRequired()])
    priezvisko = StringField('Priezvisko', validators=[DataRequired()])
    spolucestujuci = StringField('Spolucestujúci')
    odkial = StringField('Odkiaľ', validators=[DataRequired()])
    kam = StringField('Kam', validators=[DataRequired()])
    od_datum = DateField('Od dátumu', validators=[DataRequired()])
    do_datum = DateField('Do dátumu', validators=[DataRequired()])
    miesto = StringField('Miesto', validators=[DataRequired()])
    poznamka = TextAreaField('Poznámka k ceste')
    submit = SubmitField('Vytvoriť cestu')

    def validate_do_datum(form, field):
        if form.od_datum.data and field.data:
            if field.data < form.od_datum.data:
                raise ValidationError('Dátum „Do“ musí byť rovnaký alebo neskorší ako dátum „Od“.')
