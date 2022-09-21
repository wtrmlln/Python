import keyring
import pickle
import os
import re
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

def authorization(site_name, driver):
    if driver.title == "Система управления сайтами NetCat" or site_name == 'ПМК':
        
        login_input = os.getlogin()
        if 'ПМК' in site_name or 'Кабинетоф' in site_name:
            password_input = keyring.get_password('PMK', login_input)
        else:
            password_input = keyring.get_password('SOT/Toruda', login_input)
        
        login_box = driver.find_element(By.NAME, "AUTH_USER")
        password_box = driver.find_element(By.NAME, "AUTH_PW")
        auth_button = driver.find_element(By.XPATH, "//button[@type = 'submit']")
        login_box.send_keys(login_input)
        password_box.send_keys(password_input)
        auth_button.click()
    else:
        return

def add_cookies(cookies, driver, site_name):
    cookie_dict = {}
    for cookie in cookies:
        if cookie["domain"] == '.toruda.ru':
            cookie_dict['Торуда'] = cookie
        elif cookie["domain"] == '.s-o-t.ru':
            cookie_dict['SOT'] = cookie
        elif cookie["domain"] == '.kompkresla.ru':
            cookie_dict['Н'] = cookie
        elif cookie["domain"] == '.prommashkomplekt.ru':
            cookie_dict['ПМК'] = cookie
        elif cookie["domain"] == '.kabinetof.ru':
            cookie_dict['Кабинетоф'] = cookie
        elif cookie["domain"] == '.d-d-i.ru':
            cookie_dict['DDI'] = cookie
        try:
            driver.add_cookie(cookie_dict[site_name])
        except:
            pass

def load_file(filename, site_name, driver):
    fileload_button = driver.find_element(By.NAME, 'f_File')
    fileload_button.send_keys(filename)
    if 'Остатки' in filename:
    
        if site_name == 'Компкресла':
            priceload_button = driver.find_element(By.LINK_TEXT, 'Отправить')
            priceload_button.click()
            result = driver.find_element(By.ID, 'nc_admin_mode_content11845')
            result = result.text[result.text.find("Обновлено товаров"):]
        else:
            try:
                timeout = 20
                element_present = EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Добавить']"))
                WebDriverWait(driver, timeout).until(element_present)
                priceload_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Добавить']")
                priceload_button.click()
                
                element_present = EC.visibility_of_element_located((By.CLASS_NAME, 'alert-success'))
                WebDriverWait(driver, timeout).until(element_present)
                result = driver.find_element(By.CLASS_NAME, 'alert-success')
                result = result.text
            except TimeoutException:
                print(site_name.ljust(15) + '/// ' + filename.ljust(15) + ' /// '.ljust(3) + 'Timed out') 
    else:
        if site_name == 'Компкресла':
            priceload_button = driver.find_element(By.LINK_TEXT, 'Отправить')
            priceload_button.click()
            result = driver.find_element(By.ID, 'nc_admin_mode_content9346')
            result = result.text[result.text.find("Обновлено товаров"):]
        elif site_name == 'Кабинетоф':
            priceload_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Обработать']")
            priceload_button.click()
            result = driver.find_element(By.ID, 'main')
            result = result.text[result.text.find('Обновлено товаров'):result.text.find('Объект')]
            result = re.sub(r'\s+$', '', result)
        else:
            try:
                timeout = 20
                element_present = EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Добавить']"))
                WebDriverWait(driver, timeout).until(element_present)
                priceload_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Добавить']")
                priceload_button.click()
                
                element_present = EC.visibility_of_element_located((By.CLASS_NAME, 'alert-success'))
                WebDriverWait(driver, timeout).until(element_present)
                result = driver.find_element(By.XPATH, "//*[contains(text(), 'Обновлено товаров')]")
                result = result.text
            except TimeoutException:
                print(site_name.ljust(15) + '/// ' + filename.ljust(15) + ' /// '.ljust(3) + 'Timed out')   
    pickle.dump(driver.get_cookies(), open(os.environ.get('PROGRUZKA') + "cookies.pkl","wb"))
    driver.close()
    
    if 'Остатки' in filename:
        try:
            filename = filename[len(os.environ.get('OSTATKI').replace('\\', '/')):]
        except:
            filename = filename
    elif 'Прогрузка' in filename:
        try:
            filename = filename[len(os.environ.get('PROGRUZKA').replace('\\', '/')):]
        except:
            filename = filename
    else:
        filename = filename
    print(site_name.ljust(15) + '/// ' + filename.ljust(15) + ' /// '.ljust(3) + result)
    