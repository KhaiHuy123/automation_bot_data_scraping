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
Tiki_page_1 = 'https://tiki.vn/thoi-trang-nu/c931'
Tiki_page_2 = 'https://tiki.vn/thoi-trang-nu/c931?page=2'
Tiki_page_3 = 'https://tiki.vn/thoi-trang-nu/c931?page=3'
Tiki_page_4 = 'https://tiki.vn/thoi-trang-nu/c931?page=4'
Tiki_page_5 = 'https://tiki.vn/thoi-trang-nu/c931?page=5'
Tiki_page_6 = 'https://tiki.vn/thoi-trang-nu/c931?page=6'
Tiki_page_7 = 'https://tiki.vn/thoi-trang-nu/c931?page=7'
Tiki_page_8 = 'https://tiki.vn/thoi-trang-nu/c931?page=8'
Tiki_page_9 = 'https://tiki.vn/thoi-trang-nu/c931?page=9'
Tiki_page_10 = 'https://tiki.vn/thoi-trang-nu/c931?page=10'

list_tiki = [
    Tiki_page_1, Tiki_page_2, Tiki_page_3, Tiki_page_4,
    Tiki_page_5, Tiki_page_6, Tiki_page_7, Tiki_page_8,
    Tiki_page_9, Tiki_page_10
]
app_path = os.path.dirname(sys.executable)
current_day = datetime.now()
day_month_year = current_day.strftime("%d%m%y")
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
def scrape_Tiki(website):
    driver.get(website)
    driver.fullscreen_window()
    time.sleep(3)
    driver.set_page_load_timeout(20.0)
    driver.set_script_timeout(20.0)
    for i in range(200):
        driver.execute_script(f"window.scrollTo(0, {str(i)}00);")

    ########################################################################################################################################

    containers_links = driver.find_elements(By.XPATH, '//*[@class="product-item"]')
    print(len(containers_links))
    links = [container_link.get_attribute("href") for container_link in containers_links]

    ########################################################################################################################################

    containers_name_products = driver.find_elements(By.XPATH, '//*[@class="product-item"]/div/span/div[@class="info"]/div[1]')
    print(len(containers_name_products))
    name_products = [container_name_product.text for container_name_product in containers_name_products]

    ########################################################################################################################################

    containers_org_prices = driver.find_elements(By.XPATH, "//*[@class='product-item']/div/span/div[@class='info']/div[3]/div[@class='price-discount__price']")
    print(len(containers_org_prices))
    org_prices = [container_org_price.text for container_org_price in containers_org_prices]

    ########################################################################################################################################

    containers_discounts = driver.find_elements(By.CSS_SELECTOR, ".price-discount__discount")
    print(len(containers_discounts))
    discounts = [containers_discount.text for containers_discount in containers_discounts]

    ########################################################################################################################################

    containers_saled_products = driver.find_elements(By.XPATH, "//*[@class='product-item']/div/span/div[@class='info']/div[2]/div[@class='styles__StyledQtySold-sc-732h27-2 fCfYNm']")
    print(len(containers_saled_products))
    saled_products = [container_saled_product.text for container_saled_product in containers_saled_products]

    ########################################################################################################################################

    containers_images = driver.find_elements(By.XPATH, "//*[@class='product-item']/div/span/div/div[@class='image-wrapper']/picture/img")
    print(len(containers_images))
    images = [container_image.get_attribute("src") for container_image in containers_images]

    ########################################################################################################################################

    max_len = max(len(links), len(name_products), len(images), len(org_prices), len(saled_products), len(discounts))

    links += [float('NaN')] * (max_len - len(links))
    name_products += [float('NaN')] * (max_len - len(name_products))
    images += [float('NaN')] * (max_len - len(images))
    org_prices += [float('NaN')] * (max_len - len(org_prices))
    saled_products += [float('NaN')] * (max_len - len(saled_products))
    discounts += [float('NaN')] * (max_len - len(discounts))

    tiki_dict = {"name_product": name_products,
               "price_org": org_prices, "discount": discounts,
               "saled": saled_products, "image": images, "link": links}
    tiki_df = pd.DataFrame(tiki_dict)
    tiki_df['discount'].fillna('-0%', inplace=True)
    tiki_df['saled'].fillna('0', inplace=True)
    return tiki_df
    pass
def scrape_Tiki_s(list_url):
    list_df = []
    for url in list_url:
        df = scrape_Tiki(url)
        list_df.append(df)
    return list_df
    pass
def create_csv_file(df,file_name):
    file = f'{file_name}_female_{day_month_year}.csv'
    file_export = os.path.join(app_path, file)
    df.to_csv(file_export, header=True, encoding="utf-8", index=False)
    pass
def merge_df(dataframes):
    return pd.concat(dataframes, axis=0)
    pass
def cleaning(df):
    if type(df) == list:
        return df.drop_duplicates()
    return df
    pass

if __name__ == '__main__':
    df_Tiki = scrape_Tiki_s(list_tiki)
    final_dataframe_Tiki = merge_df(df_Tiki)
    create_csv_file(final_dataframe_Tiki, file_name="Info_Tiki_Product")
    driver.quit()

# Single page version
# page_Tiki = scrape_Tiki(website=Tiki_page_1)
# create_csv_file(page_Tiki, file_name="Tiki")
# driver.quit()
