import requests
import json
import datetime
import pandas as pd
import unidecode
import datetime


class city:

    def __init__(self, db, cursor, epci):
        self.db = db
        self.cursor = cursor
        self.epci = epci
        self.ville = []

    # Ajout de tout les EPCI présent dans la première requête à l'API des données météorologique ainsi que des régions
    # et département auquel elles appartiennent


    def ajoutEPCI(self, date):
        uri = f"https://public.opendatasoft.com/api/records/1.0/search/?dataset=donnees-synop-essentielles-omm&q=&rows=500&&refine.date={date}"
        response = requests.get(uri)
        cities = response.json()

        for record in cities['records']:
            if 'nom_epci' in record['fields']:
                epci = record['fields']['nom_epci']
                epci = unidecode.unidecode(epci)

                if epci in ['CA Mont-de-Marsan Agglomeration', 'CC de Belle-Ile-en-Mer']:
                    epci = epci.replace('-', ' ')

                if epci == 'CA Cap Excellence':
                    epci = 'CA CAP Excellence'

                if epci not in self.epci:
                    self.epci.append(epci)
                    code_region = record['fields']['code_reg']
                    donnee_region = self.cursor.execute(f"SELECT id from Region WHERE id = {code_region}")

                    if donnee_region == 0:
                        nom_region = (record['fields']['nom_reg'])
                        self.cursor.execute(f"INSERT INTO Region (id, nom) VALUES(%s, %s)", (code_region, nom_region))
                        self.db.commit()

                    code_departement = record['fields']['code_dep']
                    donnee_departement = self.cursor.execute(f"SELECT code from Departement WHERE code=%s",
                                                             code_departement)

                    if donnee_departement == 0:
                        nom_departement = (record['fields']['nom_dept'])
                        self.cursor.execute(f"INSERT INTO Departement (code, nom, region) VALUES(%s, %s, %s)",
                                            (code_departement, nom_departement, code_region))

                    self.cursor.execute(f"INSERT INTO EPCI (nom) VALUES(%s)", epci)
                    self.db.commit()
        return self.epci

    # Ajout des villes qui sont dans les EPCI recueilli à partir du fichier epcicom2023
    # ainsi que leur département si celui-ci est abscent de la base de données

    def ajoutVille(self):
        data = pd.read_excel("data/epcicom2023.xlsx")

        for ligne in data.itertuples():
            epci = unidecode.unidecode(ligne[3])
            if epci in self.epci:
                nom = ligne[12]
                code_postal = ligne[10]
                departement = ligne[9]
                donnee_departement = self.cursor.execute(f"SELECT code from Departement WHERE code=%s", departement)

                if donnee_departement == 0:
                    data_departement = pd.read_csv("data/departements-france.csv")

                    for ligne_departement in data_departement.itertuples():
                        nom_departement = ligne_departement[2]
                        code_departement = ligne_departement[1]
                        code_region = ligne_departement[3]

                        if departement == code_departement:
                            self.cursor.execute(f"INSERT INTO Departement (code, nom, region) VALUES(%s, %s, %s)",
                                                (code_departement, nom_departement, code_region))

                self.cursor.execute(f"SELECT id from EPCI WHERE nom=%s", epci)
                donnee_epci = self.cursor.fetchone()
                self.cursor.execute(f"INSERT INTO Ville (nom, code_postal, departement, epci) VALUES(%s, %s, %s, %s)",
                                    (nom, code_postal, departement, donnee_epci[0]))
                self.db.commit()

    # Ajout d'une EPCI qui n'est pas dans la base de données ainsi les villes qui la compose que leur département et
    # région si ces derniers ne sont pas dans la base de données

    def EPCIManquant(self, nom, code_region, nom_region, code_departement, nom_departement):
        nom = unidecode.unidecode(nom)
        self.epci.append(nom)
        donnee_region = self.cursor.execute(f"SELECT id from Region WHERE id = {code_region}")

        if donnee_region == 0:
            self.cursor.execute(f"INSERT INTO Region (id, nom) VALUES(%s, %s)", (code_region, nom_region))
            self.db.commit()

        donnee_departement = self.cursor.execute(f"SELECT code from Departement WHERE code=%s",
                                                 code_departement)

        if donnee_departement == 0:
            self.cursor.execute(f"INSERT INTO Departement (code, nom, region) VALUES(%s, %s, %s)",
                                (code_departement, nom_departement, code_region))
            self.db.commit()

        donnee_epci = self.cursor.execute(f"SELECT id from EPCI WHERE nom=%s",
                                          nom)

        if donnee_epci == 0:
            self.cursor.execute(f"INSERT INTO EPCI (nom) VALUES(%s)", nom)
            self.db.commit()
            self.villeManquante(nom)

        return self.epci

    # Ajout des villes qui sont dans l'EPCI manquante à partir du fichier epcicom2023
    # ainsi que leur département si celui-ci est abscent de la base de données

    def villeManquante(self, nom_EPCI):
        data = pd.read_excel("data/epcicom2023.xlsx")

        for ligne in data.itertuples():
            epci = unidecode.unidecode(ligne[3])
            if epci == nom_EPCI:
                nom = ligne[12]
                code_postal = ligne[10]
                departement = ligne[9]
                donnee_departement = self.cursor.execute(f"SELECT code from Departement WHERE code=%s", departement)

                if donnee_departement == 0:
                    data_departement = pd.read_csv("../data/departements-france.csv")

                    for ligne_departement in data_departement.itertuples():
                        nom_departement = ligne_departement[2]
                        code_departement = ligne_departement[1]
                        code_region = ligne_departement[3]

                        if departement == code_departement:
                            self.cursor.execute(f"INSERT INTO Departement (code, nom, region) VALUES(%s, %s, %s)",
                                                (code_departement, nom_departement, code_region))

                self.cursor.execute(f"SELECT id from EPCI WHERE nom=%s", epci)
                donnee_epci = self.cursor.fetchone()
                self.cursor.execute(f"INSERT INTO Ville (nom, code_postal, departement, epci) VALUES(%s, %s, %s, %s)",
                                    (nom, code_postal, departement, donnee_epci[0]))
                self.db.commit()

    # Récupération de toutes les villes de la base de données dans une liste

    def recuperationVille(self, lst_epci):
        lst_ville = []
        for epci in lst_epci:
            self.cursor.execute(f"SELECT id from EPCI WHERE nom=%s ", epci)
            donne_epci = self.cursor.fetchone()
            self.cursor.execute(f"SELECT id from Ville WHERE epci=%s ", donne_epci[0])
            donnee_ville = self.cursor.fetchall()
            for ville in donnee_ville:
                lst_ville.append(ville[0])
        return lst_ville
