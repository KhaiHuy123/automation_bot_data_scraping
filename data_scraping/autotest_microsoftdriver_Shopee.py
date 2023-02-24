from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import os
from datetime import datetime
import sys, time
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
def is_element_stale(element):
    try:
        # Check if the element is still present in the DOM
        element.is_enabled()
        return False
    except StaleElementReferenceException:
        return True
def check_element_version(driver, element):
    wait = WebDriverWait(driver, 10)
    try:
        # Wait for the element to become present in the DOM
        wait.until(EC.staleness_of(element))
        return False
    except:
        return True
def check_stale(element, driver,value):
    if  check_element_version(driver, element):
        driver.refresh()
    element = driver.find_elements(by='xpath', value=value)
    return True
def cleaning(df):
    df.drop_duplicates(inplace=True)
    df.drop_duplicates(subset=['price', "discount"], inplace=True)
    return df
    pass
def create_csv_file(df,file_name):
    file = f'{file_name}_female_{day_month_year}.csv'
    file_export = os.path.join(app_path, file)
    df.to_csv(file_export, header=False, encoding="utf-8", index=False)
    pass
def merge_df(dataframes):
    return pd.concat(dataframes)
    pass
def read_file(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            data.append(line.strip())
    return data
'''OK VERSION BELOW'''
def scrape_Shopee(website):
    driver.get(website)
    driver.fullscreen_window()
    time.sleep(3)
    driver.set_page_load_timeout(20.0)
    driver.set_script_timeout(20.0)
    for i in range(300):
        driver.execute_script(f"window.scrollTo(0, {str(i)}00);")

    ########################################################################################################################################

    containers_links = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[4]/div[2]/div/div[2]/div/a')
    print(len(containers_links))
    links = [container_link.get_attribute("href") for container_link in containers_links]

    ########################################################################################################################################

    containers_name_products = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div[4]/div[2]/div/div[2]/div/a/div/div/div[2]/div[1]/div/div[@class='_1yN94N WoKSjC _2KkMCe']")
    print(len(containers_name_products))
    name_products = [container_name_product.text for container_name_product in containers_name_products]

    ########################################################################################################################################

    containers_org_prices = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div[4]/div[2]/div/div[2]/div/a/div/div/div[2]/div[2]/div[1]")
    print(len(containers_org_prices))
    org_prices = [container_org_price.text for container_org_price in containers_org_prices]

    ########################################################################################################################################

    containers_saled_products = driver.find_elements(By.CSS_SELECTOR, '.tysB0L')
    print(len(containers_saled_products))
    saled_products = [container_saled_product.text for container_saled_product in containers_saled_products]

    ########################################################################################################################################

    containers_locations = driver.find_elements(By.CSS_SELECTOR, ".mrz-bA  ")
    print(len(containers_locations))
    locations = [container_location.text for container_location in containers_locations]

    ########################################################################################################################################

    max_len = max(len(links), len(name_products), len(locations), len(saled_products), len(org_prices))

    links += [float('NaN')] * (max_len - len(links))
    name_products += [float('NaN')] * (max_len - len(name_products))
    locations += [float('NaN')] * (max_len - len(locations))
    saled_products += [float('NaN')] * (max_len - len(saled_products))
    org_prices += [float('NaN')] * (max_len - len(org_prices))
    shopee_dict = {"name_product": name_products,
               "price_org": org_prices,
               "saled": saled_products, "location": locations, "link": links}
    shopee_df = pd.DataFrame(shopee_dict)
    shopee_df['saled'].fillna('0', inplace=True)
    shopee_df['location'].fillna('unknown', inplace=True)
    return shopee_df
    pass
'''OK VERSION BELOW'''
# def scrape_Shopee(website):
#     driver.get(website)
#     time.sleep(3)
#     html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
#     soup = BeautifulSoup(html, "html.parser")
#     #soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
#     containers_links = soup.find_all(xpath_='/html/body/div[1]/div/div[2]/div/div/div[4]/div[2]/div/div[2]/div/a')
#     print(len(containers_links))
#     links = [container_link.get_attribute("href") for container_link in containers_links]
#
#     containers_name_products = soup.find_all(xpath="/html/body/div[1]/div/div[2]/div/div/div[4]/div[2]/div/div[2]/div/a/div/div/div[2]/div[1]/div/div[@class='_1yN94N WoKSjC _2KkMCe']")
#     print(len(containers_name_products))
#     name_products = [container_name_product.text for container_name_product in containers_name_products]
#
#     containers_discount = soup.find_all("div", class_="sWDsGo")
#     print(len(containers_discount))
#     discount = [container_discount.text for container_discount in containers_discount]
#
#     containers_org_prices = soup.find_all(xpath= "/html/body/div[1]/div/div[2]/div/div/div[4]/div[2]/div/div[2]/div/a/div/div/div[2]/div[2]/div[1]")
#     print(len(containers_org_prices))
#     org_prices = [container_org_price.text for container_org_price in containers_org_prices]
#
#     containers_saled_products = soup.find_all('div', class_='x+3B8m wOebCz')
#     print(len(containers_saled_products))
#     saled_products = [container_saled_product.text for container_saled_product in containers_saled_products]
#
#     containers_locations = soup.find_all('div', class_="mrz-bA")
#     print(len(containers_locations))
#     locations = [container_location.text for container_location in containers_locations]
#
#     shopee_dict = {"name_product": name_products, "discount": discount,
#                "price_org": org_prices,
#                "saled": saled_products, "location": locations, "link": links}
#     shopee_df = pd.DataFrame(shopee_dict)
#     return shopee_df
#     pass
def scrape_Shopee_s(list_url):
    list_df = []
    for url in list_url:
        df = scrape_Shopee(url)
        list_df.append(df)
    return list_df
    pass
'''OK VERSION BELOW'''
# def scrape_Shopee(website):
#     driver.get(website)
#     driver.maximize_window()
#     time.sleep(3)
#
#     containers_links = driver.find_elements(By.XPATH, '//*[@class="col-xs-2-4 shopee-search-item-result__item"]/a')
#     print(len(containers_links))
#     links = [container_link.get_attribute("href") for container_link in containers_links]
#
#     containers_name_products = driver.find_elements(By.XPATH, "//*[@class='_1yN94N WoKSjC _2KkMCe']")
#     print(len(containers_name_products))
#     name_products = [container_name_product.text for container_name_product in containers_name_products]
#
#     containers_org_prices = driver.find_elements(By.XPATH, "//*[@class='AQ4KLF']")
#     print(len(containers_org_prices))
#     org_prices = [container_org_price.text for container_org_price in containers_org_prices]
#
#     containers_saled_products = driver.find_elements(By.CSS_SELECTOR, '.tysB0L')
#     print(len(containers_saled_products))
#     saled_products = [container_saled_product.text for container_saled_product in containers_saled_products]
#
#     containers_locations = driver.find_elements(By.CSS_SELECTOR, ".mrz-bA  ")
#     print(len(containers_locations))
#     locations = [container_location.text for container_location in containers_locations]
#
#     shopee_dict = {"name_product": name_products,
#                "price_org": org_prices,
#                "saled": saled_products, "location": locations, "link": links}
#     shopee_df = pd.DataFrame.from_dict(shopee_dict)
#     shopee_df.fillna('0', inplace=True)
#     return shopee_df
#     pass
''''''
list_Shopee = read_file("shopee_product_female.txt")
if __name__ == '__main__':
    df_Shopee = scrape_Shopee_s(list_Shopee)
    final_dataframe_Shopee = merge_df(df_Shopee)
    create_csv_file(final_dataframe_Shopee, file_name="Info_Shopee_Product")
    driver.quit()

# Single page version
# page_shopee = scrape_Shopee(website=Shopee_page7)
# create_csv_file(page_shopee, file_name="shopee")
# driver.quit()
''''''
