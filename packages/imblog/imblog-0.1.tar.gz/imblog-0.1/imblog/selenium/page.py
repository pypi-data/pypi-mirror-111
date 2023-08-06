from imblog.selenium.elements import BasePageElement
from selenium import webdriver
from imblog.selenium.locators import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback
from selenium.webdriver.common.keys import Keys
class UploadElement(BasePageElement):
    locator=UploadPageLocators.INPUT
    is_find_hide=True
class TitleUploadElement(BasePageElement):
    locator=UploadPageLocators.TITLE
    is_click_on = True
class DescriptionUploadElement(BasePageElement):
    locator = UploadPageLocators.DESCRIPTION
    is_click_on = True
class TagUploadElement(BasePageElement):
    locator = UploadPageLocators.TAG
class ThumbnailUploadElement(BasePageElement):
    locator = UploadPageLocators.CUSTOM_THUMB
    is_find_hide = True
class VideoLinkUploadElement(BasePageElement):
    locator = UploadPageLocators.VIDEO_LINK
class EmailLoginElement(BasePageElement):
    delay = 5
    locator=LoginPageLocators.EMAIL_LOGIN
class PassWordLoginElement(BasePageElement):
    delay = 5
    locator=LoginPageLocators.PASS_WORD_LOGIN
class EmailRecoElement(BasePageElement):
    delay = 5
    locator=LoginPageLocators.EMAIL_RECO

class EmailRecoElement2(BasePageElement):
    delay = 5
    locator = LoginPageLocators.EMAIL_RECO2
class LocationElement(BasePageElement):
    delay= 5
    locator = UploadPageLocators.UPL_LOCATION_INPUT
    is_click_on = True
class LocationTABElement(BasePageElement):
    delay= 5
    locator = UploadPageLocators.UPL_LOCATION_INPUT
    is_clear_text = False
class BlogImageInput(BasePageElement):
    delay= 5
    locator = BlogLocators.BLOG_IMG_INPUT
    is_clear_text = False
    is_find_hide = True
class BlogImagePicker(BasePageElement):
    delay = 10
    locator = BlogLocators.BLOG_IMG_PICKER
    is_clear_text = False
    attr_get="src"
class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""
    def __init__(self, driver):
        self.driver = driver

class BlogPage(BasePage):
    input_image = BlogImageInput()
    picker_src = BlogImagePicker()
    def get_url_picker(self):
        self.driver.get("https://www.blogger.com/blog/posts/670")
        time.sleep(3)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(BlogLocators.BLOG_NEW_POST))
        self.driver.find_element(*BlogLocators.BLOG_NEW_POST).click()
        time.sleep(3)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                BlogLocators.BLOG_INSERT_IMAGE))
        items = self.driver.find_elements(*BlogLocators.BLOG_INSERT_IMAGE)
        for item in items:
            if item.is_displayed():
                item.click()
                break
        time.sleep(2)
        items = self.driver.find_elements(*BlogLocators.BLOG_UPLOAD_FROM_COMPUTER)
        for item in items:
            if item.is_displayed():
                item.click()
                break
        time.sleep(3)
        return self.picker_src
    def upload_images(self, picker_src, image_paths):
        self.driver.get(picker_src)
        img_cnt = len(image_paths)
        for image_path in image_paths:
            self.input_image = image_path
        return self.get_images(img_cnt)

    def get_images(self,img_cnt):
        arr = []
        retries=0
        while retries < img_cnt*5:
            arr = []
            items = self.driver.find_elements(*BlogLocators.BLOG_IMG_RS)
            if len(items)==img_cnt:
                for item in items:
                    arr.append(item.get_attribute('src'))
                break
            time.sleep(1)
            retries+=1
        if len(arr)==0:
            items = self.driver.find_elements(*BlogLocators.BLOG_IMG_RS)
            for item in items:
                arr.append(item.get_attribute('src'))
        return arr

class LoginPage(BasePage):
    email_login=EmailLoginElement()
    pass_word_login=PassWordLoginElement()
    email_reco_login=EmailRecoElement()
    email_reco_login2=EmailRecoElement2()
    def is_login(self):
        return "accounts.google.com" in self.driver.current_url
    def is_en_lang(self):
        return "English" in self.driver.find_element(*LoginPageLocators.LANG_CHOOSE_BUTTON).text
    def click_cofirm_reco(self,email_reco):
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.find_element(
                    *LoginPageLocators.RECO_EMAIL_BUTTON))
            self.driver.find_element(*LoginPageLocators.RECO_EMAIL_BUTTON).click()
        except:
            pass
        try:
            self.email_reco_login2=email_reco+Keys.RETURN
        except:
            pass
        try:
            self.email_reco_login=email_reco+Keys.RETURN
        except:
            pass
    def click_profile_indentifier(self):
        self.driver.find_element(*LoginPageLocators.PROFILE_INDENTIFIER).click()
        time.sleep(2)
    def click_next_verify(self):
        self.driver.find_element(*LoginPageLocators.VERIFY_NEXT).click()
        time.sleep(2)
    def change_language(self):
        if self.is_en_lang():
            return
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element(
                *LoginPageLocators.LANG_CHOOSE_BUTTON))
        self.driver.find_element(*LoginPageLocators.LANG_CHOOSE_BUTTON).click()
        time.sleep(1)
        self.driver.find_element(*LoginPageLocators.LANG_IT).click()
        time.sleep(2)
        self.driver.find_element(*LoginPageLocators.LANG_CHOOSE_BUTTON).click()
        time.sleep(1)
        self.driver.find_element(*LoginPageLocators.LANG_EN).click()
        time.sleep(2)
    def click_done_button(self):
        self.driver.find_element(*LoginPageLocators.DONE_BUTTON).click()
        time.sleep(2)



class SearchResultsPage(BasePage):
    """Search results page action methods come here"""

    def is_results_found(self):
        # Probably should search for this text in the specific page
        # element, but as for now it works fine
        return "No results found." not in self.driver.page_source


class AboutMePage(BasePage):
    def fill_text(self, element, text):
        element = self.driver.find_element(*element)
        element.clear()
        element.send_keys(text)
    def change_name(self, full_name):
        first_name=full_name.split(" ")[0]
        last_name=full_name.split(" ")[1]
        try:
            self.fill_text(AboutMeLocators.FIRST_NAME,first_name)
            time.sleep(1)
            self.fill_text(AboutMeLocators.LAST_NAME, last_name)
        except:
            pass
        time.sleep(1)
        try:
            self.fill_text(AboutMeLocators.SUR_NAME, last_name)
        except:
            pass
        time.sleep(1)
        try:
            self.fill_text(AboutMeLocators.FULL_NAME, full_name)
        except:
            pass
        time.sleep(1)
        try:
            self.fill_text(AboutMeLocators.FIRST_NAME_ROLE, first_name)
            time.sleep(1)
            self.fill_text(AboutMeLocators.LAST_NAME_ROLE, last_name)
        except:
            pass
        time.sleep(1)
        try:
            self.driver.find_element(AboutMeLocators.OK_BUTTON).click()
            time.sleep(3)
            self.driver.find_element(AboutMeLocators.CONFIRM_BUTTON).click()
        except:
            pass