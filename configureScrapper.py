import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()





STARTDATE = datetime(2023,5,8) #Replace for your limits
ENDDATE = datetime(2023,12,31)

SCROLLTIME = 500 #Seconds
DISTANCE = 250 #Pixels

DIRSAVECSV = "imgs/"
NAMECSV = "urlImagenesAccidentes.csv"

#Replace for you search equation
SEARCHEQUATION = "((accidente or siniestro or colision or choque) and (transito or vehicular or automovilistico)))"


#Read from your .env twitter username and password 
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')



SEARCHEQUATION = SEARCHEQUATION.replace(" ", "%20")
SEARCHEQUATION = SEARCHEQUATION.replace("since:", "since%3A")
SEARCHEQUATION = SEARCHEQUATION.replace("until:", "until%3A")



COMOQUEDA = f"https://x.com/search?q=((accidente%20or%20siniestro%20or%20colision%20or%20choque)%20and%20(transito%20or%20vehicular%20or%20automovilistico)))%20since%3A2023-05-08%20until%3A2023-05-09&src=spelling_expansion_revert_click"

falq = f"https://x.com/search?q={SEARCHEQUATION}&src=spelling_expansion_revert_click" 
print(falq)
print(len(falq))
print(len(COMOQUEDA))

print(falq == COMOQUEDA)
# # print(SEARCHEQUATION)