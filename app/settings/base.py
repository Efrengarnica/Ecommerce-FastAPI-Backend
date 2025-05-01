from pathlib import Path #Ncessario para poder leer el .env en el test
from dotenv import load_dotenv #Necesario para pode leer el .env en el test
import os
 
# settings/base.py
# 1) Indica la ruta de tu .env (por defecto en el mismo nivel de settings/)
ENV_PATH = Path(__file__).parent.parent / ".env" #Necesario para poder leer el .env en el test

# 2) Carga las variables de entorno desde ese fichero
load_dotenv(dotenv_path=ENV_PATH)    # <— lee automáticamente tu .env y lo inyecta en os.environ, neceario para el test.

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "ecommerce_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") #Busca en mi local la varible de ambiente que se llame de esa forma, en el .env.
#Esto es para ver si el contenedor una vez que se levanta reconoce la variable de ambiente de mi local, print(JWT_SECRET_KEY).