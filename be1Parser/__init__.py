from credentials import arsenkin_login, arsenkin_password, google_api_key

import pickle
import pandas as pd
import requests
import tqdm
import os
from datetime import datetime

from io import StringIO
from multiprocessing.dummy import Pool as ThreadPool
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

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

def find_social_link(social_network):
    try:
        if driver.find_element(By.XPATH, '//*[@class="fa fa-fw fa-' + social_network + '"]').get_attribute('href') != None or driver.find_element(By.LINK_TEXT, social_network + '.com').get_attribute('href') != None:
            return driver.find_element(By.LINK_TEXT, social_network + '.com').get_attribute('href')
    except NoSuchElementException:
        return 'Отсутствует'

def be1_parsing(site):
    
    timeout = 15
    
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
        captcha_element = EC.presence_of_element_located((By.ID, 'recaptcha'))
        WebDriverWait(driver, timeout=2).until(captcha_element)
        WebDriverWait(driver, timeout=recaptcha_timeout).until_not(captcha_element)
    finally:
        pass
       
    try:
        # Вытягиваем всю страницу HTML с отчетом
        bypass_popup_window(driver)
        element_present = EC.element_to_be_clickable((By.XPATH, '//div[@class="col-md-11" and @id="report"]'))
        WebDriverWait(driver, timeout=timeout).until(element_present)
        
        html_page = driver.find_element(By.XPATH, '//div[@class="col-md-11" and @id="report"]')
        text_list = html_page.text.split('\n')
    except (NoSuchElementException, TimeoutException):
        bypass_popup_window(driver)
        element_present = EC.element_to_be_clickable((By.ID, 'report'))
        WebDriverWait(driver, timeout=timeout).until(element_present)
        html_page = driver.find_element(By.ID, 'report')
        text_list = html_page.text.split('\n')

    title = driver.find_element(By.ID, 'set_title').text
    title_len = len(title)

    description = driver.find_element(By.ID, 'set_description').text
    description_len = len(description)

    keywords = driver.find_element(By.ID, 'set_keywords').text.split(',')

    h_titles_list = [text_list[9], text_list[10], text_list[11], text_list[12], text_list[13], text_list[14]]

    tech_errors = text_list[15]

    site_age_whois = driver.find_element(By.ID, 'set_vozrast').text

    page_size = driver.find_element(By.ID, 'set_page_size').text

    page_speed = driver.find_element(By.ID, 'set_page_load_time').text

    ip_address = driver.find_element(By.ID, 'set_site_ip').text

    site_cost = driver.find_element(By.ID, 'set_site_cost').text

    yandex_indexing = driver.find_element(By.ID, 'set_pages_in_yandex').text

    yandex_iks = driver.find_element(By.ID, 'set_iks').text

    virus_filter = driver.find_element(By.ID, 'set_virus').text

    google_indexing = driver.find_element(By.ID, 'set_pages_in_google').text

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
        
    youtube_link = find_social_link('youtube')
    vk_link = find_social_link('vk')
    facebook_link = find_social_link('facebook')
    instagram_link = find_social_link('instagram')
    twitter_link = find_social_link('twitter')
    telegram_link = find_social_link('telegram')

    row_list = [site, title, title_len, description, description_len, keywords, h_titles_list, 
                tech_errors, site_age_whois, page_size, page_speed, ip_address, site_cost, yandex_indexing, 
                yandex_iks, virus_filter, google_indexing, megaindex_trust_rank, megaindex_domain_rank, 
                unique_links, domains, ip_addresses_list, subnetworks,mobile_friendly_test, tag_viewport, 
                flash_elements, java_applets, silverlight_plugins, amp_check, page_encoding, robots_file, 
                sitemap_file, iframe_count, html_errors, css_errors, youtube_link, 
                vk_link, facebook_link, instagram_link, twitter_link, telegram_link]
    
    pickle.dump(driver.get_cookies(), open("cookies.pkl","wb"))

    return row_list

def parse_site_age_be1(sites_to_parse):

    cookies = load_cookies()

    if cookies != None:
        add_cookies(cookies, driver)
    driver.refresh()
    
    driver.get('https://be1.ru/vozrast-stranicy/')
    
    text_form = driver.find_element(By.XPATH, '//textarea[@name="links" and @class="form-control"]')
    text_form.send_keys('\n'.join(sites_to_parse))
    
    check_button = driver.find_element(By.ID, 'tool-form-btn')
    check_button.click()
    
    table_present = EC.presence_of_element_located((By.XPATH, '//table[@class="table table-fixed table-bordered table-headed sortable"]'))
    WebDriverWait(driver, timeout=100).until(table_present)
    
    sites_age_table_be1 = pd.read_html(driver.find_element(By.XPATH, '//table[@class="table table-fixed table-bordered table-headed sortable"]').get_attribute('outerHTML'))[0]
    
    sites_age_table_be1 = sites_age_table_be1.rename({'URL': 'Сайт', 'Возраст страницы': 'Возраст be1'}, axis=1)
    
    return sites_age_table_be1

def parse_site_age_arsenkin(sites_to_parse):
    
    driver.get('https://arsenkin.ru/tools/login/')
    
    email = driver.find_element(By.NAME, 'email')
    email.send_keys(arsenkin_login) 
    password = driver.find_element(By.NAME, 'password')
    password.send_keys(arsenkin_password)

    button_in = driver.find_element(By.XPATH, '//input[@type="submit" and @value="Войти"]')
    button_in.click()

    driver.get('https://arsenkin.ru/tools/whois/')
    
    form_control = driver.find_element(By.XPATH, '//textarea[@name="urls" and @class="form-control"]')
    form_control.send_keys('\n'.join(sites_to_parse[:500]))

    show_button = driver.find_element(By.ID, 'ok')
    WebDriverWait(driver, timeout=5).until(EC.element_to_be_clickable((By.ID, 'ok')))
    show_button.click()
    WebDriverWait(driver, timeout=100).until(EC.presence_of_element_located((By.XPATH, '//table[@class="table table-striped"]')))
    sites_age_table_arsenkin = pd.read_html(driver.find_element(By.XPATH, '//table[@class="table table-striped"]').get_attribute('outerHTML'))[0]
    sites_age_table_arsenkin['Домен'] = sites_to_parse
    sites_age_table_arsenkin['Возраст'] = (pd.Timestamp('today') - pd.to_datetime(sites_age_table_arsenkin['Дата регистрации'], infer_datetime_format=True)).dt.days
    sites_age_table_arsenkin = sites_age_table_arsenkin[['Домен', 'Возраст']]
    sites_age_table_arsenkin = sites_age_table_arsenkin.rename({'Домен': 'Сайт', 'Возраст': 'Возраст страницы ARSENKIN'}, axis=1)
    return sites_age_table_arsenkin
    
def parse_google_speed(site_list):
    site = site_list[0]
    strategy = site_list[1]
    
    url = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'

    params_dict = {'url': site, 'key': google_api_key, 'strategy': strategy}
    
    try:
        response = requests.get(url, params=params_dict)
        df = pd.read_json(StringIO(response.text))
        google_speed_page = df['lighthouseResult']['categories']['performance']['score']
    except:
        google_speed_page = None
    return [site, strategy, google_speed_page]

def get_sites_to_parse():
    while True:
        try:
            file_path = str(input('Введите полный путь до txt файла, содержащего ссылки на сайты: '))
            with open(file_path) as f:
                sites_to_parse = f.read().splitlines()
                for i in range(len(sites_to_parse)):
                    sites_to_parse[i] = sites_to_parse[i].replace(' ', '')
                    sites_to_parse[i] = sites_to_parse[i].replace('\xa0', '')
                sites_to_parse = [site.strip() for site in sites_to_parse if site.strip()]
                return sites_to_parse
        except:
            print('Неверно указан путь до файла.')
            pass

def main():

    sites_to_parse = get_sites_to_parse()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    global driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                            options=chrome_options, 
                            service_log_path='NULL') 

    be1_results_list = []
    for site in sites_to_parse:
        be1_results_list.append(be1_parsing(site))
    df = pd.DataFrame(be1_results_list, columns=['Сайт', "Тайтл", "Длина тайтла", "Декскрипшен", "Длина дескрипшена", 
                                                "Ключевые слова", "Заголовки", "Технические ошибки", "Возраст сайта (WHOIS)", 
                                                "Размер страницы", "Скорость загрузки", "IP адрес", "Стоимость сайта", 
                                                "Проиндексировано в Яндекс", "Яндекс ИКС", "Фильтр за вирусы в Яндекс", 
                                                "Проиндексировано в Гугл",  "Megaindex Trust Rank", "Megaaindex Domain Rank", 
                                                "Уникальные ссылки", "Домены", "IP адреса", "Подсети", "Mobile Friendly Test", 
                                                "Тег viewport", "Flash элементы", "Java апплеты", "Silverlight плагины", "Проверка на AMP", 
                                                "Кодировка", "Robots.txt", "Sitemap.xml", "iframe на страницы", "Ошибки валидности HTML", 
                                                "Ошибки валидности CSS", "Youtube", "VK", "Facebook", "Instagram", "Twitter", "Telegram"])

    sites_age_table_be1 = parse_site_age_be1(sites_to_parse)
    sites_age_table_arsenkin = parse_site_age_arsenkin(sites_to_parse)

    driver.close()

    sites_for_pageinsights = []
    for site in sites_to_parse:
        for i in range(0, 2):
            if i == 0:
                strategy = 'desktop'
            else:
                strategy = 'mobile'
            sites_for_pageinsights.append([site, strategy])
    pool = ThreadPool(len(sites_to_parse))
    speed_results_list = list(tqdm.tqdm(pool.imap_unordered(parse_google_speed, sites_for_pageinsights), total=len(sites_for_pageinsights), desc='Парсинг PageSpeed Insights Google'))

    desktop_dict = {}
    mobile_dict = {}
    for i in range(len(speed_results_list)):
        if speed_results_list[i][1] == 'desktop':
            desktop_dict[speed_results_list[i][0]] = speed_results_list[i][2]
        elif speed_results_list[i][1] == 'mobile':
            mobile_dict[speed_results_list[i][0]] = speed_results_list[i][2]
            
    df['Скорость загрузки desktop'] = df['Сайт'].map(desktop_dict)
    df['Скорость загрузки mobile'] = df['Сайт'].map(mobile_dict)

    df = pd.merge(df, sites_age_table_be1[['Сайт', 'Возраст страницы be1']], on='Сайт')
    df = pd.merge(df, sites_age_table_arsenkin[['Сайт', 'Возраст страницы ARSENKIN']], on='Сайт')

    path_to_save = 'C:\\Users\\' + os.getlogin() + '\\Desktop\\Результаты be1 парсинга\\'

    try:
        os.makedirs(path_to_save)
    except FileExistsError:
        pass

    i = 0
    while os.path.exists(path_to_save):
        try:
            df.to_excel(path_to_save + 'be1 parsed file ' + datetime.today().strftime('%Y-%m-%d') + ' - ' + str(i) + '.xlsx')
            break
        except:
            i += 1
            pass
        
if __name__ == '__main__':
    main()