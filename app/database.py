class database:

    def __init__(self, cursor):
        self.cursor = cursor

    # Suppression de toutes les Tables de la base de données en début d'éxécution de l'application avant de la recréer
    # avec la méthode creation

    def suppression(self):
        self.cursor.execute("""
                    DROP TABLE IF EXISTS ConditionMeteo;
                """)

        self.cursor.execute("""
                    DROP TABLE IF EXISTS Personne;
                """)

        self.cursor.execute("""
                    DROP TABLE IF EXISTS Ville;
                """)

        self.cursor.execute("""
                    DROP TABLE IF EXISTS EPCI;
                """)

        self.cursor.execute("""
                    DROP TABLE IF EXISTS Departement;
                """)

        self.cursor.execute("""
                    DROP TABLE IF EXISTS Region;
                """)

    # Création de toutes les Tables de la base de données après l'exécution de la méthode suppression

    def creation(self):

        self.suppression()

        self.cursor.execute("""
           
           CREATE TABLE Region (
            id int primary key NOT NULL,
            nom varchar(30) NOT NULL
            );
        """)

        self.cursor.execute("""
           
           CREATE TABLE Departement (
             code varchar(3) primary key NOT NULL,
             nom varchar(30) NOT NULL,
             region int NOT NULL,
             constraint FK_DepartementRegion foreign key (region) references Region(id)
             );
        """)

        self.cursor.execute("""
        
           CREATE TABLE EPCI (
            id int primary key NOT NULL AUTO_INCREMENT,
            nom varchar(50) NOT NULL
            );
        """)

        self.cursor.execute("""
        
            CREATE TABLE Ville (
             id int primary key NOT NULL AUTO_INCREMENT,
             nom varchar(50) NOT NULL,
             code_postal varchar(5) NOT NULL,
             departement varchar(3) NOT NULL,
             epci int NOT NULL,
             constraint FK_VilleDepartement foreign key (departement) references Departement(code),
             constraint FK_VilleEPCI foreign key (epci) references EPCI(id)
              );
        """)

        self.cursor.execute("""
        
            CREATE TABLE Personne (
             id int primary key NOT NULL AUTO_INCREMENT,
             sexe boolean NOT NULL,
             dateNais date NOT NULL,
             dateDeces date NOT NULL,
             age int NOT NULL,
             ville int NOT NULL,
             constraint FK_PersonneVille foreign key (ville) references Ville(id)
              );
        """)

        self.cursor.execute("""
        
            CREATE TABLE ConditionMeteo (
             id int primary key NOT NULL AUTO_INCREMENT,
             pression float,
             humidite float,
             vitesseVent float,
             visibilite int,
             nebulosite int,
             precipitation float,
             rafale float,
             temperature float,
             date date NOT NULL,
             epci int NOT NULL,
             constraint FK_ConditionMeteoEPCI foreign key (epci) references EPCI(id)
              );
        """)
