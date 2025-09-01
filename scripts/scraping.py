from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd          

option = webdriver.ChromeOptions()
option.add_argument('--start-maximized')
service = Service(executable_path='D:/Lingga Backup/Coding/Study/New folder/01. Scraping/chromedriver.exe')
driver = webdriver.Chrome(options=option, service=service)

url = 'https://www.tokopedia.com'
driver.get(url)
time.sleep(1)
driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/article/div/div[2]/button').click() # Close Ads
driver.find_element(By.XPATH, '//*[@id="header-main-wrapper"]/div[2]/div[2]/div/div/div/div/input').send_keys('laptop') # Search Product
driver.find_element(By.XPATH, '//*[@id="header-main-wrapper"]/div[2]/div[2]/div/div/div/div/input').send_keys(Keys.ENTER) # Enter Product
time.sleep(3)

element = driver.find_element(By.TAG_NAME, 'body')
last_height = driver.execute_script("return document.body.scrollHeight")
start_time = time.time() 
timeout = 30
load_count = 0 
max_load = 5
while load_count <= max_load:
    element.send_keys(Keys.PAGE_DOWN)
    time.sleep(3)

    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        if time.time() - start_time > timeout:
            driver.find_element(By.XPATH, '//*[@id="zeus-root"]/div/div[2]/div/div[2]/div[4]/div[1]/button/span').click() # Load Button
            load_count += 1
            print(f'Load More... ({load_count})')
    else:
        start_time = time.time()
    
    last_height = new_height

driver.save_screenshot('home.png')
content =  driver.page_source
driver.quit()   

soup = BeautifulSoup(content, 'html.parser')
products_data = []

for item in soup.find_all('div', {'class':'css-5wh65g'}):
    name = item.find('span', {'class':'+tnoqZhn89+NHUA43BpiJg=='})
    price = item.find('div', {'class':'urMOIDHH7I0Iy1Dv2oFaNw=='})
    location = item.find('span', {'class':'gxi+fsEljOjqhjSKqjE+sw== flip'})
    rating = item.find('span', {'class':'_2NfJxPu4JC-55aCJ8bEsyw=='})
    if rating != None:
        rating = rating.get_text()
    sold = item.find('span', {'class':'u6SfjDD2WiBlNW7zHmzRhQ=='})
    if sold != None:
        sold = sold.get_text()

    product_info = {
            'Name': name.get_text(),
            'Price': price.get_text(),
            'Location': location.get_text(),
            'Rating': rating,
            'Sold': sold
        }
    products_data.append(product_info)

df = pd.DataFrame(products_data)
df.to_csv('raw_data.csv', index=False)