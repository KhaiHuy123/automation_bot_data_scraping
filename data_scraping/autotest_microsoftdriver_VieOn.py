import time
import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium_stealth import stealth
import pandas as pd
import os, random
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
app_path = os.path.dirname(sys.executable)
current_day = datetime.now()
day_month_year = current_day.strftime("%d%m%y")
path = "msedgedriver.exe"
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

VieOn_website_1 = "https://vieon.vn/"
VieOn_Website_2 = "https://vieon.vn/phim-bo/"

list_VieOn = [
    VieOn_website_1, VieOn_Website_2
]
driver = webdriver.Edge(service=service, options=options)

def create_csv_file(df,file_name):
    file = f'{file_name}_films_{day_month_year}.csv'
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
# def scrape_VieOn(website):
#     driver.get(website)
#     driver.set_page_load_timeout(10.0)
#     driver.set_script_timeout(10.0)
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#
#     #containers = driver.find_elements(by="xpath", value='//*[@class="swiper-slide slider__item"]')
#
#     containers_images = driver.find_elements(By.XPATH, '//*[@class="swiper-slide slider__item"]/div/div/a/span/img')
#     images = [container_image.get_attribute("src") for container_image in containers_images]
#
#     containers_titles = driver.find_elements(By.XPATH, '//*[@class="swiper-slide slider__item"]/div/div/a')
#     titles = [containers_title.get_attribute("title")for containers_title in containers_titles]
#
#     containers_links = driver.find_elements(By.XPATH, '//*[@class="swiper-slide slider__item"]/div/div[2]/div/h3/a')
#     links = [container_link.get_attribute("href") for container_link in containers_links]
#
#     containers_discriptions = driver.find_elements(By.XPATH, '//*[@class="swiper-slide slider__item"]/div/div[2]/div/div')
#     discriptions = [container_discription.text for container_discription in containers_discriptions]
#     #
#     # print(len(containers))
#     print(len(images))
#     print(len(titles))
#     print(len(discriptions))
#     print(len(links))
#     # print(titles)
#     # print(images)
#     # print(links)
#     # print(discriptions)
#     vieon_dict = {"titles": titles, "discripsion": discriptions, "image": images,
#                   "link ": links}
#     vion_df = pd.DataFrame.from_dict(vieon_dict, orient="columns")
#     vion_df.fillna("unknown")
#     return vion_df
def scrape_VieOn_s(list_url):
    list_df = []
    for url in list_url:
        df = scrape_VieOn(url)
        list_df.append(df)
    return list_df
    pass
def scrape_VieOn(website):
    driver.get(website)
    driver.fullscreen_window()
    time.sleep(3)
    for i in range(200):
        driver.execute_script(f"window.scrollTo(0, {str(i)}00);")
    #wait = WebDriverWait(driver, 10)
    driver.set_page_load_timeout(20)
    driver.set_script_timeout(20)
    #page_height = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # containers = driver.find_elements(by="xpath", value='//*[@class="swiper-slide slider__item"]')

    #wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="swiper-slide slider__item"]/div/div/a')))
    # containers_images = driver.find_elements(By.XPATH, '//*[@class="swiper-slide slider__item"]/div/div/a/span/img')
    # images = [container_image.get_attribute("src") for container_image in containers_images]

    #wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="swiper-slide slider__item"]/div/div/a')))
    # containers_titles = driver.find_elements(By.XPATH, '//*[@class="swiper-slide slider__item"]/div/div/a/span/img')
    # titles = [containers_title.get_attribute("title") for containers_title in containers_titles]

    #wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="swiper-slide slider__item"]/div/div[2]/div')))
    containers_links = driver.find_elements(By.XPATH, '//*[@class="swiper-slide slider__item"]/div/div[@class="card__section absolute right bottom left"]/div/h3/a')
    links = [container_link.get_attribute("href") for container_link in containers_links]

    #wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="swiper-slide slider__item"]/div/div[2]/div/div')))
    # containers_discriptions = driver.find_elements(By.XPATH, '//*[@class="swiper-slide slider__item"]/div/div[@class="card__section absolute right bottom left"]/div/div')
    # discriptions = [container_discription.text for container_discription in containers_discriptions]

    # print(len(containers))
    # print(len(images))
    # print(len(titles))
    # print(len(discriptions))
    print(len(links))

    # max_len = max(len(links), len(images), len(titles), len(discriptions))
    # links += [float('NaN')] * (max_len - len(links))
    # titles += [float('NaN')] * (max_len - len(titles))
    # images += [float('NaN')] * (max_len - len(images))
    # discriptions += [float('NaN')] * (max_len - len(discriptions))
    vieon_dict = {"link ": links}
    vion_df = pd.DataFrame.from_dict(vieon_dict, orient="columns")
    vion_df.fillna("NaN", inplace=True)
    return vion_df
df_VieOn = scrape_VieOn_s(list_VieOn)
final_dataframe_VieOn = merge_df(df_VieOn)
create_csv_file(final_dataframe_VieOn, file_name="VieOn")
driver.quit()

# page_VieOn = scrape_VieOn(website=VieOn_website_1)
# create_csv_file(page_VieOn, file_name="VieOn")
# driver.quit()
