from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import time
import csv
import random
from bs4 import BeautifulSoup
import os

def tecnocasa(driver,city,url_given,cookies_click):
    url_site = str(url_given) + "1"
    driver.get(url_site)
    time.sleep(random.uniform(4,6))
    if cookies_click==True:
        cookies = driver.find_element(By.XPATH, "/html/body/div[3]/button[1]")
        cookies.click()
    time.sleep(random.uniform(4,6))
    stop = BeautifulSoup(driver.page_source, 'html.parser').find_all('div', class_='estate-card')
    page = 0
    while True:
        if page>300:
            print("Went over 300 pages, stopping")
            break
        page+=1
        print("url given: ", url_given)
        print("PAGE NUMBER: ",page)
        url_site = str(url_given)+str(page)
        print("site searched: ",url_site)
        driver.get(url_site)
        time.sleep(random.uniform(4,6))
        bsjob = BeautifulSoup(driver.page_source, 'html.parser')
        listings_list = bsjob.find_all('div', class_='estate-card')
        if page!=1 and stop == listings_list:
            print("Page completed")
            break
        for listing in listings_list:
            precio = listing.find('div', class_='estate-card-current-price')
            lista_metraje = listing.find_all('span')
            lugar = listing.find('h4', class_='estate-card-subtitle')
            titulo = listing.find('h3', class_='estate-card-title')
            url = listing.find('a', href=True)
            pattern = re.compile(r"([0-9]+\sm)",re.IGNORECASE)
            metraje = find_value_by_regex_in_a_list(pattern, lista_metraje)
            try:
                precio = precio.text.replace('€', '')
                metraje = metraje.replace('m', '')
            except:
                pass
            data = {'price': precio.strip(), 'size': metraje.strip(), 'location': lugar.text.strip(),'city':city, 'title': titulo.text.strip(), 'url': url['href']}
            if precio is not None and metraje is not None and titulo is not None and url is not None:
                add_to_csv_without_duplicates(dict_data=data)
            else:
                print("No se ha podido añadir")
                print(data)

def call_tecnocasa(headless):
    cities={
        "araba":"https://www.tecnocasa.es/venta/inmuebles/pais-vasco/araba.html/pag-",
        "albacete":"https://www.tecnocasa.es/venta/inmuebles/castilla-la-mancha/albacete.html/pag-",
        "alicante":"https://www.tecnocasa.es/venta/inmuebles/comunidad-valenciana/alicante.html/pag-",
        "almería":"https://www.tecnocasa.es/venta/inmuebles/andalucia/almeria.html/pag-",
        "asturias":"https://www.tecnocasa.es/venta/inmuebles/principado-de-asturias/asturias.html/pag-",
        "ávila":"https://www.tecnocasa.es/venta/inmuebles/castilla-y-leon/avila.html/pag-",
        "badajoz":"https://www.tecnocasa.es/venta/inmuebles/extremadura/badajoz.html/pag-",
        "barcelona":"https://www.tecnocasa.es/venta/inmuebles/cataluna/barcelona.html/pag-",
        "burgos":"https://www.tecnocasa.es/venta/inmuebles/castilla-y-leon/burgos.html/pag-",
        "cáceres":"https://www.tecnocasa.es/venta/inmuebles/extremadura/caceres.html/pag-",
        "cádiz":"https://www.tecnocasa.es/venta/inmuebles/andalucia/cadiz.html/pag-",
        "cantabria":"https://www.tecnocasa.es/venta/inmuebles/cantabria/cantabria.html/pag-",
        "castellon":"https://www.tecnocasa.es/venta/inmuebles/comunidad-valenciana/castellon.html/pag-",
        "ciudad real":"https://www.tecnocasa.es/venta/inmuebles/castilla-la-mancha/ciudad-real.html/pag-",
        "córdoba":"https://www.tecnocasa.es/venta/inmuebles/andalucia/cordoba.html/pag-",
        "la coruña":"https://www.tecnocasa.es/venta/inmuebles/galicia/la-coruna.html/pag-",
        "cuenca":"https://www.tecnocasa.es/venta/inmuebles/castilla-la-mancha/cuenca.html/pag-",
        "gerona":"https://www.tecnocasa.es/venta/inmuebles/cataluna/gerona.html/pag-",
        "granada":"https://www.tecnocasa.es/venta/inmuebles/andalucia/granada.html/pag-",
        "guadalajara":"https://www.tecnocasa.es/venta/inmuebles/castilla-la-mancha/guadalajara.html/pag-",
        "gipuzkoa":"https://www.tecnocasa.es/venta/inmuebles/pais-vasco/gipuzkoa.html/pag-",
        "huelva":"https://www.tecnocasa.es/venta/inmuebles/andalucia/huelva.html/pag-",
        "huesca":"https://www.tecnocasa.es/venta/inmuebles/aragon/huesca.html/pag-",
        "baleares":"https://www.tecnocasa.es/venta/inmuebles/islas-baleares/islas-baleares.html/pag-",
        "jaén":"https://www.tecnocasa.es/venta/inmuebles/andalucia/jaen.html/pag-",
        "león":"https://www.tecnocasa.es/venta/inmuebles/castilla-y-leon/leon.html/pag-",
        "lerida":"https://www.tecnocasa.es/venta/inmuebles/cataluna/lerida.html/pag-",
        "lugo:":"https://www.tecnocasa.es/venta/inmuebles/galicia/lugo.html/pag-",
        "madrid":"https://www.tecnocasa.es/venta/inmuebles/comunidad-de-madrid/madrid.html/pag-",
        "malaga":"https://www.tecnocasa.es/venta/inmuebles/andalucia/malaga.html/pag-",
        "murcia":"https://www.tecnocasa.es/venta/inmuebles/region-de-murcia/murcia.html/pag-",
        "navarra":"https://www.tecnocasa.es/venta/inmuebles/comunidad-foral-de-navarra/navarra.html/pag-",
        "orense":"https://www.tecnocasa.es/venta/inmuebles/galicia/orense.html/pag-",
        "palencia":"https://www.tecnocasa.es/venta/inmuebles/castilla-y-leon/palencia.html/pag-",
        "las palmas":"https://www.tecnocasa.es/venta/inmuebles/canarias/las-palmas.html/pag-",
        "pontevedra":"https://www.tecnocasa.es/venta/inmuebles/galicia/pontevedra.html/pag-",
        "la rioja":"https://www.tecnocasa.es/venta/inmuebles/la-rioja/la-rioja.html/pag-",
        "salamanca":"https://www.tecnocasa.es/venta/inmuebles/castilla-y-leon/salamanca.html/pag-",
        "segovia":"https://www.tecnocasa.es/venta/inmuebles/castilla-y-leon/segovia.html/pag-",
        "sevilla":"https://www.tecnocasa.es/venta/inmuebles/andalucia/sevilla.html/pag-",
        "soria":"https://www.tecnocasa.es/venta/inmuebles/castilla-y-leon/soria.html/pag-",
        "tarragona":"https://www.tecnocasa.es/venta/inmuebles/cataluna/tarragona.html/pag-",
        "santa cruz de tenerife":"https://www.tecnocasa.es/venta/inmuebles/canarias/santa-cruz-de-tenerife.html/pag-",
        "teruel":"https://www.tecnocasa.es/venta/inmuebles/aragon/teruel.html/pag-",
        "toledo":"https://www.tecnocasa.es/venta/inmuebles/castilla-la-mancha/toledo.html/pag-",
        "valencia":"https://www.tecnocasa.es/venta/inmuebles/comunidad-valenciana/valencia/valencia.html/pag-",
        "valladolid":"https://www.tecnocasa.es/venta/inmuebles/castilla-y-leon/valladolid.html/pag-",
        "bizkaia":"https://www.tecnocasa.es/venta/inmuebles/pais-vasco/bizkaia.html/pag-",
        "zamora":"https://www.tecnocasa.es/venta/inmuebles/castilla-y-leon/zamora.html/pag-",
        "zaragoza":"https://www.tecnocasa.es/venta/inmuebles/aragon/zaragoza.html/pag-"
    }
    options = Options()
    chrome_options = Options()
    #options.headless = True
    if headless:
        chrome_options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    cookies_click = True
    for city,url in cities.items():
        try:
            print("Starting tecnocasa with Url: {}".format(url))
            tecnocasa(driver,city,url,cookies_click)
        except Exception as e:
            print("----------------error----------------")
            print(e)
            print("----------------Scraping Error using Url: {}".format(url))
        finally:
            cookies_click = False
    print("Finished tecnocasa")

def find_value_by_regex_in_a_list(pattern, list):
    for item in list:
        match = pattern.match(item.text)
        if match is not None:
            return match.group()
    return None

def add_to_csv_without_duplicates(dict_data,file_name='data/realestate_data_spain.csv'):
    headers = ['price', 'size', 'location', 'city','title', 'url']
    if os.path.exists(file_name):
        pass
    else:
        # Check if alternative path exists
        if os.path.exists('scraper/data'):
            file_name = 'scraper/data/realestate_data_spain.csv'
        if os.path.exists(file_name):
            pass
        else:
        # Create the file and write the header row
            with open(file_name, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(headers)
            print("File created successfully_scraping in progress")
        # Check if the URL is already present in the CSV file
        with open(file_name, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row['url'] == dict_data['url']:
                    return "URL already present"
    
    # Append the data to the CSV file
    with open(file_name, 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writerow(dict_data)
    return "Data added successfully"


call_tecnocasa(True)