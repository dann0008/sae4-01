# Commande pour la création de la machine virtuelle

## Connexion à la machine virtuelle

ssh root@10.31.5.28

## Création d'un utilisateur

    adduser dann0008

    usermod -aG sudo dann0008

    mkdir /home/dann0008/.ssh

    cp /root/.ssh/authorized_keys /home/dann0008/.ssh/

    chown dann0008 /home/dann0008/.ssh /home/dann0008/.ssh/authorized_keys

## Mise à jour de la machine virtuelle

    apt update && apt upgrade -y

## Installation d'un serveur mariadb

    apt install mariadb-server

    mysql_secure_installation

## Installation du service apache2
    apt install apache2
## Installation de php en version 7.4 avec des extensions pour mysql

    apt install php7.4 php-mysql php-xml

## Téléchargement et installation de phpmyadmin 

    wget https://files.phpmyadmin.net/phpMyAdmin/4.9.11/phpMyAdmin-4.9.11-all-languages.tar.gz

    mv phpMyAdmin-4.9.11-all-languages.tar.gz /var/www/html/

    cd /var/www/html/

    tar xvf phpMyAdmin-4.9.11-all-languages.tar.gz

    mv phpMyAdmin-4.9.11-all-languages/ phpmyadmin

## Création d'un utilisateur root avec le mot de passe sae41 dans la base de données

    mysql -p
    MariaDB [(none)]> SET PASSWORD FOR root@localhost=PASSWORD('sae41');
    MariaDB [(none)]> GRANT ALL PRIVILEGES ON *.* TO root@localhost IDENTIFIED BY 'sae41'
        -> WITH GRANT OPTION;

## installation et configuration de git pour récupérer le dépot du projet

    apt-get install git

    git config --global user.email "lucas.danneaux@etudiant.univ-reims.fr"

    git config --global user.name "Lucas Danneaux"

    git config --global --list
    
    git clone https://iut-info.univ-reims.fr/gitlab/dann0008/sae4-01.git
