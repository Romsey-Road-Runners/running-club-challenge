from agegrader.agegrader import AgeGrader
import decimal


def get_activity_age_grade(athlete, elapsed_time, race, start_time):
    age = get_athlete_age(athlete=athlete, date=start_time.date())
    if not age:
        return 0
    age_grader = AgeGrader()
    age_graded_performance_factor = age_grader.age_graded_performance_factor(
        age,
        athlete.sex,
        race_distance_in_km(race),
        elapsed_time.total_seconds(),
    )
    return age_graded_performance_factor * 100


def get_athlete_age(athlete, date):
    date_of_birth = athlete.DOB
    if not date_of_birth:
        return None

    return (
        date.year
        - date_of_birth.year
        - ((date.month, date.day) < (date_of_birth.month, date_of_birth.day))
    )


def race_distance_in_km(race):
    if race.distance_unit == "M":
        race_distance_km = race.distance * decimal.Decimal(1.609344)
    else:
        race_distance_km = race.distance
    return float(race_distance_km)
