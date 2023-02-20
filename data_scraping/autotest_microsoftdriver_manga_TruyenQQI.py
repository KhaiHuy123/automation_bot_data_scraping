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
import sys
website_truyenqqi_page1 = "https://truyenqqhot.com/truyen-moi-cap-nhat/trang-1.html"
website_truyenqqi_page2 = "https://truyenqqhot.com/truyen-moi-cap-nhat/trang-2.html"
website_truyenqqi_page3 = "https://truyenqqhot.com/truyen-moi-cap-nhat/trang-3.html"
website_truyenqqi_page4 = "https://truyenqqhot.com/truyen-moi-cap-nhat/trang-4.html"
website_truyenqqi_page5 = "https://truyenqqhot.com/truyen-moi-cap-nhat/trang-5.html"
website_truyenqqi_page6 = "https://truyenqqhot.com/truyen-moi-cap-nhat/trang-6.html"
website_truyenqqi_page7 = "https://truyenqqhot.com/truyen-moi-cap-nhat/trang-7.html"
website_truyenqqi_page8 = "https://truyenqqhot.com/truyen-moi-cap-nhat/trang-8.html"
website_truyenqqi_page9 = "https://truyenqqhot.com/truyen-moi-cap-nhat/trang-9.html"
website_truyenqqi_page10 = "https://truyenqqhot.com/truyen-moi-cap-nhat/trang-10.html"
list_TruyenQQi = [
    website_truyenqqi_page1, website_truyenqqi_page2, website_truyenqqi_page3, website_truyenqqi_page4,
    website_truyenqqi_page5, website_truyenqqi_page6, website_truyenqqi_page7,
    website_truyenqqi_page8, website_truyenqqi_page9, website_truyenqqi_page10
]
app_path = os.path.dirname(sys.executable)
current_day = datetime.now()
day_month_year = current_day.strftime("%d%m%y")
path = "D:\microsoftdriver_autotest_110\msedgedriver.exe"
service = Service(executable_path=path)
options = webdriver.EdgeOptions()
options.add_argument("--headless")
driver = webdriver.Edge(service=service, options=options)
def scrape_TruyenQQI(website):
    driver.get(website)
    titles, links, lastest_chap_list, conditions, views, follows, discriptions = [], [], [], [], [], [], []
    containers = driver.find_elements(by="xpath", value='''//div[@class="main_content"]/div/div[@class="list_grid_out"]/ul/li''')
    for container in containers:
        title = container.find_element(by="xpath", value='''./div[@class="book_info"]/div/h3/a''').text
        link = container.find_element(by="xpath", value='''./div[@class="book_info"]/div/h3/a''').get_attribute("href")
        latest_chap = container.find_element(by="xpath", value='''./div[@class="book_info"]/div[@class="last_chapter"]/a''').text
        sub_container_invisible = container.find_element(by="xpath", value='''./div[@class="book_info"]/div[@class="more-info"]''')
        driver.execute_script("return arguments[0].removeAttribute('style')", sub_container_invisible)
        condition = container.find_element(by="xpath", value='''./div[@class="book_info"]/div[@class="more-info"]//p[@class="info"][1]''').text
        view = container.find_element(by="xpath", value='''./div[@class="book_info"]/div[@class="more-info"]//p[@class="info"][2]''').text
        follow = container.find_element(by="xpath", value='''./div[@class="book_info"]/div[@class="more-info"]//p[@class="info"][3]''').text
        discription = container.find_element(by="xpath", value='''./div[@class="book_info"]/div[@class="more-info"]//div[@class="excerpt"]''').text
        titles.append(title)
        links.append(link)
        lastest_chap_list.append(latest_chap)
        conditions.append(condition)
        views.append(view)
        follows.append(follow)
        discriptions.append(discription)
    topDay_manga_dict = {"titles": titles, "discripsion": discriptions, "lastest_Chap": lastest_chap_list,
                         "condition": conditions, "view": views, "follow": follows, "link ": links}
    topDay_manga_df = pd.DataFrame(topDay_manga_dict)
    return topDay_manga_df
    pass
def cleaning(df):
    if type(df) == list:
        return df.drop_duplicates()
    return df
    pass
def create_csv_file(df,file_name):
    file = f'{file_name}_manga_{day_month_year}.csv'
    file_export = os.path.join(app_path, file)
    final_df = cleaning(df)
    final_df.to_csv(file_export, header=True, encoding="utf-8", index=False)
    pass
def merge_df(dataframes):
    return pd.concat(dataframes, axis=0)
    pass
def scrape_TruyenQQi_s(list_url):
    list_df = []
    for url in list_url:
        df = scrape_TruyenQQI(url)
        list_df.append(df)
    return list_df
    pass
# Multiple pages version:
if __name__ == '__main__':
    df_TruyenQQI = scrape_TruyenQQi_s(list_TruyenQQi)
    final_dataframe_TruyenQQI = merge_df(df_TruyenQQI)
    create_csv_file(final_dataframe_TruyenQQI, file_name="topDayTruyenQQi")
    driver.quit()

#########################################################################
# Single page version                                                   #
# page1_TruyenQQI = scrape_TruyenQQI(website=website_truyenqqi_page1)   #
#                                                                       #
# create_csv_file(page1_TruyenQQI, file_name="topDayTruyenQQI")         #
#                                                                       #
# driver.quit()                                                         #
#########################################################################
