from app.connection import db, cursor
from app.database import database
from app.city import city
from app.people import people
from app.weather import weather
import datetime
import time

# initialisation de l'application à la date du 1er janvier 2010, avec la création de la base de données, des classes
# City, People et Weather

annee = 2010
jour = 1
mois = 1
date = datetime.date(annee, mois, jour)
date = date.strftime("%Y/%m/%d")

database = database(cursor)
database.creation()

city = city(db, cursor, [])
epci = city.ajoutEPCI(date)
city.ajoutVille()

people = people(db, cursor)
weather = weather(db, cursor, epci)

# Création d'une boucle d'exécution permettant l'exécution des méthodes d'utilisation des API dans les classes
# weather et people afin de remplir la base de donénes pour chaque journée sans jamais être interrompu

while database:
    try:
        date = datetime.date(annee, mois, jour)
        date = date.strftime("%Y/%m/%d")
        lst_epci = weather.ajoutCondition(date)
        while not lst_epci:
            time.sleep(120)
            lst_epci = weather.ajoutCondition(date)
        lst_ville = city.recuperationVille(lst_epci)
        data = people.ajoutPersonne(date, lst_ville)
        while data is False:
            time.sleep(7200)
            data = people.ajoutPersonne(date)
        jour += 1
    except ValueError:
        if mois != 12:
            jour = 1
            mois += 1
        else:
            jour = 1
            mois = 1
            annee += 1

