from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import time
import csv
import random
from bs4 import BeautifulSoup
import os

#Funciona
def tecnocasa(driver):
    url_site = 'https://www.tecnocasa.es/venta/inmuebles/cataluna/barcelona.html/pag-1'
    driver.get(url_site)
    time.sleep(random.uniform(4,6))
    cookies = driver.find_element(By.XPATH, "/html/body/div[3]/button[1]")
    cookies.click()
    time.sleep(random.uniform(4,6))
    stop = BeautifulSoup(driver.page_source, 'html.parser').find_all('div', class_='estate-card')
    page = 0
    while True:
        page+=1
        url_site = 'https://www.tecnocasa.es/venta/inmuebles/cataluna/barcelona.html/pag-{}'.format(page)
        driver.get(url_site)
        time.sleep(random.uniform(4,6))
        bsjob = BeautifulSoup(driver.page_source, 'html.parser')
        listings_list = bsjob.find_all('div', class_='estate-card')
        if page!=1 and stop == listings_list:
            break
        for listing in listings_list:
            precio = listing.find('div', class_='estate-card-current-price')
            lista_metraje = listing.find_all('span')
            lugar = listing.find('h4', class_='estate-card-subtitle')
            titulo = listing.find('h3', class_='estate-card-title')
            url = listing.find('a', href=True)
            #print("Tecnocasa--------------------------------------")
            #print(precio.text.strip())
            pattern = re.compile(r"([0-9]+\sm)",re.IGNORECASE)
            metraje = find_value_by_regex_in_a_list(pattern, lista_metraje)
            #print(metraje)
            #print(lugar.text.strip())
            #print(titulo.text.strip())
            #print(url['href'])
            #print("------------------------------------------------")
            try:
                precio = precio.text.replace('€', '')
                metraje = metraje.replace('m', '')
            except:
                pass
            data = {'precio': precio.strip(), 'metraje': metraje.strip(), 'lugar': lugar.text.strip(), 'titulo': titulo.text.strip(), 'url': url['href']}
            if precio is not None and metraje is not None and titulo is not None and url is not None:
                add_to_csv_without_duplicates(data)
            else:
                print("No se ha podido añadir")
                print(data)

#Funciona
def servihabitad(driver):
    driver.get("https://www.servihabitat.com/es/venta/vivienda/madrid-areametropolitanamadrid-madrid?lc=madrid-areametropolitanamadrid-madarganzuela_atocha,madrid-areametropolitanamadrid-madcanillejas,madrid-areametropolitanamadrid-madcarabanchel,madrid-areametropolitanamadrid-madcarabanchel_abrantes,madrid-areametropolitanamadrid-madcentro,madrid-areametropolitanamadrid-madchamartin,madrid-areametropolitanamadrid-madchamberi,madrid-areametropolitanamadrid-madciudadlineal,madrid-areametropolitanamadrid-madfuencarral,madrid-areametropolitanamadrid-madhortaleza,madrid-areametropolitanamadrid-madhortaleza_sanchinarro,madrid-areametropolitanamadrid-madlalatina,madrid-areametropolitanamadrid-madlalatina_aguilas,madrid-areametropolitanamadrid-madmoncloa_valdezarza,madrid-areametropolitanamadrid-madpuentedevallecas,madrid-areametropolitanamadrid-madsalamanca,madrid-areametropolitanamadrid-madtetuan,madrid-areametropolitanamadrid-madusera,madrid-areametropolitanamadrid-madvicalvaro,madrid-areametropolitanamadrid-madvilladevallecas,madrid-areametropolitanamadrid-madvillaverde&p=1")
    time.sleep(random.uniform(1,3))
    cookies = driver.find_element(By.XPATH, '//*[@id="p_p_id_servihavitatretailmodalcondiciones_WAR_servihavitatretailmodalcondicionesportlet_"]/div/div/div[1]/div/button[1]')
    cookies.click()
    page = 0
    while True:
        page += 1
        url_site = "https://www.servihabitat.com/es/venta/vivienda/madrid-areametropolitanamadrid-madrid?lc=madrid-areametropolitanamadrid-madarganzuela_atocha,madrid-areametropolitanamadrid-madcanillejas,madrid-areametropolitanamadrid-madcarabanchel,madrid-areametropolitanamadrid-madcarabanchel_abrantes,madrid-areametropolitanamadrid-madcentro,madrid-areametropolitanamadrid-madchamartin,madrid-areametropolitanamadrid-madchamberi,madrid-areametropolitanamadrid-madciudadlineal,madrid-areametropolitanamadrid-madfuencarral,madrid-areametropolitanamadrid-madhortaleza,madrid-areametropolitanamadrid-madhortaleza_sanchinarro,madrid-areametropolitanamadrid-madlalatina,madrid-areametropolitanamadrid-madlalatina_aguilas,madrid-areametropolitanamadrid-madmoncloa_valdezarza,madrid-areametropolitanamadrid-madpuentedevallecas,madrid-areametropolitanamadrid-madsalamanca,madrid-areametropolitanamadrid-madtetuan,madrid-areametropolitanamadrid-madusera,madrid-areametropolitanamadrid-madvicalvaro,madrid-areametropolitanamadrid-madvilladevallecas,madrid-areametropolitanamadrid-madvillaverde&p={}".format(page)
        driver.get(url_site)
        time.sleep(random.uniform(1,3))
        bsjob = BeautifulSoup(driver.page_source, "html.parser")
        if bsjob.find('div',class_="noResults") is not None:
            break
        listings_list = bsjob.find_all('div',class_='flipper')
        for listing in listings_list:
            precio = listing.find('span',class_="price")
            metraje = listing.find('li',class_="features-list-metros")
            lugar = None
            titulo = listing.find('span',class_="text-capitalize")
            url_raw = listing.find('a',class_="features vivienda",onclick=True)
            url = re.search("'(.*)'", url_raw['onclick'])
            url = "https://www.servihabitat.com" + url.group(1)
            #print("-----------------------------------------")
            #print(precio.text.strip())
            #print(metraje.text.strip())
            #print(lugar)
            #print(titulo.text.strip())
            #print(url)
            #print("-----------------------------------------")
            try:
                precio = precio.text.replace('€', '')
                metraje = metraje.text.replace('m2', '')
            except:
                pass
            data = {'precio': precio.strip(), 'metraje': metraje.strip(), 'lugar': lugar, 'titulo': titulo.text.strip(), 'url': url}
            if precio is not None and metraje is not None and titulo is not None and url is not None:
                add_to_csv_without_duplicates(data)
            else:
                print("No se ha podido añadir")
                print(data)
            #Añadir lista y llamar funcion de csv

#Funciona
def solvia(driver):
    driver.get("https://www.solvia.es/es/comprar/viviendas/madrid?numeroPagina=0")
    time.sleep(1)
    cookies = driver.find_element(By.XPATH, '//*[@id="solvia-app"]/solvia-cookies-policy/solvia-simple-modal[1]/div/div/div[2]/a[1]')
    cookies.click()
    page = -1
    while True:
        page += 1
        url_site = "https://www.solvia.es/es/comprar/viviendas/madrid?numeroPagina={}".format(page)
        driver.get(url_site)
        time.sleep(5)
        bsjob = BeautifulSoup(driver.page_source, "html.parser")
        print()
        if bsjob.find('search-not-found') is not None:
            break
        listings_list = bsjob.find_all('div',class_='house-info')
        for listing in listings_list:
            precio = listing.find('span',class_="final-price")
            atributos = listing.find('div',class_='u__pl--0 tags-container border-bottom-grey col-8 col-xs-12 d-flex flex-row align-items-baseline u__pb--sm')
            lista_metraje = atributos.find_all('li')
            #print(lista_metraje)
            pattern = re.compile(r"(\s\d*\.?\d*?\sm)",re.IGNORECASE)
            metraje = find_value_by_regex_in_a_list(pattern, lista_metraje)
            lugar = listing.find('div',class_="build-address")
            titulo = listing.find('h3',class_="build-name")
            url = listing.find('a',href=True)
            try:
                precio = precio.text.replace('€', '')
                try:
                    precio = precio.split(',', 1)[0]
                except:
                    pass
                metraje = metraje.replace('m', '')
                url = "https://www.solvia.es" + url['href']
            except:
                pass
            data = {'precio': precio.strip(), 'metraje': metraje.strip(), 'lugar': lugar.text.strip(), 'titulo': titulo.text.strip(), 'url': url}
            if precio is not None and metraje is not None and titulo is not None and url is not None:
                add_to_csv_without_duplicates(data)
            else:
                print("No se ha podido añadir")
                print(data)

#Funciona
def haya(driver):
    driver.get("https://www.haya.es/bbva/viviendas/madrid/?p=1")
    time.sleep(random.uniform(2,6))
    page = 0
    while True:
        page += 1
        url_site = "https://www.haya.es/bbva/viviendas/madrid/?p={}".format(page)
        driver.get(url_site)
        time.sleep(random.uniform(2,6))
        bsjob = BeautifulSoup(driver.page_source, "html.parser")
        listings_list = bsjob.find_all('div',class_='h-100 d-md-flex flex-column align-items-end')
        if url_site != driver.current_url:
            break
        for listing in listings_list:
            precio = listing.find('strong')
            metraje = listing.find('span',class_="text-20 text-medium")
            lugar = None
            title_and_url_raw = listing.find('a',class_='text-black',title=True,href=True)
            titulo = title_and_url_raw['title']
            url = title_and_url_raw['href']
            #print("------------------------------------")
            #print(precio.text.strip())
            #print(metraje.text.strip())
            #print(lugar)
            #print(titulo)
            #print(url)
            #print("------------------------------------")
            try:
                precio = precio.text.replace('€', '')
                precio = precio.strip()
            except:
                pass
            data = {'precio': precio, 'metraje': metraje.text.strip(), 'lugar': lugar, 'titulo': titulo, 'url': url}
            if precio is not None and metraje is not None and titulo is not None and url is not None and precio != 'consultar precio':
                add_to_csv_without_duplicates(data)
            else:
                print("No se ha podido añadir")
                print(data)

def altamira(driver):
    driver.get("https://www.altamirainmuebles.com/resultados/venta/pisos-y-casas/madrid/40p4167754lm3p7037902z13")
    time.sleep(1)
    cookies = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
    cookies.click()
    while True:
        try:
            ver_mas = driver.find_element(By.XPATH, '//*[@id="verMasSubmit"]')
            ver_mas.click()
            time.sleep(1)
        except:
            print("No hay mas resultados")
            break
    bsjob = BeautifulSoup(driver.page_source, 'html.parser')
    listings_list = bsjob.find_all('div', class_='minificha')
    print("Hay {} resultados".format(len(listings_list)))
    for listing in listings_list:
        lista_precio = listing.find_all('span')
        #print('lista_precio',lista_precio[0].text.strip())
        pattern = re.compile(r"(\d*\.\d*€)",re.IGNORECASE)
        for i in lista_precio:
            match = pattern.match(i.text.strip())
            if match.group() is not None:
                precio = match.group()
                break
        #precio = find_value_by_regex_in_a_list(pattern, lista_precio)
        lista_metraje = listing.find_all('li', class_='superf')
        pattern = re.compile(r"(\d*\.?\d*?)",re.IGNORECASE)
        for i in lista_metraje:
            match = pattern.match(i.text.strip())
            if match.group() is not None:
                metraje = match.group()
                break
        lugar = None
        title = listing.find('h2')
        titulo_and_url = title.find('a',href=True)
        titulo = titulo_and_url.text.strip()
        url = 'https://www.altamirainmuebles.com'+titulo_and_url['href']
        try:
            precio = precio.replace('€', '')
            precio = precio.strip()
            metraje = metraje.strip()
        except:
            pass

        data = {'precio': precio, 'metraje': metraje, 'lugar': lugar, 'titulo': titulo, 'url': url}
        if precio is not None and metraje is not None and titulo is not None and url is not None:
            add_to_csv_without_duplicates(data)
        else:
            print("No se ha podido añadir")
            print(data)

#Problemas de deteccion de bot, aveces funciona, aveces no
def idealista(driver):
    driver.get("https://www.idealista.com/venta-viviendas/madrid-provincia/pagina-1.htm")
    time.sleep(random.uniform(2,3))
    cookies = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/button[2]')
    cookies.click()
    time.sleep(random.uniform(5,8))
    page = 1
    while True:
        page += 1
        url_site = "https://www.idealista.com/venta-viviendas/madrid-provincia/pagina-{}.htm".format(page)
        time.sleep(random.uniform(5,8))
        bsjob = BeautifulSoup(driver.page_source, "html.parser")
        listings_list = bsjob.find_all('div',class_='item-info-container')
        check = bsjob.find('div',id_='captcha-box')
        if check is None:
            print("Bot Detectado")
            break
        for listing in listings_list:
            precio = listing.find('span',class_="item-price h2-simulated")
            metraje = listing.find('span',class_="item-detail")
            lugar = None
            titulo_and_url = listing.find('a',class_="item-link",href=True)
            titulo = titulo_and_url.text.strip()
            url = 'https://www.idealista.com' + titulo_and_url['href']
            try:
                precio = precio.text.replace('€', '')
                precio = precio.strip()
                metraje = metraje.text.replace('m²', '')
                metraje = metraje.strip()
            except:
                pass
            data = {'precio': precio, 'metraje': metraje, 'lugar': lugar, 'titulo': titulo, 'url': url}
            if precio is not None and metraje is not None and titulo is not None and url is not None:
                add_to_csv_without_duplicates(data)
            else:
                print("No se ha podido añadir")
                print(data)
        driver.get(url_site)
            
#Problemas de deteccion de bot, aveces funciona, aveces no
def fotocasa(driver):
    driver.get("https://www.fotocasa.es/es/comprar/viviendas/madrid-provincia/todas-las-zonas/l/1")
    time.sleep(random.uniform(1,5))
    cookies = driver.find_element(By.XPATH, '//*[@id="App"]/div[2]/div/div/div/footer/div/button[2]')
    cookies.click()
    time.sleep(random.uniform(5,8))
    page = 1
    while True:
        page += 1
        time.sleep(random.uniform(5,8))
        bsjob = BeautifulSoup(driver.page_source, "html.parser")
        listings_list = bsjob.find_all('div',class_='re-CardPackPremium-info')
        check = bsjob.find('div',id_='captcha-box')
        if check is None:
            print("Bot Detectado")
            break
        for listing in listings_list:
            precio = listing.find('span',class_="re-CardPrice")
            metraje = listing.find('span',class_="re-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--surface")
            lugar = None
            titulo = listing.find('span',class_="re-CardTitle re-CardTitle--big")
            url = listing.find('a',class_="re-CardPackPremium-info-container",href=True)
            try:
                precio = precio.text.replace('€', '')
                precio = precio.strip()
                metraje = metraje.text.replace('m²', '')
                metraje = metraje.strip()
            except:
                pass
            data = {'precio': precio, 'metraje': metraje, 'lugar': lugar, 'titulo': titulo.text.strip(), 'url': url['href']}
            if precio is not None and metraje is not None and titulo is not None and url is not None:
                add_to_csv_without_duplicates(data)
            else:
                print("No se ha podido añadir")
                print(data)
        url_site = 'https://www.fotocasa.es/es/comprar/viviendas/madrid-provincia/todas-las-zonas/l/{}'.format(page)
        driver.get(url_site)

def call_all_barcelona():

    options = Options()
    chrome_options = Options()
    options.headless = True
    chrome_options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    try:
        print("Iniciando tecnocasa")
        tecnocasa(driver)
    except:
        print("Error en tecnocasa")
    print("---Terminado---")

def find_value_by_regex_in_a_list(pattern, list):
    for item in list:
        match = pattern.match(item.text)
        if match is not None:
            return match.group()
    return None

def add_to_csv_without_duplicates(dict_data,file_name='data/realestate_data_barcelona.csv'):
    headers = ['precio', 'metraje', 'lugar', 'titulo', 'url']
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

#Todo misc after this point--------------------------------------------------------------



call_all_barcelona()