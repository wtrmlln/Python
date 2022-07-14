import pickle
import pandas as pd

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

global df
df = pd.DataFrame(columns=['Сайт', "Тайтл", "Длина тайтла", "Декскрипшен", "Длина дескрипшена", 
                           "Ключевые слова", "Заголовки", "Технические ошибки", "Возраст сайта", 
                           "Размер страницы", "Скорость загрузки", "IP адрес", "Стоимость сайта", 
                           "Проиндексировано в Яндекс", "Яндекс ИКС", "Фильтр за вирусы в Яндекс", 
                           "Проиндексировано в Гугл", "Скорость загрузки dekstop Гугл", "Скорость загрузки mobile Гугл", 
                           "Megaindex Trust Rank", "Megaaindex Domain Rank", "Уникальные ссылки",
                           "Домены", "IP адреса", "Подсети", "Mobile Friendly Test", "Тег viewport",
                           "Flash элементы", "Java апплеты", "Silverlight плагины", "Проверка на AMP", 
                           "Кодировка", "Robots.txt", "Sitemap.xml", "iframe на страницы", "Ошибки валидности HTML", 
                           "Ошибки валидности CSS", "Youtube", "VK", "Facebook", "Instagram", "Twitter", "Telegram"]) 

def load_cookies():
    try:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        return cookies
    except:
        cookies = None
        return cookies

def add_cookies(cookies, driver):
    for cookie in cookies:
        if cookie["domain"] == '.be1.ru':
            try:
                driver.add_cookie(cookie)
            except:
                pass

def bypass_popup_window(driver):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="custom-modal-btn"]')))
        pop_up_window = driver.find_element(By.XPATH, '//*[@class="custom-modal-btn"]')
        pop_up_window.click()
    except (NoSuchElementException, TimeoutException, WebDriverException):
        pass

def testing(site):
    
    timeout = 20
    
    # Заходим на сайт
    driver.get('https://be1.ru/')

    # Ищем окно ввода сайта
    site_box = driver.find_element(By.ID, "url")
    site_box.send_keys(site)
    
    # Ищем кнопку "Анализировать" и жмем её
    try:
        find_button = driver.find_element(By.XPATH, '//button[@class="btn btn2 hidden-xs hidden-sm"][normalize-space()="Анализировать"]')
    except NoSuchElementException:
        find_button = driver.find_element(By.XPATH, '//button[@class="btn2 btn btn-sm hidden-lg hidden-md margin_top5"][normalize-space()="Анализировать"]')
    find_button.click()
   
    recaptcha_timeout = 500
    try:
        WebDriverWait(driver, recaptcha_timeout).until_not(EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-border")))
    except:
        pass
       
    try:
        # Вытягиваем всю страницу HTML с отчетом
        bypass_popup_window(driver)
        element_present = EC.element_to_be_clickable((By.XPATH, '//div[@class="col-md-11" and @id="report"]'))
        WebDriverWait(driver, timeout).until(element_present)
        
        html_page = driver.find_element(By.XPATH, '//div[@class="col-md-11" and @id="report"]')
        text_list = html_page.text.split('\n')
    except (NoSuchElementException, TimeoutException):
        bypass_popup_window(driver)
        element_present = EC.element_to_be_clickable((By.ID, 'report'))
        WebDriverWait(driver, timeout).until(element_present)
        html_page = driver.find_element(By.ID, 'report')
        text_list = html_page.text.split('\n')

    title = driver.find_element(By.ID, 'set_title').text
    title_len = len(title)

    description = driver.find_element(By.ID, 'set_description').text
    description_len = len(description)

    keywords = driver.find_element(By.ID, 'set_keywords').text.split(',')

    h_titles_list = [text_list[9], text_list[10], text_list[11], text_list[12], text_list[13], text_list[14]]

    tech_errors = text_list[15]

    site_age = driver.find_element(By.ID, 'set_vozrast').text

    page_size = driver.find_element(By.ID, 'set_page_size').text

    page_speed = driver.find_element(By.ID, 'set_page_load_time').text

    ip_address = driver.find_element(By.ID, 'set_site_ip').text

    site_cost = driver.find_element(By.ID, 'set_site_cost').text

    yandex_indexing = driver.find_element(By.ID, 'set_pages_in_yandex').text

    yandex_iks = driver.find_element(By.ID, 'set_iks').text

    virus_filter = driver.find_element(By.ID, 'set_virus').text

    google_indexing = driver.find_element(By.ID, 'set_pages_in_google').text

    google_speed_page_desktop = driver.find_element(By.ID, 'set_google_speed_desktop').text

    google_speed_page_mobile = driver.find_element(By.ID, 'set_google_speed_mobile').text

    megaindex_trust_rank = driver.find_element(By.ID, 'set_trust_rank').text
    megaindex_domain_rank = driver.find_element(By.ID, 'set_domain_rank').text

    backlinks_total = driver.find_element(By.ID, 'set_backlinks_total').text.split('\n')
    unique_links = backlinks_total[1]
    domains = backlinks_total[3]
    ip_addresses_list = backlinks_total[5]
    subnetworks = backlinks_total[7]

    mobile_friendly_test = driver.find_element(By.ID, 'set_google_mobile_friendly').get_attribute('outerHTML')
    if 'fa fa-check text-success' in mobile_friendly_test:
        mobile_friendly_test = 'Пройден'
    else:
        mobile_friendly_test = 'Не пройден'

    tag_viewport = driver.find_element(By.ID, 'set_viewport').get_attribute('outerHTML')
    if 'fa fa-check text-success' in tag_viewport:
        tag_viewport = 'Указан'
    else:
        tag_viewport = 'Нет'
        
    flash_elements = driver.find_element(By.ID, 'set_adobe_flash').get_attribute('outerHTML')
    if 'fa fa-check text-success' in flash_elements:
        flash_elements = 'Flash элементов нет'
    else:
        flash_elements = 'Flash элементы есть'

    java_applets = driver.find_element(By.ID, 'set_adobe_flash').get_attribute('outerHTML')
    if 'fa fa-check text-success' in java_applets:
        java_applets = 'Java апплетов нет'
    else:
        java_applets = 'Java апплеты есть'

    silverlight_plugins = driver.find_element(By.ID, 'set_silverlight').get_attribute('outerHTML')
    if 'fa fa-check text-success' in silverlight_plugins:
        silverlight_plugins = 'Silverlight плагинов нет'
    else:
        silverlight_plugins = 'Silverlight плагины есть'

    if 'Главная страница не соответствует требованиям AMP!' in driver.find_element(By.ID, 'set_amp').get_attribute('outerHTML'):
        amp_check = 'Главная страница не соответствует требованиям AMP'
    else:
        amp_check = 'Главная страница соответствует требованиям AMP'

    page_encoding = driver.find_element(By.ID, 'set_charset').text
    robots_file = driver.find_element(By.ID, 'set_robots').text
    sitemap_file = driver.find_element(By.ID, 'set_sitemap').text
    iframe_count = driver.find_element(By.ID, 'set_iframe_count').text

    html_errors = driver.find_element(By.ID, 'set_html_errors').text
    css_errors = driver.find_element(By.ID, 'set_css_errors').text
    
    try:
        if driver.find_element(By.XPATH, '//*[@class="fa fa-fw fa-youtube"]').get_attribute('href') != None or driver.find_element(By.LINK_TEXT, 'youtube.com').get_attribute('href') != None:
            youtube_link = driver.find_element(By.LINK_TEXT, 'youtube.com').get_attribute('href')
        
    except NoSuchElementException:
        youtube_link = 'Отсутствует'
         
    try:
        if driver.find_element(By.XPATH, '//*[@class="fa fa-fw fa-vk"]').get_attribute('href') != None or driver.find_element(By.LINK_TEXT, 'vk.com').get_attribute('href') != None:
            vk_link = driver.find_element(By.LINK_TEXT, 'vk.com').get_attribute('href')
        
    except NoSuchElementException: 
        vk_link = 'Отсутствует'   
    
    try:
        if driver.find_element(By.XPATH, '//*[@class="fa fa-fw fa-facebook"]').get_attribute('href') != None or driver.find_element(By.LINK_TEXT, 'facebook.com').get_attribute('href') != None:
            facebook_link = driver.find_element(By.LINK_TEXT, 'facebook.com').get_attribute('href')
        
    except NoSuchElementException:
        facebook_link = 'Отсутствует' 

    try:
        if driver.find_element(By.XPATH, '//*[@class="fa fa-fw fa-instagram"]').get_attribute('href') != None or driver.find_element(By.LINK_TEXT, 'instagram.com').get_attribute('href') != None:
            instagram_link = driver.find_element(By.LINK_TEXT, 'instagram.com').get_attribute('href')
    except NoSuchElementException:
        instagram_link = 'Отсутствует'  
        
    try:
        if driver.find_element(By.XPATH, '//*[@class="fa fa-fw fa-twitter"]').get_attribute('href') != None or driver.find_element(By.LINK_TEXT, 'twitter.com').get_attribute('href') != None:
            twitter_link = driver.find_element(By.LINK_TEXT, 'twitter.com').get_attribute('href')
    except NoSuchElementException:
        twitter_link = 'Отсутствует'  
    
    try:
        if driver.find_element(By.XPATH, '//*[@class="fa fa-fw fa-telegram"]').get_attribute('href') != None or driver.find_element(By.LINK_TEXT, 'telegram.com').get_attribute('href') != None:
            telegram_link = driver.find_element(By.LINK_TEXT, 'telegram.com').get_attribute('href')
    except NoSuchElementException:
        telegram_link = 'Отсутствует'
               
    row_list = [site, title, title_len, description, description_len, keywords, h_titles_list, 
                tech_errors, site_age, page_size, page_speed, ip_address, site_cost, yandex_indexing, 
                yandex_iks, virus_filter, google_indexing, google_speed_page_desktop, google_speed_page_mobile, 
                megaindex_trust_rank, megaindex_domain_rank, unique_links, domains, ip_addresses_list, subnetworks,
                mobile_friendly_test, tag_viewport, flash_elements, java_applets, silverlight_plugins, amp_check, 
                page_encoding, robots_file, sitemap_file, iframe_count, html_errors, css_errors, youtube_link, 
                vk_link, facebook_link, instagram_link, twitter_link, telegram_link]
    
    pickle.dump(driver.get_cookies(), open("cookies.pkl","wb"))
    
    
    return row_list


# sites_to_parse = ['https://toruda.ru/', 'https://det-ploshadka.ru/', 'https://hoff.ru/', 'https://zaborkin.ru/', 
#                   'https://www.livemaster.ru/','https://www.livemaster.ru/', 'https://besedkis.ru/', 'https://hozotdel.ru/', 
#                   'https://www.detmir.ru/', 'https://www.profpokritie.com/']
while True:
    try:
        file_path = str(input('Введите полный путь до txt файла, содержащего ссылки на сайты: '))
        with open(file_path) as f:
            sites_to_parse = f.read().splitlines()
            break
    except:
        print('Неверно указан путь до файла.')
        pass

for i in range(len(sites_to_parse)):
    sites_to_parse[i] = sites_to_parse[i].replace(' ', '')
    sites_to_parse[i] = sites_to_parse[i].replace('\xa0', '')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                        options=chrome_options, 
                        service_log_path='NULL') 
cookies = load_cookies()
driver.get('https://be1.ru/')
if cookies != None:
    add_cookies(cookies, driver)
driver.refresh()

for i in range(len(sites_to_parse)):
    df.loc[i] = testing(sites_to_parse[i])

df.to_excel('test_result be1pars 11.07.xlsx')

driver.close()

x = 0