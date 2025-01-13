from datetime import datetime
from datetime import timedelta

class DateUtils():
    @staticmethod
    def getDate(jour, semaine, annee):
        """Renvoie la date du jour et de la semaine donnés et de l'année donnée

        Args:
            jour (int): Le jour de la semaine
            semaine (int): Le numéro de la semaine
            annee (int): L'année

        Returns:
            datetime: La date
        """
        first_day_of_year = datetime(annee, 1, 1)
        days_to_first_week = timedelta(days=(7 - first_day_of_year.weekday()))
        first_week_start = first_day_of_year + days_to_first_week
        target_date = first_week_start + timedelta(weeks=semaine-2, days=jour-1)
        return target_date