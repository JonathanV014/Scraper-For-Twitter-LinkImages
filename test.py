import csv
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta

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
        
    def generateDates(self) -> list:
        dates = []
        fechaI = self.STARTDATE
        while fechaI <= self.ENDDATE:
            dates.append(fechaI.strftime("%Y-%m-%d"))
            fechaI += timedelta(days=1)
        return dates
    
    def generateUrlEquation(self, equation):
        equation = equation.replace(" ", "%20")
        equation = equation.replace("since:", "since%3A")
        equation = equation.replace("until:", "until%3A")
        url = f"https://x.com/search?q={equation}&src=spelling_expansion_revert_click"
        return url


    def saveCSV(self):
        for url in self.IMAGESL:
            img = {"#": self.ITERA, "URL": url}
            self.ITERA = self.ITERA + 1
            self.IMGPRETOCSV.append(img)
            
        with open(self.DIR, 'w', newline='') as f:
            write = csv.DictWriter(f, fieldnames=['#', "URL"])
            write.writeheader()
            write.writerows(self.IMGPRETOCSV)

        print("Guardado exitosamente")

    def extractImagesForDay(self, page):
        start = datetime.now()
        end = False
        while not end:
            self.extractImageUrls(page, self.IMAGESCLASS)
            end = page.evaluate("""() => {
                const scrollHeight = document.documentElement.scrollHeight;
                const scrollTop = window.pageYOffset;
                return (scrollTop + window.innerHeight) >= scrollHeight;
            }""")
            if not end:
                page.evaluate(f"""async () => {{
                    await new Promise(resolve => {{
                        const scrollHeight = document.documentElement.scrollHeight;
                        const distance = {self.DISTANCE}; 
                        const delay = {self.SCROLLTIME}; 
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
        self.showLinks()
        end = datetime.now()
        print("---------------------------------------------")
        print("Total URLS extraidas en la fecha: ", len(self.IMAGESL))
        diference = -1
        if start > end:
            diference =  start - end
        else:
            diference = end - start
        print("Tomó: ", diference, " en terminar")

    def extractImageUrls(self, page, cn):
        images = page.query_selector_all(f'img.{cn}')
        for img in images:
            link = img.get_attribute('src')
            if "profile_images" not in link and link not in self.IMAGESLT:
                self.IMAGESL.add(link)
                self.IMAGESLT.add(link)

    def generateForDate(self, dtStart, dtEnd, page):
        print("\n---------------------------------------------")
        print("Fecha: ", dtStart, dtEnd, '\n')

        equation = self.SEARCHEQUATION 
        equation = f"{self.SEARCHEQUATION} since:{dtStart} until:{dtEnd}"
        url = self.generateUrlEquation(equation)

        page.goto(url)
        time.sleep(7)

        self.extractImagesForDay(page)
        self.saveCSV()
        self.IMAGESL.clear()
    
    def showLinks(self):
        for link in self.IMAGESL:
            print(link)

    def startScrapper(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=50)
            page = browser.new_page()
            page.goto('https://x.com/i/flow/login')
            
            page.wait_for_selector('//*[contains(concat( " ", @class, " " ), concat( " ", "r-fdjqy7", " " ))]')
            page.fill('//*[contains(concat( " ", @class, " " ), concat( " ", "r-fdjqy7", " " ))]', self.USER)

            page.click('//button[div/span/span[contains(text(), "Siguiente")]]')

            page.wait_for_selector('input[name="password"]')
            page.fill('input[name="password"]', self.PASSWORD)

            page.click('//button[div/span/span[contains(text(), "Iniciar sesión")]]')
            time.sleep(7)

            for j in range(1,len(self.DATES)):
                i = j-1
                self.generateForDate(self.DATES[i], self.DATES[j], page)
            print("\n---------------------------------------------")
            print("Total de URLS extraidas: ", len(self.IMAGESLT))
            input("PROCESO TERMINADO")
            page.close()
    

    
   
    

    
    
            

    
    
    

    

    