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
        print("")

    # sertifikasi shm
    sertifikasiSHM = wait.until(
        EC.presence_of_element_located(
            (By.ID, 'p_certificateshm-sertifikathakmilik')
        )
    )
    sertifikasiSHM.click()

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
        driver.get(item)
        description = driver.find_element_by_xpath('//*[@id="container"]/main/div/div/div/div[5]/div[1]/div/section/h1').text
        pricePerM2 = 0
        price = driver.find_element_by_xpath('//*[@id="container"]/main/div/div/div/div[5]/div[1]/div/section/span').text
        price = sanitizePrice(price)
        luasM2 = driver.find_element_by_xpath('//*[@id="container"]/main/div/div/div/div[4]/section[1]/div/div/div[1]/div/div[2]/div/span[2]').text
        luasM2 = int(luasM2)
        if(price < 15000000) :
            pricePerM2 = price
            price = pricePerM2 * luasM2
        else :
            pricePerM2 = price/luasM2

        result.append({
            'link': item,
            'description': description,
            'price': price,
            'price_per_m2': math.ceil(pricePerM2),
            'luas_m2': luasM2
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

if (sortBy == '1') :
    result.sort(key=lambda x: x.get('luas_m2'), reverse=True)
elif (sortBy == '2'):
    result.sort(key=lambda x: x.get('price_per_m2'))
else :
    result.sort(key=lambda x: x.get('luas_m2'), reverse=True)
    result[0:9]
    result.sort(key=lambda x: x.get('price_per_m2'))

i = 0
while i < 10 :
    print('description : ' + result[i]['description'])
    print('price per m2 : Rp' + str(result[i]['price_per_m2']))
    print('luas : ' + str(result[i]['luas_m2']) + " m2")
    print('total price : Rp' + str(result[i]['price']))
    print('link : ' + result[i]['link'])
    print('')
    i += 1