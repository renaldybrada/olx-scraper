# Requirements
1. Python 3.*
2. [Selenium Python](https://selenium-python.readthedocs.io/installation.html)
3. Browser driver. [check this out](https://selenium-python.readthedocs.io/installation.html#drivers) for installation
4. Virtualenv (recommended, but not mandatory)

# Installation
1. Install python 3.* for your OS. Check in your terminal by typing 
```sh
$ python --version
```

2. [Install browser driver](https://selenium-python.readthedocs.io/installation.html#drivers). Make sure to make it global by registering to PATH. Then restart your terminal. Check if the installation is okay by typing chromedriver for chrome user, or geckodriver for firefox user
```sh
$ chromedriver
```
it should show something like this
```sh
Starting ChromeDriver blablabla on port 9515
Only local connections are allowed.
Please see https://chromedriver.chromium.org/security-considerations for suggestions on keeping ChromeDriver safe.
ChromeDriver was started successfully.
```

3. Install global virtualenv. Skip if you have installed it
```sh
$ pip install virtualenv
```

4. Clone this repository, then cd
```sh
$ git clone https://github.com/renaldybrada/olx-scraper.git olx-scraper
$ cd olx-scraper
```

5. Create virtualenv
```sh
$ python -m virtualenv venv
```

6. Activate virtualenv and install requirements
```sh
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

## Getting started
1. Simply typing
```sh
$ python src\olx-property.py
```
2. Input as you like<br>
![olx-scraper-input](https://user-images.githubusercontent.com/45556134/87877290-a29cfa80-ca07-11ea-8a8a-c74677baf144.PNG)<br>
**note : next page are loop through search result page. Leave it empty first for testing**

3. It takes several minutes to completed. You can view the browser operated automatically for scraping

4. When scraping is completed, you can choose to sort that data<br>
![olx-scraper-sort](https://user-images.githubusercontent.com/45556134/87877461-aa10d380-ca08-11ea-9769-e08c2a033b0e.PNG)

5. And the result is something like this<br>
![olx-scraper-result](https://user-images.githubusercontent.com/45556134/87877718-14764380-ca0a-11ea-9597-1869e2be2f22.PNG)


6. When you restart the process, you will prompted to use your last search data or not<br>
![olx-scraper-use-last-data](https://user-images.githubusercontent.com/45556134/87877544-2d322980-ca09-11ea-877a-5bd69d5c97a4.PNG)<br>
choose **y** if you want to use last data, or **n** if you want to scrap new data
