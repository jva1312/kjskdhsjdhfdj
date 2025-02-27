import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver as wire_webdriver  # Import selenium-wire webdriver
# from webdriver_manager.chrome import ChromeDriverManager
import os

# Start virtual display
# display = Display(visible=1, size=(1920, 1080))
# display.start()

# Telegram bot configuration

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Proxy configuration
PROXY_HOSTS = [
    "80.240.23.220"
]
PROXY_PORT = "16902"
PROXY_USER = "w7373848392923"
PROXY_PASS = os.getenv("PROXY_PASS")

def send_telegram_message(message):
    """Send a message to the specified Telegram chat."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Message sent to Telegram successfully!")
        else:
            print(f"Failed to send message: {response.text}")
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")

def setup_driver(proxy_host):
    """Initialize Selenium WebDriver with proxy and auto-install ChromeDriver."""
    
    # Configure proxy settings
    seleniumwire_options = {
        "proxy": {
            "http": f"http://{PROXY_USER}:{PROXY_PASS}@{proxy_host}:{PROXY_PORT}",
            "https": f"https://{PROXY_USER}:{PROXY_PASS}@{proxy_host}:{PROXY_PORT}",
        }
    }

    # Set Chrome options
    options = webdriver.ChromeOptions()
    # options.add_argument("--no-sandbox")  
    # options.add_argument("--disable-dev-shm-usage")  
    options.add_argument("--disable-blink-features=AutomationControlled")    
    # Automatically install the latest ChromeDriver
    driver = wire_webdriver.Chrome(
        seleniumwire_options=seleniumwire_options,
        options=options
    )
    
    # driver.maximize_window()
    driver.implicitly_wait(5)
    wait = WebDriverWait(driver, 10)
    return driver, wait

keywords = [
    "Sassuolo ceramica ",
    "Gres porcellanato Sassuolo ",
    "Ceramiche Sassuolo",
    "Ceramica Sassuolo plus ",
    "Vendita gres porcellanato Sassuolo ",
    "Piastrelle Sassuolo",
    "Showroom piastrelle Sassuolo",
    "Rivestimenti Sassuolo ",
    "Effetto marmo Sassuolo",
    "Effetto legno Sassuolo"
]


def search_and_click(proxy_host):
    """Search for a keyword and click a Google ad, sending results to Telegram."""
    for keyword in keywords:
        driver, wait = setup_driver(proxy_host)
        
        try:
            # Step 1: Open Google
            driver.get("http://www.google.it")
            time.sleep(random.uniform(2, 4))

            # Get public IP address


            # Accept cookies if pop-up appears
            try:
                time.sleep(5)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(2, 5))
                # print('error here 2')
                accept_button = wait.until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="L2AGLb"]/div'))
                    # //*[@id="L2AGLb"]/div
                )
                accept_button.click()
                time.sleep(random.uniform(2, 5))
            except:
                print("No cookie pop-up found.")

            # Step 2: Perform search
            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys(keyword)
            time.sleep(random.uniform(1, 3))
            search_box.send_keys(Keys.RETURN)
            time.sleep(random.uniform(3, 6))
            ip_address = driver.execute_script("return fetch('https://api64.ipify.org?format=json').then(res => res.json()).then(data => data.ip);")
            time.sleep(2)

            # Step 3: Find Sponsored Ads
            ads = driver.find_elements(By.XPATH, "//span[contains(text(),'Sponsorizzato')]/ancestor::div[1]//a")

            if ads:
                ad_link = ads[0].get_attribute("href")  # Get ad link
                print(f"Clicking ad: {ad_link}")
                ads[0].click()
                time.sleep(random.uniform(5, 10))  # Wait for page to load
                
                message = f"✅ Ad Found!\n🔍 Keyword: {keyword}\n🌍 IP: {ip_address}\n🔗 Ad Link: {ad_link}"
            else:
                print("No Google Ads found!")
                message = f"❌ No Ad Found!\n🔍 Keyword: {keyword}\n🌍 IP: {ip_address}"

            send_telegram_message(message)

        except Exception as e:
            print("An error occurred:", e)

        finally:
            time.sleep(5)  # Reduce wait time
            driver.quit()

if __name__ == "__main__":
        for host in PROXY_HOSTS:
           
            for i in range(10):
                print(i)
                search_and_click(host)
                if i==10:
                    break
                
