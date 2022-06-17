from datetime import datetime
from sqlalchemy import and_
from src.TennisApplication.models import Club, Reservation, Court, Surface


def get_location_info_of_reservation(reservation):
    court = Court.query.filter(Court.id == reservation.court_id).first()
    club = Club.query.filter(Club.id == court.club_id).first()
    return court.court_number, club.name


def get_user_reservations(user_id):
    reservations = Reservation.query.filter(Reservation.user_id == user_id).all()
    active = tuple(filter(lambda reservation: reservation.date_to >= datetime.now(), reservations))
    active_reservations = [(reservation, *get_location_info_of_reservation(reservation)) for reservation in active]
    past = tuple(filter(lambda reservation: reservation.date_to < datetime.now(), reservations))
    past_reservations = [(reservation, *get_location_info_of_reservation(reservation)) for reservation in past]
    return active_reservations, past_reservations


def get_courts_by_surface(club_name, surface_type):
    club_id = Club.query.filter(Club.name == club_name).first().id
    if surface_type == 'all':
        courts = Court.query.filter(Court.club_id == club_id).all()
    else:
        surfaces = Surface.query.filter(Surface.type == surface_type).all()
        if surfaces:
            surface_id = Surface.query.filter(Surface.type == surface_type).first().id
            courts = Court.query.filter(and_(Court.club_id == club_id, Court.surface_id == surface_id)).all()
        else:
            courts = []
    return courts


def get_club_by_name(club_name):
    return Club.query.filter(Club.name == club_name).first()


def get_court_by_number(club_name, court_number):
    club = get_club_by_name(club_name)
    if not club:
        return None
    court = Court.query.filter(and_(Court.club_id == club.id, Court.court_number == court_number)).first()
    return court


def get_reservation(date, court):
    reservations = Reservation.query.filter(Reservation.court_id == court.id).all()
    reservations = [reservation for reservation in reservations if reservation.date_from.date() == date]
    reservation_list = [list(range(reservation.date_from.hour, reservation.date_to.hour))
                        for reservation in reservations]
    flatten_list = [hours for reservation in reservation_list for hours in reservation]
    return flatten_list


def get_reservations(date, courts):
    return [get_reservation(date, court) for court in courts]


def get_surface_names():
    surfaces = Surface.query.all()
    surface_names = [surface.type for surface in surfaces]
    return surface_names


def get_court_surface_name(court):
    return Surface.query.filter(Surface.id == court.surface_id).first().type


def get_courts_surface_names(courts):
    surfaces = [get_court_surface_name(court) for court in courts]
    return surfaces


def get_club_names():
    club_name_rows = Club.query.with_entities(Club.name).all()
    club_names = [row[0] for row in club_name_rows]
    return club_names

