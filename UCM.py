
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import concurrent.futures
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--log-level=3')
# chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--start-maximized")

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

chrome_options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
driver_path = 'chromedriver'
# driver = webdriver.Chrome(options = chrome_options, executable_path = driver_path)

# driver.get("https://mycentral.ucmo.edu")
# driver.maximize_window()
# wait = WebDriverWait(driver, 10)

def login(driver):
    
   
    # Login
    
    driver.find_element(By.ID,"username").send_keys("username")  
    driver.find_element(By.ID,"password").send_keys("password")
    driver.find_element(By.XPATH,"//*[@id='loginForm']/div[5]/div/button").click()

    
def open_Records_and_Regestrations(driver):
    try:
        # driver.find_element(By.XPATH,"/html/body/div[2]/nav/div/div[1]/ul/li[3]/a/span[1]").click()

        # driver.get("https://mycentral.ucmo.edu/web/home-community/records-and-registration")
        driver.get("https://banner.ucmo.edu:4770/StudentRegistrationSsb/ssb/classRegistration/classRegistration")
        driver.find_element(By.XPATH,"/html/body/main/div[2]/div[2]/div/div/ul/li[2]/a").click()
        driver.find_element(By.XPATH,"/html/body/main/div[3]/div/div/div[2]/div[1]/fieldset/div[2]/div[1]/div[1]/a/span[1]").click()
        driver.find_element(By.XPATH,"/html/body/div[8]/div/input").send_keys("Spring 2023")
        
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/ul/li/div")))
        driver.find_element(By.XPATH,"/html/body/div[8]/ul/li/div").click()
        
        driver.find_element(By.XPATH,"/html/body/main/div[3]/div/div/div[2]/div[3]/button").click()
       

        wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/main/div[3]/div/div[2]/div/div[1]/div/div[1]/div[3]/div[1]/div/fieldset/div[1]/p/div/ul")))
        
        time.sleep(2)
        driver.find_element(By.XPATH,"//*[@id='content']/div[3]/div/div[1]/div/div[2]/div/div/ul/li[6]/a").click()

    except:
        
        pass


def logout(driver):
    try:
        driver.find_element(By.XPATH,"//*[@id='page-wrapper']/div[1]/nav/div[2]/ul/li/a").click()
    except:
        pass
    try:
        driver.find_element(By.XPATH,"//*[@id='user'']").click()
        driver.find_element(By.XPATH,"//*[@id='signOut']/span").click()
    except:
        pass

    time.sleep(2)
    driver.close()

def start_brave(driver):
    
    open_Records_and_Regestrations(driver)
    search_course(driver)
    


def search_course(driver):

    try:
        # wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='loadPlans-tab']")))

        driver.find_element(By.XPATH,"//*[@id='loadPlans-tab']").click()

        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div[3]/div/div[2]/div/div[3]/div[1]/div[2]/div/div[3]/div[2]/div[1]/div/table/tbody/tr[1]/td[10]/div/button")))

        driver.find_element(By.XPATH,"/html/body/main/div[3]/div/div[2]/div/div[3]/div[1]/div[2]/div/div[3]/div[2]/div[1]/div/table/tbody/tr[1]/td[10]/div/button").click()

        driver.find_element(By.XPATH,"/html/body/main/div[3]/div/div[2]/div/div[3]/div[1]/div[2]/div/div[3]/div[2]/div[1]/div/table/tbody/tr[2]/td[10]/div/button").click()
        driver.find_element(By.XPATH,"/html/body/main/div[3]/div/div[2]/div/div[3]/div[1]/div[2]/div/div[3]/div[2]/div[1]/div/table/tbody/tr[3]/td[10]/div/button").click()

        time.sleep(1)
        driver.find_element(By.XPATH,"/html/body/main/div[6]/div[2]").click()
        print("Submit Clicked")
        #Switch the control to the Alert window
        obj = driver.switch_to.alert


        #use the accept() method to accept the alert
        obj.accept()
        
    except:
        pass
    

driver = webdriver.Chrome(options = chrome_options, executable_path = driver_path)

driver.get("https://mycentral.ucmo.edu")
driver.execute_script("window.alert = function() {};")
driver.maximize_window()
wait = WebDriverWait(driver, 10)

login(driver)

try:
    start_brave(driver)
except:
    start_brave(driver)
