import os
 
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "ecommerce_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") #Busca en mi local la varible de ambiente que se llame de esa forma, en el .env.
#Esto es para ver si el contenedor una vez que se levanta reconoce la variable de ambiente de mi local, print(JWT_SECRET_KEY).