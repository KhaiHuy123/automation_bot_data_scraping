from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from datetime import datetime
import sys, time, os, pandas as pd

global list_Amazon

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
    file = f'{file_name}_{day_month_year}.csv'
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
def write_to_file(lst, filename):
    with open(filename, 'w') as f:
        for item in lst:
            f.write(str(item) + '\n')

def scrape_Amazon(website):
    driver.get(website)
    driver.fullscreen_window()
    time.sleep(3)
    driver.set_page_load_timeout(20.0)
    driver.set_script_timeout(20.0)
    for i in range(250):
        driver.execute_script(f"window.scrollTo(0, {str(i)}00);")

    ########################################################################################################################################

    containers_links = driver.find_elements(By.XPATH, '//*[@id="search"]//div[@class="s-main-slot s-result-list s-search-results sg-row"]'
                                                      '//div[@class="sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16"]'
                                                      '//a[@class="a-link-normal s-no-outline"]')
    print(len(containers_links))
    links = [container_link.get_attribute("href") for container_link in containers_links]

    ########################################################################################################################################

    containers_name_products = driver.find_elements(By.XPATH, '*//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]'
                                                              '/span[@class="a-size-medium a-color-base a-text-normal"]')
    print(len(containers_name_products))
    name_products = [container_name_product.text for container_name_product in containers_name_products]

    ########################################################################################################################################

    containers_authors = driver.find_elements(By.XPATH, '*//div[@class="a-row a-size-base a-color-secondary"]/div[@class="a-row"]')
    print(len(containers_authors))
    author = [container_author.text for container_author in containers_authors]

    ########################################################################################################################################

    containers_star_rate = driver.find_elements(By.XPATH, "*//span[@aria-label]/span[@class='a-size-base']")
    print(len(containers_star_rate))
    star_rate = [container_star.text for container_star in containers_star_rate]

    ########################################################################################################################################
    price_xpath = '*//div[@class="a-row a-size-base a-color-base"]/a/span[@class="a-price"]/span[@aria-hidden="true"]'
    container_prices = driver.find_elements(By.XPATH, price_xpath)
    print(len(container_prices))
    price = [container_price.text for container_price in container_prices]

    ########################################################################################################################################

    max_len = max(len(links), len(name_products), len(star_rate), len(author), len(price))
    links += [float('NaN')] * (max_len - len(links))
    name_products += [float('NaN')] * (max_len - len(name_products))
    star_rate += [float('NaN')] * (max_len - len(star_rate))
    author += [float('NaN')] * (max_len - len(author))
    price += [float('NaN')] * (max_len - len(price))
    amazon_dict = {"name_product": name_products, "star_rate": star_rate, "price": price,
                   "author": author,  "link": links}
    amazon_df = pd.DataFrame(amazon_dict)
    amazon_df['star_rate'].fillna('unknown', inplace=True)
    amazon_df['price'].fillna("0", inplace=True)
    return amazon_df
    pass
def scrape_Amazon_s(list_url):
    list_df = []
    for url in list_url:
        df = scrape_Amazon(url)
        list_df.append(df)
    return list_df
    pass

def main():
    df_Amazon = scrape_Amazon_s(list_Amazon)
    final_dataframe_Amazon = merge_df(df_Amazon)
    create_csv_file(final_dataframe_Amazon, file_name="Info_Amazon")
    driver.quit()

list_Amazon = read_file("C:\\Users\\HTH\\PycharmProjects\\another_project_test\\"
                        "automation_bot_data_scraping\\data_scraping\\url_list\\manga_dystopian_amazon.txt")
if __name__ == '__main__':
    main()