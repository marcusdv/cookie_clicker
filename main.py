from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import numpy as np

PATH = "C:\Program Files (x86)\chromedriver.exe"
s = Service(PATH)
driver = webdriver.Chrome(service=s)

driver.get("https://orteil.dashnet.org/cookieclicker/")

aceitar_cookies_site = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "cc_btn_accept_all"))
).click()

change_language_btn = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.ID, "changeLanguage"))
).click()

close_language_menu = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.ID, "promptClose"))
).click()



def main():
    # loop infinito
    while 1:
        big_cookie = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "bigCookie"))
        )
        big_cookie.click()

        # programa não precisa crashar
        # caso um erro aconteça ele continuará clicando
        try:
            # quando o upgrade fica disponível pra compra, ele muda a classe de 'disabled' para 'enabled'
            upgrades = driver.find_elements(
                By.CSS_SELECTOR, "div#upgrades > .crate.upgrade.enabled")
                
            achievments_close_btns = driver.find_elements(
                By.CSS_SELECTOR, "div.framed.note.haspic.hasdesc > .close")
            
            products = driver.find_elements(
                By.CSS_SELECTOR, ".product.unlocked.enabled")

            if(len(upgrades) > 0):
                upgrade_to_buy = upgrades[0]
                upgrade_actions = ActionChains(driver)
                upgrade_actions.move_to_element(upgrade_to_buy)
                upgrade_actions.click()
                upgrade_actions.perform()

            if(len(products) > 0):
                product_to_buy = products[-1]
                product_to_buy_arr = product_to_buy.text.split('\n')
                product_quantity = None

                if(len(product_to_buy_arr) > 2):
                    product_quantity = int(product_to_buy_arr[2])
                else:
                    product_quantity = 0
                
                product_limit = 100
                if(product_quantity < product_limit):
                    products_actions = ActionChains(driver)
                    products_actions.move_to_element(product_to_buy)
                    products_actions.click()
                    products_actions.perform()
                
            # fecha balões de conquistas
            if(len(achievments_close_btns) > 0):
                    achievment_to_close = achievments_close_btns[0]
                    achievments_actions = ActionChains(driver)
                    achievments_actions.move_to_element(achievment_to_close)
                    achievments_actions.click()
                    achievments_actions.perform()

        # ! pesquisar maneiras melhores de lidar com erros ! #
        except:
            print('Algo inesperado aconteceu!')


if __name__ == '__main__':
    main()
