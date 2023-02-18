from selenium import webdriver
from selenium.webdriver.edge.service import Service
import pandas as pd
import os
from datetime import datetime
import sys

women_TheSun_Website_page1 = "https://www.thesun.co.uk/health/womens-health/"
women_TheSun_Website_page2 = "https://www.thesun.co.uk/health/womens-health/page/2/"
women_TheSun_Website_page3 = "https://www.thesun.co.uk/health/womens-health/page/3/"
women_TheSun_Website_page4 = "https://www.thesun.co.uk/health/womens-health/page/4/"
women_TheSun_Website_page5 = "https://www.thesun.co.uk/health/womens-health/page/5/"
men_TheSun_Website_page1 = "https://www.thesun.co.uk/health/mens-health-and-fitness/"
men_TheSun_Website_page2 = "https://www.thesun.co.uk/health/mens-health-and-fitness/page/2/"
men_TheSun_Website_page3 = "https://www.thesun.co.uk/health/mens-health-and-fitness/page/3/"
men_TheSun_Website_page4 = "https://www.thesun.co.uk/health/mens-health-and-fitness/page/4/"
men_TheSun_Website_page5 = "https://www.thesun.co.uk/health/mens-health-and-fitness/page/5/"
worldnews_TheSun_Website_page1 = "https://www.thesun.co.uk/news/worldnews/"
worldnews_TheSun_Website_page2 = "https://www.thesun.co.uk/news/worldnews/page/2/"
worldnews_TheSun_Website_page3 = "https://www.thesun.co.uk/news/worldnews/page/3/"
worldnews_TheSun_Website_page4 = "https://www.thesun.co.uk/news/worldnews/page/4/"
worldnews_TheSun_Website_page5 = "https://www.thesun.co.uk/news/worldnews/page/5/"
list_women_heath = [
    women_TheSun_Website_page1, women_TheSun_Website_page2,
    women_TheSun_Website_page3, women_TheSun_Website_page4, women_TheSun_Website_page5
]
list_men_heath = [
    men_TheSun_Website_page1, men_TheSun_Website_page2,
    men_TheSun_Website_page3, men_TheSun_Website_page4, men_TheSun_Website_page5
]
list_world_news = [
    worldnews_TheSun_Website_page1, worldnews_TheSun_Website_page2,
    worldnews_TheSun_Website_page3, worldnews_TheSun_Website_page4, worldnews_TheSun_Website_page5
]
path = "D:\microsoftdriver_autotest_110\msedgedriver.exe"
service = Service(executable_path=path)
options = webdriver.EdgeOptions()
options.add_argument("--headless")
driver = webdriver.Edge(service=service, options=options)
app_path = os.path.dirname(sys.executable)
current_day = datetime.now()
day_month_year = current_day.strftime("%d%m%y")

def merge_df(dataframes):
    return pd.concat(dataframes, axis=0)
    pass
def cleaning(df):
    if type(df) == list:
        return df.drop_duplicates()
    return df
    pass
def create_csv_file(df,file_name):
    file = f'{file_name}_{day_month_year}.csv'
    file_export = os.path.join(app_path, file)
    final_df = cleaning(df)
    final_df.to_csv(file_export, header=True, encoding="utf-8", index=False)
    pass
def scrape_Women_Heath(website):
    driver.get(website)
    links = []
    titles = []
    discriptions = []
    illutrations = []
    containers = driver.find_elements(by="xpath",
                                      value='//div/div/div/div[@id="main-content"]/section/div[@class="sun-row teaser teaser--main"]'
                                            '/div[@class="col sun-col-2"]')
    for contain in containers:
        link = contain.find_element(by="xpath", value='./div/div[@class="teaser__copy-container"]/a').get_attribute("href")
        title = contain.find_element(by="xpath", value='./div/div[@class="teaser__copy-container"]/a/h3').text
        discription = contain.find_element(by="xpath", value='./div/div[@class="teaser__copy-container"]/a/p').text
        illutration = contain.find_element(by="xpath", value='./div/div[@class="teaser__image-container"]/a/picture/img').get_attribute("data-src")
        links.append(link)
        titles.append(title)
        discriptions.append(discription)
        illutrations.append(illutration)
    women_healh_dict = {"title": titles, "discription": discriptions,
                        "illutration": illutrations, "link": links}
    women_heath_df = pd.DataFrame(women_healh_dict)
    return women_heath_df
    pass
def scrape_Men_Heath(website):
    driver.get(website)
    links = []
    titles = []
    discriptions = []
    illutrations = []
    containers = driver.find_elements(by="xpath", value='//div/div/div/div[@id="main-content"]/section/div[@class="sun-row teaser teaser--main"]/div[@class="col sun-col-2"]')
    for contain in containers:
        link = contain.find_element(by="xpath", value='./div/div[@class="teaser__copy-container"]/a').get_attribute("href")
        title = contain.find_element(by="xpath", value='./div/div[@class="teaser__copy-container"]/a/h3').text
        discription = contain.find_element(by="xpath", value='./div/div[@class="teaser__copy-container"]/a/p').text
        illutration = contain.find_element(by="xpath", value='./div/div[@class="teaser__image-container"]/a/picture/img').get_attribute("data-src")
        links.append(link)
        titles.append(title)
        discriptions.append(discription)
        illutrations.append(illutration)
    men_healh_dict = {"title": titles, "discription": discriptions,
                        "illutration": illutrations, "link": links}
    men_heath_df = pd.DataFrame(men_healh_dict)
    return men_heath_df
    pass
def scrape_WorldNews(website):
    driver.get(website)
    links = []
    titles = []
    discriptions = []
    illutrations = []
    containers = driver.find_elements(by="xpath",
                                      value='//div/div/div/div[@id="main-content"]/section/div[@class="sun-row teaser teaser--main"]/div[@class="col sun-col-2"]')
    for contain in containers:
        link = contain.find_element(by="xpath", value='./div/div[@class="teaser__copy-container"]/a').get_attribute("href")
        title = contain.find_element(by="xpath", value='./div/div[@class="teaser__copy-container"]/a/h3').text
        discription = contain.find_element(by="xpath", value='./div/div[@class="teaser__copy-container"]/a/p').text
        illutration = contain.find_element(by="xpath", value='./div/div[@class="teaser__image-container"]/a/picture/img').get_attribute("data-src")
        links.append(link)
        titles.append(title)
        discriptions.append(discription)
        illutrations.append(illutration)
    world_news_dict = {"title": titles, "discription": discriptions,
                      "illutration": illutrations, "link": links}
    world_news_df = pd.DataFrame(world_news_dict)
    return world_news_df
    pass
def scrape_Women_Heath_s(list_url):
    list_df = []
    for url in list_url:
        df = scrape_Women_Heath(url)
        list_df.append(df)
    return list_df
    pass
def scrape_Men_Heath_s(list_url):
    list_df = []
    for url in list_url:
        df = scrape_Men_Heath(url)
        list_df.append(df)
    return list_df
    pass
def scrape_WorldNews_s(list_url):
    list_df = []
    for url in list_url:
        df = scrape_WorldNews(url)
        list_df.append(df)
    return list_df
    pass
women_heath_Df = scrape_Women_Heath_s(list_women_heath)
men_heath_Df = scrape_Men_Heath_s(list_men_heath)
worldnews_DF = scrape_WorldNews_s(list_world_news)
final_women_heath_DF = merge_df(women_heath_Df)
final_men_heath_DF = merge_df(men_heath_Df)
final_worldnews_DF = merge_df(worldnews_DF)
create_csv_file(final_women_heath_DF, "women_heath_TheSun")
create_csv_file(final_men_heath_DF, "man_heath_TheSun")
create_csv_file(final_worldnews_DF, "worldnews_TheSun")
driver.quit()