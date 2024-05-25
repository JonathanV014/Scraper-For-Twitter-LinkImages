import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()





#Replace for your limits
STARTDATE = datetime(2023,5,8) 
ENDDATE = datetime(2023,12,31)

SCROLLTIME = 500 #Seconds
DISTANCE = 250 #Pixels

#where you are going to save your csv
DIRSAVECSV = "imgs/"
NAMECSV = "urlImagenesAccidentes.csv"

#Replace for you search equation
SEARCHEQUATION = "((accidente or siniestro or colision or choque) and (transito or vehicular or automovilistico)))"



#Read from your .env twitter username and password 
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')

