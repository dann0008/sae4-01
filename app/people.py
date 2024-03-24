import requests
import json


class people:

    def __init__(self, db, cursor):
        self.db = db
        self.cursor = cursor

    # Requête sur l'api des personnes décédés pour une journée donnée afin de récupérer les personnes qui sont décédés
    # dans une ville présente dans la liste des villes afin d'en extraire certaines informations pour les insérer dans
    # la base de données

    def ajoutPersonne(self, date, lst_ville) -> bool:
        uri = f'https://public.opendatasoft.com/api/records/1.0/search/?dataset=liste-des-personnes-decedees-en-france&q=&rows=3000&refine.death_date={date}'
        response = requests.get(uri)
        people = response.json()
        data = False
        for record in people['records']:
            data = True
            if "sex" in record['fields'] and "birth_date" in record['fields'] and "age" in record['fields'] and "current_death_com_name" in record['fields']:
                sexe = False
                if record['fields']['sex'] == 'F':
                    sexe = True
                date_nais = record['fields']['birth_date']
                age = record['fields']['age']
                ville = record['fields']['current_death_com_name']
                if 'Paris' in ville:
                    ville = 'Paris'
                donnee_ville = self.cursor.execute(f"SELECT id, epci from Ville WHERE nom=%s ", ville)
                if donnee_ville == 1:
                    donnee_ville = self.cursor.fetchone()
                    id_ville = donnee_ville[0]
                    if id_ville in lst_ville:
                        self.cursor.execute(
                            f"INSERT INTO Personne (sexe, dateNais, dateDeces, age, ville) VALUES(%s, %s, %s, "
                            f"%s, %s)", (sexe, date_nais, date, age, id_ville))
                        self.db.commit()
        return data
