import os
import json
import time
from getpass import getpass
from requests import get
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions, Chrome
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
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
        self.carouseloffset = 0

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

    def is_story_loaded(self, driver):
        try:
            driver.find_element(By.CLASS_NAME, "coreSpriteRightChevron")
        except NoSuchElementException as e:
            return False

        return True


    def get_user(self):
        # host_user = input("Enter username to scrap: ")
        user = "ojaswita_kolhe"
        self.host_url = self.url + user + "/"

        self.driver.get(self.host_url)
        self.dirpath = os.path.join(os.getcwd(), user)

        if os.path.exists(self.dirpath):
            os.mkdir(self.dirpath)

    def get_stories(self):
        stories = self.driver.find_elements_by_xpath("//div[@aria-label='Open Stories']")
        
        if len(stories):
            stories[0].click()

        print(len(stories))
        self.wait.until(self.is_story_loaded)

        rightDrag = self.driver.find_element_by_class_name("coreSpriteRightChevron")

        try:
            while True:
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                imgs = soup.findAll(lambda tag: tag.name == "img" and tag.has_attr("srcset"))

                for img in imgs:
                    imgsrc = img.attr["srcset"].split(",")[0]
                    
                    if len(self.stories) > self.maxStoryDownloads:
                        return 

                    if imgsrc not in self.stories:
                        self.stories.append(imgsrc) 

                rightDrag.click()
                time.sleep(0.5)
        
        except StaleElementReferenceException as e:
            print(e.message)

    def get_images(self):
        self.driver.get(self.host_url)
        time.sleep(2)

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while len(self.images) <= self.maxImgDownloads:
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            imgs = soup.findAll(lambda tag: tag.name == "img" and tag.has_attr("srcset"))

            for img in imgs:
                linkParent = img.find_parent(lambda tag: tag.name == "a")
                numChildren = len([child for child in linkParent.children])

                if numChildren == 1:
                    imgsrc = img.attrs["srcset"].split(",")[-1]
                    if imgsrc not in self.downloadlist:
                        self.downloadlist.append(imgsrc)
                else:
                    newLink = linkParent.attrs["href"]
                    for index, link in self.carousellist:
                        if link == newLink:
                            break
                    else:
                        self.carousellist.append((len(self.downloadlist), newLink))

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            # WebDriverWait(self.driver, 3)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if last_height == new_height:
                break

            last_height = new_height
            

    def __del__(self):
        self.driver.quit()

X = Instagram()
X.login()
