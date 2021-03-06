from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math
import pickle
import os

# check cache
useCache = 'n'
if (os.path.isfile('data/scrap-result.pickle')) :
    useCache = input('use last scraping data? (y/n) : ')

if (useCache == 'n') :
    # input
    location = input('specified location : ')
    search = input('specified keywords (rumah subsidi/tanah) : ')
    maxBudget = input('your maximum budget : ')
    nextPage = input('next page : ')

    # initiate webdriver
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 5) 

    # go to olx
    driver.get("https://www.olx.co.id/")

    # set location
    searchLocationBox = driver.find_element_by_xpath('//*[@id="container"]/header/div/div/div[2]/div/div/div[1]/div/div[1]/input')
    searchLocationBox.click()
    searchLocationBox.send_keys(location)
    selectLocation = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="container"]/header/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[1]')
        )
    )
    selectLocation.click()

    # set search box
    searchBox = driver.find_element_by_xpath('//*[@id="container"]/header/div/div/div[2]/div/div/div[2]/div/form/fieldset/div/input')
    searchBox.send_keys(search)
    selectSpecificSearch =  wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="container"]/header/div/div/div[2]/div/div/div[2]/div/form/ul/li[1]')
        )
    )

    if "Apakah maksud anda" in selectSpecificSearch.text :
        selectSpecificSearch = driver.find_element_by_xpath('//*[@id="container"]/header/div/div/div[2]/div/div/div[2]/div/form/ul/li[2]')
        
    selectSpecificSearch.click()

    # set filter
    # cari yang dijual
    try :
        filterTipe = wait.until(
            EC.presence_of_element_located(
                (By.ID, 'typedijual')
            )
        )
        filterTipe.click()
    except :
        print("filter type dijual not found")

    # sertifikasi shm
    try :
        sertifikasiSHM = wait.until(
            EC.presence_of_element_located(
                (By.ID, 'p_certificateshm-sertifikathakmilik')
            )
        )
        sertifikasiSHM.click()
    except :
        print("filter shm not found")

    # budget max 0 - 160000000
    hargaMin = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="container"]/main/div/section/div/div/div[4]/div[1]/div/div[4]/div[1]/div[2]/div/input[1]')
        )
    )
    hargaMin.send_keys("0")
    hargaMax = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="container"]/main/div/section/div/div/div[4]/div[1]/div/div[4]/div[1]/div[2]/div/input[2]')
        )
    )
    hargaMax.send_keys(maxBudget)
    buttonHarga = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="container"]/main/div/section/div/div/div[4]/div[1]/div/div[4]/div[1]/div[2]/div/a')
        )
    )
    filteredUrl = buttonHarga.get_attribute("href")

    # go to filtered url
    driver.get(filteredUrl)

    # load more item x times
    if (nextPage == '') :
        xmax = 0
    else :
        xmax = int(nextPage)

    try :
        loadMoreButton = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="container"]/main/div/section/div/div/div[4]/div[2]/div/div[3]/button')
            )
        )
        x = 0
        while x < xmax :
            try :
                loadMoreButton.click()
                x += 1
                driver.implicitly_wait(1)
            except :
                break
    except :
        print("load more button not shown")

    # extracting item
    # get item link
    items = []
    for item in driver.find_elements_by_class_name("EIR5N") :
        link = item.find_element_by_tag_name("a").get_attribute("href")
        items.append(link)

    def sanitizePrice(val) :
        val = val.replace("Rp ", "")
        val = val.replace(".", "")
        return int(val)

    # loop item link, grab data
    result = []
    for item in items :
        description = ''
        location = ''
        pricePerM2 = 0
        price = 0
        luasM2 = 0

        driver.get(item)
        try :
            descriptionEl = driver.find_element_by_xpath('//*[@id="container"]/main/div/div/div/div[5]/div[1]/div/section/h1')
            if descriptionEl :
                description = descriptionEl.text
        except :
            print('description element not found')
        
        try :
            priceEl = driver.find_element_by_xpath('//*[@id="container"]/main/div/div/div/div[5]/div[1]/div/section/span')
            if priceEl :
                price = priceEl.text
                price = sanitizePrice(price)
        except :
            print('price element not found')

        try :
            luasM2El = driver.find_element_by_css_selector('span[data-aut-id="value_p_sqr_land"')
            if luasM2El : 
                luasM2 = int(luasM2El.text)
        except :
            print('luas element not found')

        try :
            locationEl = driver.find_element_by_css_selector('span[data-aut-id="value_p_alamat"')
            if locationEl :
                location = locationEl.text
        except :
            print('location element not found')

        if(price < 15000000) :
            pricePerM2 = price
            price = pricePerM2 * luasM2
        else :
            try :
                pricePerM2 = price/luasM2
            except :
                pricePerM2 = 0

        result.append({
            'link': item,
            'description': description,
            'price': price,
            'price_per_m2': math.ceil(pricePerM2),
            'luas_m2': luasM2,
            'location': location
        })

    # cache result to pickle
    with open ('data/scrap-result.pickle', 'wb') as f :
        pickle.dump(result, f)
    print("success scraping " + str(len(result)) + " items")

    # quit driver
    driver.quit()
else :
    with open ('data/scrap-result.pickle', 'rb') as f :
        result = pickle.load(f)

# show result
print("urut berdasarkan : ")
print("1. Tanah terluas")
print("2. Harga per m2 termurah")
print("3. Terluas & termurah (terluas dengan harga m2 termurah)")
sortBy = input('1/2/3 : ')

limitResult = input('limit result? (default not limited) ')
if (limitResult == '') :
    limitResult = len(result)
else :
    if (int(limitResult) > len(result)) :
        limitResult = len(result)
    else :
        limitResult = int(limitResult)

if (sortBy == '1') :
    result.sort(key=lambda x: x.get('luas_m2'), reverse=True)
elif (sortBy == '2'):
    result.sort(key=lambda x: x.get('price_per_m2'))
else :
    result.sort(key=lambda x: x.get('luas_m2'), reverse=True)
    result[0:limitResult - 1]
    result.sort(key=lambda x: x.get('price_per_m2'))

i = 0
while i < limitResult :
    print('description : ' + result[i]['description'])
    print('price per m2 : Rp' + str(f"{result[i]['price_per_m2'] : ,}"))
    print('luas : ' + str(result[i]['luas_m2']) + " m2")
    print('total price : Rp' + str(f"{result[i]['price'] : ,}"))
    print('location : ' + result[i]['location'])
    print('link : ' + result[i]['link'])
    print('')
    i += 1