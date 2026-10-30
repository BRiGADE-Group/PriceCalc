import time
import selenium
from selenium import webdriver
from selenium.common.exceptions import *
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
ua = UserAgent()

def check_id(url, appid=None):
    look4redirect: bool | None = None
    successm: bool | None = None
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    # options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(f'user-agent={ua.random}')
    driver = webdriver.Chrome(options=options)

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

    # url = url.replace("<appid>", str(appid))
    if ".com" in url:
        look4redirect = True
    print("INFO - Accessing check URL (Speed : {speed})".format(speed=("Fast" if look4redirect == True else "Normal")))
    driver.get(url)
    if look4redirect == True:
        try:
            WebDriverWait(driver, 20).until(EC.url_changes(url))
            print("Redirection detected.")
            if "Welcome to Steam" not in driver.title:
                success = True
            else:
                success = False
        except TimeoutException as e:
                print("Timeout reached, no redirection, prob error!")
                success = False
        driver.quit()
        return success
    else:
        def check_validity():
            # if "Error 404 · SteamDB" in driver.title or "Error · SteamDB" in driver.title or "Unknown" in driver.title:
            if driver.title == "Error 404 · SteamDB" or driver.title == "Error · SteamDB":
                driver.quit()
                validity = False
            else:
                driver.quit()
                validity = True
            return validity
        time.sleep(1.564254)
        print("Checking if a captcha spawns...")
        try:
            # WebDriverWait(driver, 20).until(EC.text_to_be_present_in_element_attribute((By.TAG_NAME, "a"), "href", "cloudflare"))
            # WebDriverWait(driver, 7).until(EC.text_to_be_present_in_element_attribute((By.TAG_NAME, "input"), "aria-label", "Verify you are human"))
            time.sleep(10)
            if "Just a moment..." in driver.title:
                # WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.TAG_NAME, "title"), "Just a moment..."))
                print("Captcha spawned...")
                print("Will we be lucky?")
                for i in range(10):
                    if i <= 1:
                        if not "Just a moment..." in driver.title:
                            check_validity()
                        else:
                            time.sleep(1)
                            i = i-1
                    else:
                        print("Unlucky! Trying to manually bypass captcha...")
                # try:
                    time.sleep(5)
                    for elm in driver.find_elements(By.TAG_NAME, "input"):
                        if not "Verify you are human" in elm.get_dom_attribute("aria-label"):
                            pass
                        else:
                    # elm2 = WebDriverWait(driver, 7).until(EC.text_to_be_present_in_element_attribute((By.TAG_NAME, "input"), "aria-label", "Verify you are human"))
                            try:
                                WebDriverWait(driver, 15).until(EC.element_to_be_clickable(elm))
                                time.sleep(5.956874)
                                elm.click()
                                print("Supposedly clicked the captacha, now wating for page URL to change...")
                                try:
                                    # WebDriverWait(driver, 30).until_not(EC.text_to_be_present_in_element((By.TAG_NAME, "title"), "Just a moment"))
                                    for i in range(30):
                                        if i <= 1:
                                            if not "Just a moment..." in driver.title:
                                                check_validity()
                                            else:
                                                time.sleep(1)
                                                i = i-1
                                        else:
                                            print("Title not changed. Captcha bypassing failed.")
                                            driver.quit()
                                            return None
                                except TimeoutError:
                                    print("Title not changed! Captcha bypassing failed!")
                                    driver.quit()
                                    return None
                            except TimeoutError:
                                print("Could never click the captcha.")
                                driver.quit()
                                return None
            else:
                print("No captcha detected! Thank God!")
                check_validity()
        except TimeoutError:
            print("No captcha detected! Thank God!")
            check_validity()

        """
        If my theory is right, the following code is something I wrote and will never be used,
        Since it took me long enough to write that, I'm leaving it here, enjoy my very rookie mistake :>
        - 0xSenko
        for elm in driver.find_elements(By.TAG_NAME, "a"):
            if "cloudflare" not in elm.get_dom_attribute("href"):
                pass
            else:
                for elm2 in driver.find_elements(By.TAG_NAME, "input"):
                    if not elm2.get_dom_attribute("aria-label") == "Verify you are human":
                        pass
                    else:
                        print("Will we be lucky?")
                        try:
                            WebDriverWait(driver, 20).until(EC.url_changes())
                        except TimeoutError:
                            print("Unlucky! Trying to manually bypass captcha...")
                        try:
                            WebDriverWait(driver, 50).until(EC.element_to_be_clickable(elm2))
                            time.sleep(5.956874)
                            elm2.click()
                        except TimeoutError:
                            print("Could never click the captcha.")
                        print("Supposedly clicked the captacha, now wating for page URL to change...")
                        try:
                            WebDriverWait(driver, 20).until(EC.url_changes())
                            if "404" in 
                        except TimeoutError:
                            print("URL not changed! Captcha bypassing failed!")"""