from configureScrapper import *
from test import TwitterScrapper


#Create object TwitterScrapper and run
myScrapper = TwitterScrapper(startDate=STARTDATE, endDate=ENDDATE, scrollTime=SCROLLTIME, distance=DISTANCE,dirSaveCsv=DIRSAVECSV, nameCsv=NAMECSV,searchEquation=SEARCHEQUATION, user=USER, password=PASSWORD)

myScrapper.startScrapper()