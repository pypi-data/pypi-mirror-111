from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import shutil, requests, os, json
from imblog.selenium import page
from imblog.common import config, utils, Requests
import time, traceback
import threading
import re
class Client():
    def __init__(self, id, email,album_id, timeout=150):
        self.timeout=timeout
        self.id = id
        self.album_id=album_id
        self.email = email.strip()
        self.root_path = utils.get_dir('auto_browser')
        self.cookie_load_folder =os.path.join(self.root_path,self.email)
        self.driver = None
        self.cookie_cur_folder = self.cookie_load_folder
        self.retries_upload=3
        self.is_stop=False

    def setup(self, root_folder="", version="52",ext=".exe"):
        ff_root_folder = os.getenv('FF_ROOT_FOLDER',root_folder)
        ff_version = os.getenv('FF_VERSION', version)
        ff_ext = os.getenv('FF_EXT', ext)
        firefox_binary = ff_root_folder+"FirefoxSetup"+ff_version+"/core/firefox"+ff_ext
        executable_path = ff_root_folder+"geckodriver_"+ff_version+ff_ext
        mail_server = os.getenv("MAIL_SERVER", config.ServerAdress.MAIL_SERVER)
        email_obj = requests.post(f"{mail_server}/automail/api/mail/get/", json={"gmail": self.email}).json()
        if "gmail" not in email_obj:
            return False
        self.pass_word = email_obj["pass_word"]
        self.reco_email = email_obj["recovery_email"]
        utils.load_cookie(self.cookie_load_folder, self.email)
        profile = webdriver.FirefoxProfile(self.cookie_load_folder)
        set_preference=profile.set_preference
        set_preference("dom.webdriver.enabled", False)
        set_preference("webdriver_enable_native_events", False)
        set_preference("webdriver_assume_untrusted_issuer", False)
        set_preference("media.peerconnection.enabled", False)
        set_preference("media.navigator.permission.disabled", False)
        self.driver = webdriver.Firefox(firefox_profile=profile, firefox_binary=firefox_binary,
                                        executable_path=executable_path)
        self.cookie_cur_folder = self.driver.capabilities.get('moz:profile')
        return True

    def check_login(self):
        self.driver.get("https://www.blogger.com/blog/posts/670")
        login_page = page.LoginPage(self.driver)
        if login_page.is_login():
            try:
                login_page.change_language()
            except:
                pass
            try:
                login_page.click_next_verify()
            except:
                pass
            try:
                login_page.click_profile_indentifier()
            except:
                pass
            try:
                login_page.email_login = self.email+Keys.RETURN
                self.sleep(3)
            except:
                pass
            try:
                login_page.pass_word_login = self.pass_word+Keys.RETURN
                self.sleep(3)
            except:
                pass
            try:
                login_page.click_cofirm_reco(self.reco_email)
            except:
                pass
            try:
                login_page.click_done_button()
            except:
                pass
            self.sleep(5)
            self.driver.get("https://www.blogger.com/blog/posts/670")
            login_page = page.LoginPage(self.driver)
            if login_page.is_login():
                print("Login  Fail")
                return False
        return True

    def sleep(self,t):
        if self.is_stop:
            return
        time.sleep(t)
    def get_album_id(self,url):
        r1 = re.findall(r"uploadToAlbumId=(\d+)&", url)
        if len(r1)>0:
            return r1[0]
    def create_picker_src(self):
        return 'https://www.blogger.com/picker?protocol=gadgets&origin=https://www.blogger.com&authuser=0' \
               '&rpcUrl=https://www-rpcjs-opensocial.googleusercontent.com/gadgets/js/rpc.js?c=1&container=' \
               'blogger&hl=en&parent=https://www.blogger.com/rpc_relay.html&thumbs=orig&multiselectEnabled=true&hostId=blogger' \
               f'&title=Add Images&uploadToAlbumId={self.album_id}&pp=' \
               '[["blogger",{"albumId":' \
               f'"{self.album_id}","copyFromPicasa":true' \
               '}]]&nav=(("photos","Upload",{"mode":"palette","allowedItemTypes":"photo","hideBc":"true","upload":"true","data":{"silo_id":"3"},' \
               f'"parent":"{self.album_id}"' \
               '}))&rpcService=wwkj267xnhdo&rpctoken=jvzma95boegi#rpctoken=jvzma95boegi'
    def get_iframe_image(self):
        self.driver.get("https://www.blogger.com/blog/posts/670")
        time.sleep(1)
        self.driver.find_element_by_xpath('//div[@role="button"]//span[contains(text(),"New Post")]').click()
        items = self.driver.find_elements_by_xpath('//div[@role="button" and @data-tooltip="Insert image"]')
        for item in items:
            if item.is_displayed():
                item.click()
    def execute(self):
        try:
            next = True
            if not self.setup(root_folder=config.Client.ROOT_FOLDER, version="68", ext=config.Client.EXT):
                Requests.log(self.id, "[Error]Can't Init")
                next = False
                return
            if  not self.check_login():
                Requests.log(self.id, "[Error]Login Fail")
                next = False
            if next:
                blog = page.BlogPage(self.driver)
                if not self.album_id:
                    self.picker_src = blog.get_url_picker()
                    self.album_id = self.get_album_id(self.picker_src)
                    Requests.update_album_id(self.id, self.album_id)
                else:
                    self.picker_src = self.create_picker_src()
                cnt_error = 0
                while not self.is_stop and cnt_error < 10:
                    try:
                        dUrl=requests.get(config.ServerAdress.BLOG_SERVER +"cdn/image/job/get").json()
                        if "id" in dUrl:
                            urls=json.loads(dUrl['urls'])
                            arr_path=[]
                            for url in urls:
                                img_path= utils.download_img(url)
                                if img_path:
                                    arr_path.append(img_path)
                            arr_rs = blog.upload_images(self.picker_src, arr_path)
                            data={"id":dUrl["id"], "blog_urls":arr_rs}
                            requests.post(config.ServerAdress.BLOG_SERVER +"cdn/image/job/update",json=data).text
                            for path in arr_path:
                                os.remove(path)
                            self.sleep(1)
                            cnt_error = 0
                    except:
                        traceback.print_exc()
                        Requests.log(self.id, "[Error] Except: " + str(traceback.format_exc()))
                        cnt_error += 1
                        self.sleep(5)
                        pass
        except Exception as e:
            Requests.log(self.id, "[Error] Except: "+str(e))
            traceback.print_exc()
            pass
        self.close()
    def start(self):
        self.processx = threading.Thread(target=self.execute)
        self.processx.start()
    def wait(self):
        self.processx.join(self.timeout)
        if self.processx.is_alive():
            Requests.log(self.id, "Restart----")
            self.close()

    def get_driver(self):
        return self.driver
    def close(self):
        self.is_stop = True
        if self.driver:
            try:
                utils.save_cookie(self.cookie_cur_folder, self.email)
            except:
                traceback.print_exc()
                pass
            try:
                self.driver.close()
            except:
                pass
            try:
                self.driver.quit()
            except:
                pass
            try:
                shutil.rmtree(self.cookie_cur_folder)
            except:
                pass
            try:
                shutil.rmtree(self.cookie_load_folder)
            except:
                pass
            try:
                shutil.rmtree(self.folder_data)
            except:
                pass
            try:
                os.system(f"pkill -f \"{self.cookie_cur_folder}\"")
                os.system(f"rm -rf \"{self.cookie_cur_folder}\"")
            except:
                pass
            self.driver=None





