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
        self.maxImgDownloads = 40
        self.maxStoryDownloads = 40
        self.url = "https://www.instagram.com/"
        self.host_url = ""
        self.stories = list()
        self.images = list()
        self.carousellist = list()
        self.names = list()
        self.carouseloffset = 0

        self.driver_init()

    def driver_init(self):
        self.chrome_options = Options()
        self.chrome_options.page_load_strategy = "complete"
    
        self.driver = Chrome(executable_path=self.chrome_path, options=self.chrome_options)

        self.wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1)

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

        time.sleep(4)
        # self.wait.until(method=self.is_insta_loaded)
        self.get_user()

    def is_insta_loaded(self, driver):
        buttons = driver.find_elements_by_tag_name("button")

        for button in buttons:
            if button.text.lower() == "save info":
                return True

        return False

    def is_right_loaded(self, driver):
        try:
            driver.find_element(By.CLASS_NAME, "coreSpriteRightChevron")
        except NoSuchElementException as e:
            return False
        return True

    def is_stories_loaded(self, driver):
        try:
            driver.find_element(By.XPATH, "//div[@aria-label='Open Stories']")
        except NoSuchElementException as e:
            return False
        return True


    def get_user(self):
        # user = input("Enter username to scrap: ")
        user = "_rucha_1104"
        self.host_url = self.url + user + "/"

        self.driver.get(self.host_url)
        time.sleep(4)
        self.dirpath = os.path.join(os.getcwd(), user)

        if not os.path.exists(self.dirpath):
            os.mkdir(self.dirpath)
        
        if not os.path.exists(os.path.join(self.dirpath, "images")):
            os.mkdir(os.path.join(self.dirpath, "images"))
        
        if not os.path.exists(os.path.join(self.dirpath, "stories")):
            os.mkdir(os.path.join(self.dirpath, "stories"))

        self.get_stories()
        self.get_images()

        self.get_names(self.images, "images")
        print(os.getcwd())
        print(self.names)
        with ThreadPoolExecutor() as executor:
            executor.map(self.get_imgs, self.names)

        self.get_names(self.stories, "stories")
        print(os.getcwd())
        print(self.names)
        with ThreadPoolExecutor() as executor:
            executor.map(self.get_imgs, self.names)

    def get_imgs(self, img_info):
        img_name, img_url = img_info
        try:
            img_bytes = get(img_url).content
        except:
            return

        with open(img_name, "wb") as file:
            file.write(img_bytes)

        print(f"{img_name} is downloaded ...")

        
    def get_names(self, imgList, name):
        self.names.clear()
        os.chdir(os.path.join(self.dirpath, name))
        for num, link in enumerate(imgList):
            filename = f"{num + 1}.jpg"
            self.names.append((filename, link))


    def get_stories(self):
        
        self.wait.until(self.is_stories_loaded)
        # time.sleep(3)
        stories = self.driver.find_elements_by_xpath("//div[@aria-label='Open Stories']")
        
        if len(stories):
            stories[0].click()
        print(len(stories))
        
        self.wait.until(self.is_right_loaded)
        rightDrag = self.driver.find_element_by_class_name("coreSpriteRightChevron")

        try:
            while True:
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                imgs = soup.findAll(lambda tag: tag.name == "img" and tag.has_attr("srcset"))
                print("Images: ", len(imgs))
                for img in imgs:
                    # print(img)
                    try:
                        imgsrclist = img.attrs["srcset"].split(",")
                        size1 = int(imgsrclist[0].split(" ")[-1][:-1])
                        size2 = int(imgsrclist[1].split(" ")[-1][:-1])
                        print(size1, size2, sep="\t")
                        imgsrc = img.attrs["srcset"].split(",")[0]
                    except IndexError as e:
                        print("Size of source set :", len(imgsrclist))
                        print(e)
                        
                    if size1 < size2:
                        print("Skipping")
                        continue
                        
                    if len(self.stories) > self.maxStoryDownloads:
                        return 

                    if imgsrc not in self.stories:
                        self.stories.append(imgsrc) 

                rightDrag.click()
                time.sleep(0.5)
        
        except:
            print("Got Stories")

    def get_images(self):
        self.driver.get(self.host_url)
        time.sleep(4)

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while len(self.images) <= self.maxImgDownloads:
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            imgs = soup.findAll(lambda tag: tag.name == "img" and tag.has_attr("srcset"))

            for img in imgs:
                linkParent = img.find_parent(lambda tag: tag.name == "a")
                numChildren = len([child for child in linkParent.children])

                if numChildren == 1:
                    imgsrc = img.attrs["srcset"].split(",")[-1]
                    if imgsrc not in self.images:
                        self.images.append(imgsrc)
                else:
                    newLink = linkParent.attrs["href"]
                    for index, link in self.carousellist:
                        if link == newLink:
                            break
                    else:
                        self.carousellist.append((len(self.images), newLink))

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if last_height == new_height:
                break

            last_height = new_height

        for x in self.carousellist:
            self.get_carousel_imgs(x)

    def get_carousel_imgs(self, links):
        index, link = links
        imgLinks = list()

        url = self.url[:-1] + link
        self.driver.get(url)

        time.sleep(2)

        try:
            while True:
                X.driver.find_element_by_class_name("coreSpriteRightChevron").click()
                time.sleep(0.6)
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                imgs = soup.findAll(lambda tag: tag.name == "img" and tag.has_attr("srcset"))

                for img in imgs:
                    parents = img.find_parents(lambda tag: tag.name == "li")
                    
                    if len(parents) > 0:
                        imgsrc = img.attrs["srcset"].split(",")[-1]
                        if imgsrc not in imgLinks:
                            imgLinks.append(imgsrc)

        except:
            print("Done with Carousel")

        for i in range(len(imgLinks) - 1, -1, -1):
            self.images.insert(self.carouseloffset + index, imgLinks[i])

        self.carouseloffset += len(imgLinks)
        print(f"Added {len(imgLinks)} arguments.")


    # def __del__(self):
    #     self.driver.quit()

X = Instagram()
X.login()
