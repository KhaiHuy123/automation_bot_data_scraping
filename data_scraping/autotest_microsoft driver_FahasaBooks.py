from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import os
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import sys, time
Fahasa_page1 = 'https://www.fahasa.com/sach-trong-nuoc/van-hoc-trong-nuoc/light-novel.html?order=num_orders_month&limit=48&p=1'
Fahasa_page2 = 'https://www.fahasa.com/sach-trong-nuoc/van-hoc-trong-nuoc/light-novel.html?order=num_orders_month&limit=48&p=2'
Fahasa_page3 = 'https://www.fahasa.com/sach-trong-nuoc/van-hoc-trong-nuoc/light-novel.html?order=num_orders_month&limit=48&p=3'
Fahasa_page4 = 'https://www.fahasa.com/sach-trong-nuoc/van-hoc-trong-nuoc/light-novel.html?order=num_orders_month&limit=48&p=4'
Fahasa_page5 = 'https://www.fahasa.com/sach-trong-nuoc/van-hoc-trong-nuoc/light-novel.html?order=num_orders_month&limit=48&p=5'
Fahasa_page6 = 'https://www.fahasa.com/sach-trong-nuoc/van-hoc-trong-nuoc/light-novel.html?order=num_orders_month&limit=48&p=6'
Fahasa_page7 = 'https://www.fahasa.com/sach-trong-nuoc/van-hoc-trong-nuoc/light-novel.html?order=num_orders_month&limit=48&p=7'
Fahasa_page8 = 'https://www.fahasa.com/sach-trong-nuoc/van-hoc-trong-nuoc/light-novel.html?order=num_orders_month&limit=48&p=8'
Fahasa_page9 = 'https://www.fahasa.com/sach-trong-nuoc/van-hoc-trong-nuoc/light-novel.html?order=num_orders_month&limit=48&p=9'
Fahasa_page10 = 'https://www.fahasa.com/sach-trong-nuoc/van-hoc-trong-nuoc/light-novel.html?order=num_orders_month&limit=48&p=10'
Fahasa_page11 = 'https://www.fahasa.com/sach-trong-nuoc/van-hoc-trong-nuoc/light-novel.html?order=num_orders_month&limit=48&p=11'
list_Fahasa = [
    Fahasa_page1, Fahasa_page2, Fahasa_page3, Fahasa_page4,
    Fahasa_page5, Fahasa_page6, Fahasa_page7, Fahasa_page8,
    Fahasa_page9, Fahasa_page10, Fahasa_page11
]
path = "D:\microsoftdriver_autotest_110\msedgedriver.exe"
service = Service(executable_path=path)
options = webdriver.EdgeOptions()
options.add_argument("--headless")
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--disable-setuid-sandbox')
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--disable-browser-side-navigation')
options.add_argument('--disable-gpu-sandbox')
options.add_argument('--disable-accelerated-2d-canvas')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-notifications')
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edge/90.0.864.75")
driver = webdriver.Edge(service=service, options=options)
app_path = os.path.dirname(sys.executable)
current_day = datetime.now()
day_month_year = current_day.strftime("%d%m%y")

def cleaning(df):
    df.drop_duplicates(inplace=True)
    df.drop_duplicates(subset=['price', "discount"], inplace=True)
    return df
    pass
def create_csv_file(df,file_name):
    file = f'{file_name}_Books_{day_month_year}.csv'
    file_export = os.path.join(app_path, file)
    df.to_csv(file_export, header=False, encoding="utf-8", index=False)
    pass
def merge_df(dataframes):
    return pd.concat(dataframes)
    pass
def scrape_Fahasa(website):
    driver.get(website)
    driver.fullscreen_window()
    time.sleep(3)
    driver.set_page_load_timeout(20.0)
    driver.set_script_timeout(20.0)
    for i in range(200):
        driver.execute_script(f"window.scrollTo(0, {str(i)}00);")

    ########################################################################################################################################

    containers_links = driver.find_elements(By.XPATH, '//*[@id="products_grid"]/li/div/div[@class="ma-box-content"]/div[1]/div/a')
    print(len(containers_links))
    links = [container_link.get_attribute("href") for container_link in containers_links]

    ########################################################################################################################################

    containers_name_products = driver.find_elements(By.XPATH, '//*[@id="products_grid"]/li/div/div[@class="ma-box-content"]/h2/a')
    print(len(containers_name_products))
    name_products = [container_name_product.text for container_name_product in containers_name_products]

    ########################################################################################################################################

    containers_official_prices = driver.find_elements(By.XPATH, "//*[@id='products_grid']/li/div/div[@class='ma-box-content']/div[@class='price-label']//*[@class='special-price']")
    print(len(containers_official_prices))
    official_prices = [containers_official_price.text for containers_official_price in containers_official_prices]

    ########################################################################################################################################

    containers_discounts = driver.find_elements(By.XPATH, "//*[@id='products_grid']/li/div/div[@class='label-pro-sale m-label-pro-sale']/span")
    print(len(containers_discounts))
    discounts = [containers_discount.text for containers_discount in containers_discounts]

    ########################################################################################################################################

    containers_images = driver.find_elements(By.XPATH, "//*[@id='products_grid']/li/div/div[@class='ma-box-content']/div[1]/div/a/span/img")
    print(len(containers_images))
    images = [container_image.get_attribute("src") for container_image in containers_images]

    ########################################################################################################################################

    max_len = max(len(links), len(name_products), len(images), len(official_prices), len(discounts))

    links += [float('NaN')] * (max_len - len(links))
    name_products += [float('NaN')] * (max_len - len(name_products))
    images += [float('NaN')] * (max_len - len(images))
    official_prices += [float('NaN')] * (max_len - len(official_prices))
    discounts += [float('NaN')] * (max_len - len(discounts))

    Fahasa_dict = {"name_product": name_products,
               "officail_price": official_prices, "discount": discounts,
               "image": images, "link": links}
    Fahasa_df = pd.DataFrame(Fahasa_dict)
    Fahasa_df['name_product'].fillna('NaN', inplace=True)
    Fahasa_df['discount'].fillna('-0%', inplace=True)
    Fahasa_df['officail_price'].fillna('0', inplace=True)
    return Fahasa_df
    pass
def scrape_Fahasa_s(list_url):
    list_df = []
    for url in list_url:
        df = scrape_Fahasa(url)
        list_df.append(df)
    return list_df
    pass

df_Fahasa = scrape_Fahasa_s(list_Fahasa)
final_dataframe_Fahasa = merge_df(df_Fahasa)
create_csv_file(final_dataframe_Fahasa, file_name="Info_Fahasa")
driver.quit()

# Single page version
# page_Fahasa = scrape_Fahasa(website=Fahasa_page7)
# create_csv_file(page_Fahasa, file_name="Fahasa")
# driver.quit()
