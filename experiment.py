from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

PATH = "C:\Program Files (x86)\chromedriver.exe"
s = Service(PATH)
driver = webdriver.Chrome(service=s)

driver.get("https://orteil.dashnet.org/cookieclicker/")

aceitar_cookies_site = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "cc_btn_accept_all"))
).click()

language = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.ID, "langSelect-PT-BR"))
).click()

# quando os cookies passam dos:
# 1000: retorna '1,000'
# 1000000: retorna '1.000 million'
# 1000000: retorna '1.000 billion'
# 1000000: retorna '1.000 trillion'
# etc
# aqui acrescenta os zeros necessários para alcançar o número a sua real escala
def text_to_int(text, scale):
    total = int(text.replace(',', '').replace('.', '').replace('\n', ''))
    scale = scale.strip()

    if(scale == 'million'):
        total *= 1000
    elif(scale == 'billion'):
        total *= 1000000
    elif(scale == 'trillion'):
        total *= 1000000000
    elif(scale == 'quadrillion'):
        total *= 1000000000000
    elif(scale == 'quintillion'):
        total *= 1000000000000000
    elif(scale == 'sextillion'):
        total *= 1000000000000000000
    else:
        total = total
    return total


def main():
    while True:
        cookies_count = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.ID, "cookies"))
        )

        big_cookie = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "bigCookie"))
        )
        big_cookie.click()
        

        try:
            upgrades = driver.find_elements(
                By.CSS_SELECTOR, "div#upgrades > .crate.upgrade.enabled")
            achievments_close_btns = driver.find_elements(
                By.CSS_SELECTOR, "div.framed.note.haspic.hasdesc > .close")
            products = driver.find_elements(
                By.CSS_SELECTOR, ".product.unlocked.enabled")

            cookies_list = cookies_count.text.split(" ")
            cookie_value_text = cookies_list[0]
            cookie_scale_text = cookies_list[1].split('\n')[0]
            cookies_total = text_to_int(cookie_value_text, cookie_scale_text)

            # se upgrade disponível, compra.
            if(len(upgrades) > 0):
                upgrade_to_buy = upgrades[0]
                upgrade_actions = ActionChains(driver)
                upgrade_actions.move_to_element(upgrade_to_buy)
                upgrade_actions.click()
                upgrade_actions.perform()
            
            # é possível comprar products da mesma forma que os upgrades são comprados
            if(len(products) > 0):
                product_to_buy = products[-1]
                product_to_buy_arr = product_to_buy.text.split('\n')
                product_scale = ''
                product_quantity = None

                print(product_to_buy_arr)

                # se estiver na escala dos "illions" (millions, billions, trillions, 'quadrillions'...)
                # o índice 1 de products retorna como: ['100.000 million']
                if('illion' in product_to_buy_arr[1]):
                    price_arr = product_to_buy_arr[1].split(' ')
                    print(price_arr)
                    product_scale = price_arr[1]
                    product_value = text_to_int(price_arr[0], product_scale)
                else:
                    product_value = text_to_int(product_to_buy_arr[1], product_scale)
                    
                if(len(product_to_buy_arr) > 2):
                    product_quantity = int(product_to_buy_arr[2])
                else:
                    product_quantity = 0
                    
                product_limit = 100
                if(cookies_total >= product_value and product_quantity < product_limit):
                    products_actions = ActionChains(driver)
                    products_actions.move_to_element(product_to_buy)
                    products_actions.click()
                    products_actions.perform()

                # um cookie de ouro aparece aleatoriamente na página, clicar nele gera bônus

                # golden_cookie = driver.find_element(By.CSS_SELECTOR, ".shimmer")

                # if(golden_cookie):
                #     golden_cookie_ations = ActionChains(driver)
                #     golden_cookie_ations.move_to_element(golden_cookie)
                #     golden_cookie_ations.click()
                #     golden_cookie_ations.perform()
                #     print('GOLDEN COOKIE')
                        
                if(len(achievments_close_btns) > 0):
                    achievment_to_close = achievments_close_btns[0]
                    achievments_actions = ActionChains(driver)
                    achievments_actions.move_to_element(achievment_to_close)
                    achievments_actions.click()
                    achievments_actions.perform()


        except:
            print('Algo inesperado aconteceu!')


if __name__ == '__main__':
    main()
