# Sae4-01

## Auteur

- Danneaux Lucas (dann0008)

## Description des API

### 1ère API

Accessible par le lien suivant

>https://public.opendatasoft.com/explore/dataset/liste-des-personnes-decedees-en-france/information/

Permet de récupérer des informations sur les personnes décédés en France depuis 1970

### 2ème API

Accessible par le lien suivant

>https://public.opendatasoft.com/explore/dataset/donnees-synop-essentielles-omm/information/

Permet de récupérer des informations météorologiques en France depuis 2010 toutes les 3h

## Installation/Configuration 

### Installation

Installation de tout les paquages nécessaires au fonctionnement de l'application dans l'environnement

    pip install –r requirements.txt

### Configuration

    il faut configurer la base de données à utiliser dans le fichier app/connection.py

    Vous pouvez modifier la date de début de l'application à votre guise dans le fichier application.py
    (attention cette date doit être après le 1er Janvier 2010 et avant les dernières données insérés, à ce
    jour le 27 Février 2023)

### Lancer l'application

    python3 application.py

## Accès aux services

### Accéder à la base de données

>http://10.31.5.28/phpmyadmin

    utilisateur : sae41
    mot de passe : sae41
    base de données : dann0008_sae_data

### Accéder à la visualisation

    La visualisation est dans le fichier Visualisation sae4-01.pbix

    Attention : les données se sont pas mise à jour car la connextion avec la machine virtuelle 
    est infonctionnelle

    