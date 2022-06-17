import os
import secrets
from datetime import datetime, time
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from src.TennisApplication.forms import *
from src.TennisApplication import app, db, bcrypt
from src.TennisApplication.models import User, Tournament, Club, Reservation, Court
from src.TennisApplication.queries import *


@app.route("/")
@app.route("/home")
def home():
    club_names = get_club_names()
    return render_template('home.html', club_names=club_names)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/cancel_reservation/<int:reservation_id>")
@login_required
def cancel_reservation(reservation_id):
    Reservation.query.filter(Reservation.id == reservation_id).delete()
    db.session.commit()
    flash('Reservation cancelled successfully', 'success')
    return redirect(url_for('home'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                    first_name=form.first_name.data, last_name=form.last_name.data, birth_date=form.birth_date.data,
                    phone_number=form.phone_number.data, city=form.city.data)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data} created account! You are able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Unsuccessful login. Check username and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static', 'profile_pictures', picture_name)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_name


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccount()
    if form.validate_on_submit():
        if form.picture.data:
            picture_name = save_picture(form.picture.data)
            current_user.image_file = picture_name
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.birth_date = form.birth_date.data
        current_user.phone_number = form.phone_number.data
        current_user.city = form.city.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.birth_date.data = current_user.birth_date
        form.phone_number.data = current_user.phone_number
        form.city.data = current_user.city
    image_file = url_for('static', filename=os.path.join('profile_pictures', current_user.image_file))
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/my_reservations", methods=['GET', 'POST'])
@login_required
def user_reservations():
    active_reservations, past_reservations = get_user_reservations(current_user.id)
    return render_template('user_reservations.html', title='My Reservations',
                           active_reservations=active_reservations, past_reservations=past_reservations)


@app.route("/reservation", methods=['GET', 'POST'])
def reservation():
    form = FilterReservations()
    reserve = MakeReservation()
    club_names = get_club_names()
    surface_names = get_surface_names()
    show = False
    if request.method == 'GET':
        reservation_date, club_name, surface_type, reservation.courts_reservations = None, None, None, None
    elif request.form.get('filter'):
        show = True
        reservation_date = form.date.data
        club_name = request.form.get('club_name')
        surface_type = request.form.get('surface_name')
        courts = get_courts_by_surface(club_name, surface_type)
        reservations = get_reservations(reservation_date, courts)
        courts_surface_names = get_courts_surface_names(courts)
        reservation.courts_reservations = tuple(zip(courts, courts_surface_names, reservations))
    elif request.form.get('submit'):
        valid_reservation = True
        show = True
        reservation_date = reserve.date.data
        court_number = reserve.court_number.data
        club_name = request.form.get('club_name')
        court = get_court_by_number(club_name, court_number)
        error_msg = 'Unable to commit reservation: '
        if court:
            reservations = get_reservation(reservation_date, court)
        else:
            valid_reservation = False
            reservations = []
            flash(error_msg + 'selected court is invalid', 'danger')
        start_hour, end_hour = 8, 23
        available_hours = [hour not in reservations for hour in range(reserve.hour_from.data, reserve.hour_to.data)]

        if reserve.hour_from.data < start_hour or reserve.hour_to.data > end_hour or \
                reserve.hour_from.data >= reserve.hour_to.data:
            flash(error_msg + 'invalid hours selected', 'danger')
            valid_reservation = False
        elif False in available_hours:
            flash(error_msg + 'reservation for given datetime already made', 'danger')
            valid_reservation = False
        elif reserve.hour_from.data >= reserve.hour_to.data:
            flash(error_msg + 'reservation for given datetime already made', 'danger')
            valid_reservation = False

        if valid_reservation:
            date_from = datetime.combine(reserve.date.data, time(reserve.hour_from.data))
            date_to = datetime.combine(reserve.date.data, time(reserve.hour_to.data))
            if date_from <= datetime.now():
                valid_reservation = False

        if valid_reservation:
            new_reservation = Reservation(user_id=current_user.id, court_id=court.id, date_from=date_from,
                                          date_to=date_to)
            db.session.add(new_reservation)
            db.session.commit()
            flash('You committed reservation succesfully', 'success')
            return redirect(url_for('home'))

    return render_template('reservation.html', title='Reservation', courts_reservations=reservation.courts_reservations,
                           form=form, show=show, club_names=club_names, surface_names=surface_names, reserve=reserve)


@app.route("/tournament", methods=['GET', 'POST'])
def tournament():
    tournaments = [(1, 12, 16), (2, 345, 123)]
    return render_template('tournament.html', title='Tournament', tournaments=tournaments)


@app.route("/tournament_form", methods=['GET', 'POST'])
def tournament_form():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    form = TournamentForm()
    if form.validate_on_submit():
        tournament12 = Tournament(date_from=form.date_from.data, club_id=form.club_id.data,
                                  organizer_id=current_user.get_id(), winner_rewards=form.winner_rewards.data,
                                  min_skill_lvl=form.min_skill_lvl.data, max_players=form.max_players.data,
                                  is_registration_closed=False)
        print(tournament12)
        db.session.add(tournament12)
        db.session.commit()
        flash('tournament added', 'success')
        return redirect(url_for('tournament'))
    return render_template('tournament_form.html', title='Tournament_form', form=form)


@app.route("/tournament_details/<id_t>", methods=['GET', 'POST'])
def tournament_details(id_t):
    tournaments1 = db.session.query(Tournament).all()
    tournament= tournaments1[int(id_t)-1]
    print(tournament)
    # tournament = None
    # for tournament2 in tournaments1:
    #     if tournament2.id == id_t:
    #         print("hi")
    #         tournament = tournament2
    #         break
    #
    # print(tournament)

    return render_template('tournament_details.html', title='Tournament_details', tournament=tournament)

