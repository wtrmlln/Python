from file_preparation_funcs import initialize_chrome, load_cookies
from file_processing_funcs import add_cookies, authorization, load_file

def price_loading(filename):
    driver = initialize_chrome()
    cookies = load_cookies()
    #Поиск необходимого сайта    
    if 'Торуда' in filename:
        site_name = 'Торуда'
        #Авторизация
        driver.get('https://toruda.ru/netcat/add.php?inside_admin=&catalogue=1&sub=3&cc=10004')
        if cookies != None:
            add_cookies(cookies, driver, site_name)
        authorization(site_name, driver)
        load_file(filename, site_name, driver)
    elif 'ПМК' in filename:
        site_name = 'ПМК'
        #Авторизация
        driver.get('https://prommashkomplekt.ru/netcat/add.php?catalogue=1&sub=3&cc=10004')
        if cookies != None:
            add_cookies(cookies, driver, site_name)
        authorization(site_name, driver)
        load_file(filename, site_name, driver)
    elif 'DDI' in filename:
        site_name = 'DDI'
        #Авторизация
        driver.get('https://d-d-i.ru/netcat/add.php?catalogue=1&sub=3&cc=10004')
        if cookies != None:
            add_cookies(cookies, driver, site_name)
        authorization(site_name, driver)
        load_file(filename, site_name, driver)
    elif ' Н ' in filename:
        site_name = 'Компкресла'
        #Авторизация
        driver.get('https://kompkresla.ru/netcat/?catalogue=2&sub=106&cc=9346')
        if cookies != None:
            add_cookies(cookies, driver, site_name)
        authorization(site_name, driver)
        load_file(filename, site_name, driver)
    elif 'Кабинетоф' in filename:
        site_name = 'Кабинетоф'
        #Авторизация
        driver.get('http://kabinetof.ru/netcat/?catalogue=1&sub=81&cc=4489&curPos=0')
        if cookies != None:
            add_cookies(cookies, driver, site_name)
        authorization(site_name, driver)
        load_file(filename, site_name, driver)
    else:
        site_name = 'SOT'
        #Авторизация
        driver.get('http://s-o-t.ru/netcat/add.php?catalogue=1&sub=3&cc=10004')
        if cookies != None:
            add_cookies(cookies, driver, site_name)
        authorization(site_name, driver)
        load_file(filename, site_name, driver)

def stocks_loading(site_name, filename):
    #Инициализация Chrome
    driver = initialize_chrome()
    cookies = load_cookies()
    if 'Торуда' in site_name:
        driver.get('https://toruda.ru/netcat/add.php?inside_admin=&catalogue=1&sub=3&cc=1195760')
        if cookies != None:
            add_cookies(cookies, driver, site_name)
            driver.refresh()
        authorization(site_name, driver)
        load_file(filename, site_name, driver)
      
    elif 'ПМК' in site_name:
        driver.get('https://prommashkomplekt.ru/netcat/add.php?catalogue=1&sub=3&cc=431514')
        if cookies != None:
            add_cookies(cookies, driver, site_name)
        authorization(site_name, driver)
        load_file(filename, site_name, driver)

    elif 'Компкресла' in site_name:
        driver.get('https://kompkresla.ru/netcat/?catalogue=2&sub=106&cc=11845')
        if cookies != None:
            add_cookies(cookies, driver, site_name)
        authorization(site_name, driver)
        load_file(filename, site_name, driver)

    else:
        driver.get('http://s-o-t.ru/netcat/add.php?catalogue=1&sub=3&cc=1195760')
        if cookies != None:
            add_cookies(cookies, driver, site_name)
        authorization(site_name, driver)
        load_file(filename, site_name, driver)