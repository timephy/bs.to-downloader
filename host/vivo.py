import utils

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# class Vivo:
#     def __init__(self, url):
#         self.url = url

#     def driver_action(self):
#         options = webdriver.ChromeOptions()
#         options.add_argument("--headless")
#         # options.add_argument("--window-size=1920x1080")
#         # options.add_experimental_option(
#         #     "excludeSwitches", ["enable-automation"])
#         # options.add_experimental_option("useAutomationExtension", False)

#         driver = webdriver.Chrome(options=options)

#         driver.switch_to_window(driver.window_handles[-1])
#         driver.get(self.url)

#         wait = WebDriverWait(driver, 10)
#         wait.until(EC.presence_of_element_located(
#             (By.CSS_SELECTOR, ".stream-content > div > div > video > source")))

#         self.html = driver.page_source

#     def get_video_url(self):
#         soup = utils.soup(self.html)

#         # source = soup.select_one(".stream-content > div > div > video > source")
#         source = soup.find("source")
#         return source["src"], source["type"], source["size"]


def resolve(url, *, driver=None):
    if driver is None:
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--headless")
        # options.add_experimental_option(
        #     "excludeSwitches", ["enable-automation"])
        # options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)

    if isinstance(url, list):
        return [resolve(url, driver=driver) for url in url]

    print(f"Resolving (vivo): {url}")

    driver.switch_to_window(driver.window_handles[-1])
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".stream-content > div > div > video > source")))

    return _extract(driver.page_source)


def _extract(html):
    soup = utils.soup(html)

    # source = soup.select_one(".stream-content > div > div > video > source")
    source = soup.find("source")
    return source["src"], source["type"], source["size"]
