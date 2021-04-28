import os
import json
import time
from getpass import getpass
from requests import get
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions, Chrome
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class Instagram(object):

    def __init__(self):
        self.driver = None
        self.chrome_options = None
        self.response = None
        self.chrome_path = os.path.abspath("chromedriver.exe")
        self.wait = None
        self.maxImgDownloads = 0
        self.maxStoryDownloads = 0
        self.url = "https://www.instagram.com/"
        self.host_url = ""
        self.stories = list()
        self.images = list()
        self.carousellist = list()

        self.driver_init()

    def driver_init(self):
        self.chrome_options = Options()
        self.chrome_options.page_load_strategy = "complete"
    
        self.driver = Chrome(executable_path=self.chrome_path, options=self.chrome_options)

        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        # username = input("Input Username: ")
        # password = getpass(prompt="Enter Password: ")
        
        username = "2maharathikarna@gmail.com"
        password = "Bhola_1810"

        self.driver.get(self.url)
        time.sleep(2)
        self.driver.find_element_by_name("username").send_keys(username)
        self.driver.find_element_by_name("password").send_keys(password)
        buttons = self.driver.find_elements_by_tag_name("button")

        for button in buttons:
            if button.text.lower() == "log in":
                button.click()

        # time.sleep(4)
        self.wait.until(method=self.is_insta_loaded)
        self.get_user()

    def is_insta_loaded(self, driver):
        buttons = driver.find_elements_by_tag_name("button")

        for button in buttons:
            if button.text.lower() == "save info":
                return True

        return False


    def get_user(self):
        # host_user = input("Enter username to scrap: ")
        user = "ojaswita_kolhe"
        self.host_url = self.url + user + "/"

        self.driver.get(self.host_url)


    def __del__(self):
        self.driver.quit()

X = Instagram()
X.login()
