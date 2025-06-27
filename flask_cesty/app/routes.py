from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_required, login_user, logout_user
from datetime import datetime, date, timedelta
from app.forms import TripDetailForm

from app import app, db, login_manager
from app.models import Trip, User
from app.forms import LoginForm, TripForm, RegisterForm


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET'])
@login_required
def index():
    trips = Trip.query.all()
    events = []
    for trip in trips:
        stav = trip.stav()
        color = "#0d6efd"  # default modrá
        if stav == "Rozpracovaná":
            color = "#fd7e14"  # oranžová
        elif stav == "Prebiehajúca":
            color = "#198754"  # zelená
        elif stav == "Ukončená":
            color = "#6c757d"  # sivá

        events.append({
            "title": f"{trip.meno} {trip.priezvisko}: {trip.odkial} → {trip.kam}",
            "start": trip.od_datum.isoformat(),
            "end": (trip.do_datum + timedelta(days=1)).isoformat(),  # FullCalendar exclusive end
            "url": url_for('trip_detail', trip_id=trip.id),
            "color": color
        })

    return render_template('index.html', trips=trips, events=events)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Prihlásenie úspešné.", "success")
            return redirect(url_for('index'))
        else:
            flash("Nesprávny email alebo heslo.", "danger")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/create_trip', methods=['GET', 'POST'])
@login_required
def create_trip():
    form = TripForm()
    destinacie_od = [trip.odkial for trip in Trip.query.distinct(Trip.odkial).all()]
    destinacie_kam = [trip.kam for trip in Trip.query.distinct(Trip.kam).all()]

    if form.validate_on_submit():
        trip = Trip(
            meno=form.meno.data,
            priezvisko=form.priezvisko.data,
            spolucestujuci=form.spolucestujuci.data,
            odkial=form.odkial.data,
            kam=form.kam.data,
            od_datum=form.od_datum.data,
            do_datum=form.do_datum.data,
            miesto=form.miesto.data,
            poznamka=form.poznamka.data
        )
        db.session.add(trip)
        db.session.commit()
        flash('Cesta bola úspešne vytvorená.', 'success')
        return redirect(url_for('index'))

    return render_template('create_trip.html', form=form, destinacie_od=destinacie_od, destinacie_kam=destinacie_kam)


@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        abort(403)
    trips = Trip.query.all()
    users = User.query.all()
    return render_template('admin.html', trips=trips, users=users)


@app.route('/trip/<int:trip_id>', methods=['GET', 'POST'])
@login_required
def trip_detail(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    form = TripDetailForm(obj=trip)

    if form.validate_on_submit():
        form.populate_obj(trip)
        db.session.commit()
        flash("Stav úloh bol aktualizovaný.", "success")
        return redirect(url_for('trip_detail', trip_id=trip.id))

    # Progress bar výpočet
    tasks = [
        form.fiori_zadane.data,
        form.ziadanka_fiori.data,
        form.ubytovanie_objednane.data,
        form.dochadzka.data,
        form.tabulka_G.data,
        form.vyuctovanie_fiori.data,
        form.sprava_z_cesty.data
    ]
    progress_percent = int((sum(tasks) / len(tasks)) * 100)

    return render_template('trip_detail.html', trip=trip, progress=progress_percent, form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Používateľ s týmto emailom už existuje.", "warning")
            return redirect(url_for('register'))
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registrácia úspešná, môžeš sa prihlásiť.", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
