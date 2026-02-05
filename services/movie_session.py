import datetime
from typing import Optional

from django.db.models.query import QuerySet
from django.utils import timezone

from db.models import CinemaHall, Movie, MovieSession


def create_movie_session(
        movie_show_time: datetime.datetime,
        movie_id: int,
        cinema_hall_id: int,
) -> None:
    movie = Movie.objects.get(id=movie_id)
    cinema_hall = CinemaHall.objects.get(id=cinema_hall_id)

    MovieSession.objects.create(
        show_time=movie_show_time,
        cinema_hall=cinema_hall,
        movie=movie,
    )


def get_movies_sessions(
        session_date: Optional[str] = None,
) -> QuerySet[MovieSession]:
    qs = MovieSession.objects.all()
    if session_date is not None:
        day = datetime.date.fromisoformat(session_date)
        qs = qs.filter(show_time__date=day)
    return qs


def get_movie_session_by_id(id:int) -> MovieSession:
    return MovieSession.objects.get(id=id)


def update_movie_session(
        session_id: int,
        show_time: Optional[str] = None,
        movie_id: Optional[int] = None,
        cinema_hall_id: Optional[int] = None,
) -> None:

    session = MovieSession.objects.get(id=session_id)

    if show_time is not None:
        session.show_time = parse_show_time(show_time)

    if movie_id is not None:
        session.movie_id = movie_id

    if cinema_hall_id is not None:
        session.cinema_hall_id = cinema_hall_id

    session.save()


def delete_movie_session_by_id(session_id: int) -> None:
    session = MovieSession.objects.get(id=session_id)
    session.delete()


def parse_show_time(show_time: str) -> datetime.datetime:
    if show_time.endswith("Z"):
        # UTC explícito
        return datetime.datetime.fromisoformat(
            show_time.replace("Z", "+00:00")
        )
    else:
        # Hora local (Ucrania)
        naive = datetime.datetime.fromisoformat(show_time)
        return timezone.make_aware(
            naive,
            timezone.get_current_timezone()
        )
