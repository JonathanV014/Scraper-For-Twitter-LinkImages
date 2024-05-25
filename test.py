import os
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
SCROLLTIME = 500
DISTANCE = 250
imagesl = set()
imagesClass = "css-9pa8cd"


years = [2024]
months = [31, 28, 31, 30, 22, 0, 0, 0, 0, 0, 0, 0 ] #30, 31, 31, 30, 31, 30, 31 

def extractImagesForDay(page):
    end = False
    while not end:
        extractImageUrls(page, imagesClass)
        print(len(imagesl))
        showLinks()
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
    input("Somos la recontra verga")
    

def extractImageUrls(page, cn):
    images = page.query_selector_all(f'img.{cn}')
    for img in images:
        link = img.get_attribute('src')
        if "profile_images" not in link:
            imagesl.add(link)

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
    time.sleep(12)



    date = ["2024-01-01","2024-01-02"]
    page.goto(f"https://x.com/search?q=((accidente%20or%20siniestro%20or%20colision%20or%20choque)%20and%20(transito%20or%20vehicular%20or%20automovilistico)))%20since%3A{date[0]}%20until%3A{date[1]}&src=spelling_expansion_revert_click")
    print(date[0], date[1])
    time.sleep(5)

    extractImagesForDay(page)

    
    
            

    
    
    

    

    