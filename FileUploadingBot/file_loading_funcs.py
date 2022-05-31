from file_preparation_funcs import initialize_chrome, load_cookies
from file_processing_funcs import add_cookies, authorization, load_file

def price_loading(filename):
    driver = initialize_chrome()
    cookies = load_cookies()
    if 'Торуда' in filename:
        list_name_link = ['Торуда', 'https://toruda.ru/netcat/add.php?inside_admin=&catalogue=1&sub=3&cc=10004']
    elif 'ПМК' in filename:
        list_name_link = ['ПМК', 'https://prommashkomplekt.ru/netcat/add.php?catalogue=1&sub=3&cc=10004']
    elif 'DDI' in filename:
        list_name_link = ['DDI', 'https://d-d-i.ru/netcat/add.php?catalogue=1&sub=3&cc=10004']
    elif ' Н ' in filename:
        list_name_link = ['Компкресла', 'https://kompkresla.ru/netcat/?catalogue=2&sub=106&cc=9346']
    elif 'Кабинетоф' in filename:
        list_name_link = ['Кабинетоф', 'http://kabinetof.ru/netcat/?catalogue=1&sub=81&cc=4489&curPos=0']
    else:
        list_name_link = ['SOT', 'http://s-o-t.ru/netcat/add.php?catalogue=1&sub=3&cc=10004']

    site_name = list_name_link[0]
    driver.get(list_name_link[1])
    if cookies != None:
        add_cookies(cookies, driver, site_name)
    authorization(site_name, driver)
    load_file(filename, site_name, driver)

def stocks_loading(site_name, filename):
    #Инициализация Chrome
    if 'Торуда' in site_name:
        name_link = 'https://toruda.ru/netcat/add.php?inside_admin=&catalogue=1&sub=3&cc=1195760'
    elif 'ПМК' in site_name:
        name_link = 'https://prommashkomplekt.ru/netcat/add.php?catalogue=1&sub=3&cc=431514'
    elif 'Компкресла' in site_name:
        name_link = 'https://kompkresla.ru/netcat/?catalogue=2&sub=106&cc=11845'
    else:
        name_link = 'http://s-o-t.ru/netcat/add.php?catalogue=1&sub=3&cc=1195760'
    
    driver = initialize_chrome()
    cookies = load_cookies()
    driver.get(name_link)
    if cookies != None:
        add_cookies(cookies, driver, site_name)
        driver.refresh()
    authorization(site_name, driver)
    load_file(filename, site_name, driver)