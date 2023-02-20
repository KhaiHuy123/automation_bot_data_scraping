import time
import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType
import pandas as pd
import os, random
from bs4 import BeautifulSoup
from datetime import datetime
import sys
website_nettruyen_page1 = "https://www.nettruyenup.com/"
website_nettruyen_page2 = "https://www.nettruyenup.com/?page=2"
website_nettruyen_page3 = "https://www.nettruyenup.com/?page=3"
website_nettruyen_page4 = "https://www.nettruyenup.com/?page=4"
website_nettruyen_page5 = "https://www.nettruyenup.com/?page=5"
website_nettruyen_page6 = "https://www.nettruyenup.com/?page=6"
website_nettruyen_page7 = "https://www.nettruyenup.com/?page=7"
website_nettruyen_page8 = "https://www.nettruyenup.com/?page=8"
website_nettruyen_page9 = "https://www.nettruyenup.com/?page=9"
website_nettruyen_page10 = "https://www.nettruyenup.com/?page=10"
list_Nettruyen = [
    website_nettruyen_page1, website_nettruyen_page2, website_nettruyen_page3, website_nettruyen_page4,
    website_nettruyen_page5, website_nettruyen_page6, website_nettruyen_page7,
    website_nettruyen_page8, website_nettruyen_page9, website_nettruyen_page10
]
app_path = os.path.dirname(sys.executable)
current_day = datetime.now()
day_month_year = current_day.strftime("%d%m%y")
path = "D:\microsoftdriver_autotest_110\msedgedriver.exe"
service = Service(executable_path=path)
options = webdriver.EdgeOptions()
def get_proxy_ip_and_port():
    url = "https://free-proxy-list.net/#list"
    response = requests.get(url)
    html = response.text
    proxy_table = html.split("<tbody>")[1].split("</tbody>")[0]
    proxies = proxy_table.split("<tr><td>")[1:]
    proxy_list = []
    for proxy in proxies:
        ip = proxy.split("</td><td>")[0]
        port = proxy.split("</td><td>")[1].split("</td><td>")[0]
        proxy_list.append({"http": f"http://{ip}:{port}"})
    return proxy_list
def is_proxy_alive(proxy):
    try:
        response = requests.get("https://free-proxy-list.net/#list", proxies={"http": proxy, "https": proxy})
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        return False
def get_proxy_list():
    url = "https://free-proxy-list.net/#list"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.104 Safari/537.3'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    proxy_list = []
    for row in soup.find_all("table")[0].tbody.find_all("tr"):
        https_value = row.find_all("td")[6].text
        if https_value == "yes":
            proxy = row.find_all("td")[0].text + ":" + row.find_all("td")[1].text
            proxy_list.append(proxy)
    return proxy_list
def extract_proxy(proxy_string):
    proxy = proxy_string.split(":")
    ip = proxy[0]
    port = proxy[1]
    return ip, port
proxy_list = get_proxy_list()
print(proxy_list)
proxy_sever = random.choice(proxy_list)
print(proxy_sever)
proxy_ip = extract_proxy(proxy_sever)[0]
print(proxy_ip)
proxy_port = extract_proxy(proxy_sever)[1]
print(proxy_port)
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': f"{proxy_ip}:{proxy_port}",
    'ftpProxy': f"{proxy_ip}:{proxy_port}",
    'sslProxy': f"{proxy_ip}:{proxy_port}"
})
options.add_argument("--headless")
# options.add_argument('--disable-extensions')
# options.add_argument('--disable-gpu')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-setuid-sandbox')
# options.add_argument('--remote-debugging-port=9222')
# options.add_argument('--disable-browser-side-navigation')
# options.add_argument('--disable-gpu-sandbox')
# options.add_argument('--disable-accelerated-2d-canvas')
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--disable-popup-blocking')
# options.add_argument('--disable-notifications')
#options.add_argument(f'--proxy-server={proxy_sever}')
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edge/90.0.864.75")
#options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36")
#options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edge/86.0.622.63")
#options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299")
#options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134")
#options.proxy = proxy
driver = webdriver.Edge(service=service, options=options)

def scrape_Nettruyen(website):
    time.sleep(3)
    driver.set_window_size(360, 640)
    driver.get(website)
    driver.set_page_load_timeout(10.0)
    driver.set_script_timeout(10.0)
    titles, links, lastest_chap_list, teasers, discriptions, types, conditions, views, follows = [], [], [], [], [], [], [], [], []
    containers = driver.find_elements(by="xpath", value='//div[@class="row"]/div//div/div/div/div[@class="row"]/div')
    for container in containers:
        title = container.find_element(by="xpath", value='./figure/figcaption/h3/a').text
        link = container.find_element(by="xpath", value='./figure/figcaption/h3/a').get_attribute("href")
        latest_chap = container.find_element(by="xpath", value='./figure/figcaption/ul/li[@class="chapter clearfix"]/a').text
        teaser = container.find_element(by="xpath", value='./div/div/div[@class="clearfix"]/div/a/img').get_attribute("data-original")
        sub_container_invisible = container.find_element(by="xpath", value='./div')
        driver.execute_script("return arguments[0].removeAttribute('style')", sub_container_invisible)
        discription = container.find_element(by="xpath", value='./div/div/div[@class="box_text"]').text
        type = container.find_element(by="xpath", value='./div/div/div[@class="clearfix"]/div[@class="message_main"]/p[2]').text
        condition = container.find_element(by="xpath", value='./div/div/div[@class="clearfix"]/div[@class="message_main"]/p[3]').text
        view = container.find_element(by="xpath", value='./div/div/div[@class="clearfix"]/div[@class="message_main"]/p[4]').text
        follow = container.find_element(by="xpath", value='./div/div/div[@class="clearfix"]/div[@class="message_main"]/p[6]').text
        titles.append(title)
        links.append(link)
        lastest_chap_list.append(latest_chap)
        teasers.append(teaser)
        discriptions.append(discription)
        types.append(type)
        conditions.append(condition)
        views.append(view)
        follows.append(follow)
    topDay_manga_dict = {"titles": titles, "lastest_Chap": lastest_chap_list, "types": types, "views": views, "follows":follows,
                         "condition": conditions, "discription": discriptions, "teasers": teasers, "links ": links}
    topDay_manga_df = pd.DataFrame(topDay_manga_dict)
    return topDay_manga_df
    pass
# scrpae_Nettruyen version using css selector
# def scrape_Nettruyen(website):
#     time.sleep(3)
#     driver.set_window_size(360, 640)
#     driver.get(website)
#     driver.set_page_load_timeout(200.0)
#     driver.set_script_timeout(150.0)
#     titles = links = lastest_chap_list = teasers = discriptions = types = conditions = views = follows = []
#     containers = driver.find_elements(by="css selector", value='''div.row > div > div > div > div.row > div''')
#     for container in containers:
#         driver.set_page_load_timeout(200.0)
#         driver.set_script_timeout(50.0)
#         title = container.find_element(by="css selector", value='''figure > figcaption > h3 > a''').text
#         link = container.find_element(by="css selector", value='''figure > figcaption > h3 > a''').get_attribute("href")
#         latest_chap = container.find_element(by="css selector", value='''figure > figcaption > ul > li.chapter.clearfix > a''').text
#         teaser = container.find_element(by="css selector", value='''div > div > div.clearfix > div > a > img''').get_attribute("src")
#         sub_container_invisible = container.find_element(by="css selector", value='''div''')
#         driver.execute_script("return arguments[0].removeAttribute('style')", sub_container_invisible)
#         discription = container.find_element(by="css selector", value='div > div > div.box_text').text
#         type = container.find_element(by="css selector", value='div > div > div.clearfix > div.message_main > p:nth-child(2)').text
#         condition = container.find_element(by="css selector", value='div > div > div.clearfix > div.message_main > p:nth-child(3)').text
#         view = container.find_element(by="css selector", value='div > div > div.clearfix > div.message_main > p:nth-child(4)').text
#         follow = container.find_element(by="css selector", value='div > div > div.clearfix > div.message_main > p:nth-child(6)').text
#         titles.append(title)
#         links.append(link)
#         lastest_chap_list.append(latest_chap)
#         teasers.append(teaser)
#         discriptions.append(discription)
#         types.append(type)
#         conditions.append(condition)
#         views.append(view)
#         follows.append(follow)
#     topDay_manga_dict = {"titles": titles, "lastest_Chap": lastest_chap_list, "types": types, "views": views, "follows":follows,
#                          "condition": conditions, "discription": discriptions, "teasers": teasers, "links ": links}
#     topDay_manga_df = pd.DataFrame(topDay_manga_dict)
#     return topDay_manga_df
def scrape_Nettuyen_s(list_url):
    list_df = []
    for url in list_url:
        df = scrape_Nettruyen(url)
        list_df.append(df)
    return list_df
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
# Multiple pages version:
df_Nettuyen = scrape_Nettuyen_s(list_Nettruyen)
final_dataframe_Nettruyen = merge_df(df_Nettuyen)
create_csv_file(final_dataframe_Nettruyen, file_name="topDayNettruyen")
driver.quit()

#########################################################################
# Single page version                                                   #
# page1_Nettruyen = scrape_Nettruyen(website=website_nettruyen_page2)   #
#                                                                       #
# create_csv_file(page1_Nettruyen, file_name="topDayNettruyen")         #
#                                                                       #
# driver.quit()                                                         #
#########################################################################
