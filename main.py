import os
import json
import time
from getpass import getpass
from requests import get
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
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
        self.stories = list()
        self.images = list()
        self.carousellist = list()

    def login(self):
        username = input("Input Username: ")
        password = getpass(prompt="Enter Password: ")

if __name__ == "__main__":
    print("Hello, World")