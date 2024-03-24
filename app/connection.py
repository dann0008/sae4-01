import pymysql
# Pour des raisons de sécurité en raisons de la réalisation du projet sur machine personnel, le mot de passe ne sera
# jamais précisé
db = pymysql.connect(host="localhost", port=3306, user="dann0008", passwd="sae41", database="dann0008_sae_data")
cursor = db.cursor()
