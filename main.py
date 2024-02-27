from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import NoSuchElementException

import exceptions
import time


class LinkedinScraper(Chrome):
    def __init__(self):
        self.login_attempt = 0

        options = ChromeOptions()
        options.use_chromium = True
        options.add_argument("--gust")
        options.add_argument("--disable-gpu")
        options.add_argument("--mute-audio")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        super().__init__(service=Service("driver\\chromedriver.exe"), options=options)

    @staticmethod
    def stay_alive():
        """ keep the browser opened, so you don't have to log in repeatedly"""
        while True:
            time.sleep(3600)

    def login(self) -> bool:
        """ try to log in if failed you have 3 more attempts before quitting """
        self.get('https://www.LinkedIn.com/login')
        with open('login.txt', 'r', encoding='utf-8', errors='ignore') as file:
            login_info = file.readline().split(':')
            username = login_info[0] or False
            passwrd = login_info[1] or False
            if username is False or passwrd is False:
                raise exceptions.LoginFailed('LoginFailed - username or password not found')
        time.sleep(3)
        chain = ActionChains(self)
        try:
            username_field = self.find_element(By.ID, 'username')
            chain.move_to_element(username_field)
            chain.click(username_field)
            username_field.send_keys(username)

            password_field = self.find_element(By.ID, 'password')
            chain.move_to_element(password_field)
            chain.click(password_field)
            password_field.send_keys(passwrd)

            chain.click(self.find_element(By.CSS_SELECTOR, 'button[type="submit"]'))

        except NoSuchElementException: pass
        else: chain.perform()

        time.sleep(5)
        if "checkpoint" in self.current_url or "login" in self.current_url:  # detects captcha and if LinkedIn didn't redirect then log in failed
            if self.find_element(By.CSS_SELECTOR, 'iframe[id="captcha-internal"]').is_displayed():
                self.set_window_rect(10, 10)
                time.sleep(20)  # 20 seconds to solve the captcha if detected

            self.login_attempt += 1
            self.login()
            if self.login_attempt > 3:
                self.quit()
                raise exceptions.LoginFailed('LoginFailed - try checking your username and password')

        self.minimize_window()
        return True
