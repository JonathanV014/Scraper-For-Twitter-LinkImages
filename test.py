import os
import csv
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta

load_dotenv()

class TwitterScrapper():
    def __init__(self, startDate, endDate, scrollTime, distance, dirSaveCsv, nameCsv, searchEquation, user, password):

        self.STARTDATE = startDate
        self.ENDDATE = endDate
        self.SCROLLTIME = scrollTime
        self.DISTANCE = distance    
        self.DIRSAVECSV = dirSaveCsv
        self.NAMECSV = nameCsv
        self.SEARCHEQUATION = searchEquation 
        self.USER = user
        self.PASSWORD = password

        self.DIR = self.DIRSAVECSV+self.NAMECSV
        self.IMAGESCLASS = imagesClass = "css-9pa8cd"
        self.ITERA = 0

        self.DATES = self.generateDates()
        self.IMAGESL = set()
        self.IMAGESLT = set()
        self.IMGPRETOCSV = []

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
SCROLLTIME = 700
DISTANCE = 250
imagesl = set()
imagesLT = set()
imagesClass = "css-9pa8cd"
imgPreToCsv = []
itera = 0


##LLEGUÉ HASTA 2023-05-07
startDate = datetime(2023,8,22)
endDate = datetime(2023,12,31)

dates = []
fechaI = startDate
while fechaI <= endDate:
    dates.append(fechaI.strftime("%Y-%m-%d"))
    fechaI += timedelta(days=1)


#years = [2024]
#months = [31, 28, 31, 30, 22, 0, 0, 0, 0, 0, 0, 0 ] #30, 31, 31, 30, 31, 30, 31 
print( os.path.exists('imgs/imagenesAcidentes.csv'))

def saveCSV():
    global itera
    for url in imagesl:
        img = {"#": itera, "URL": url}
        itera = itera + 1
        imgPreToCsv.append(img)
        
    with open('imgs/imagenesAcidentes.csv', 'w', newline='') as f:
        write = csv.DictWriter(f, fieldnames=['#', "URL"])
        write.writeheader()
        write.writerows(imgPreToCsv)
        
        
    print("Guardado exitosamente")

def extractImagesForDay(page):
    start = datetime.now()
    end = False
    while not end:
        extractImageUrls(page, imagesClass)
        end = page.evaluate("""() => {
            const scrollHeight = document.documentElement.scrollHeight;
            const scrollTop = window.pageYOffset;
            return (scrollTop + window.innerHeight) >= scrollHeight;
        }""")
        if not end:
            page.evaluate(f"""async () => {{
                await new Promise(resolve => {{
                    const scrollHeight = document.documentElement.scrollHeight;
                    const distance = {DISTANCE}; 
                    const delay = {SCROLLTIME}; 
                    let scrollTop = window.pageYOffset;
                    const scrollStep = () => {{
                        scrollTop += distance;
                        if (scrollTop >= scrollHeight) {{
                            resolve();
                            return;
                        }}
                        window.scrollTo(0, scrollTop);
                        setTimeout(scrollStep, delay);
                    }};
                    scrollStep();
                }});
            }}""")
    showLinks()
    end = datetime.now()
    print("---------------------------------------------")
    print("Total URLS extraidas en la fecha: ", len(imagesl))
    diference = -1
    if start > end:
        diference =  start - end
    else:
        diference = end - start
    print("Tomó: ", diference, " en terminar")

    
    
    

def extractImageUrls(page, cn):
    images = page.query_selector_all(f'img.{cn}')
    for img in images:
        link = img.get_attribute('src')
        if "profile_images" not in link and link not in imagesLT:
            imagesl.add(link)
            imagesLT.add(link)

def generateForDate(dtStart, dtEnd, page):
    print("\n---------------------------------------------")
    print("Fecha: ", dtStart, dtEnd, '\n')
    page.goto(f"https://x.com/search?q=((accidente%20or%20siniestro%20or%20colision%20or%20choque)%20and%20(transito%20or%20vehicular%20or%20automovilistico)))%20since%3A{dtStart}%20until%3A{dtEnd}&src=spelling_expansion_revert_click")
    time.sleep(5)
    extractImagesForDay(page)
    saveCSV()
    imagesl.clear()
    
def showLinks():
    for link in imagesl:
        print(link)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    page.goto('https://x.com/i/flow/login')
    
    page.wait_for_selector('//*[contains(concat( " ", @class, " " ), concat( " ", "r-fdjqy7", " " ))]')
    page.fill('//*[contains(concat( " ", @class, " " ), concat( " ", "r-fdjqy7", " " ))]', USER)


    page.click('//button[div/span/span[contains(text(), "Siguiente")]]')
    
    

    page.wait_for_selector('input[name="password"]')
    page.fill('input[name="password"]', PASSWORD)


    page.click('//button[div/span/span[contains(text(), "Iniciar sesión")]]')
    time.sleep(6)

    for j in range(1,len(dates)):
        i = j-1
        generateForDate(dates[i], dates[j], page)
    print("\n---------------------------------------------")
    print("Total de URLS extraidas: ", len(imagesLT))
    input("Soy la recontra verga-Terminado")
    page.close()
    

    
   
    

    
    
            

    
    
    

    

    