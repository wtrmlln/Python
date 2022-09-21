import tkinter
import os
import sys
import time
import pickle
from tkinter.filedialog import askopenfilenames
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from settings import CHROMEOPTIONS_ARGS

def choose_files():
    tkinter_root = tkinter.Tk()
    tkinter_root.wm_withdraw()
    while True:
        try:
            filenames = askopenfilenames(title='Автозагрузка',  initialdir=os.environ.get('PROGRUZKA'), filetypes=(("CSV Files","*.csv"),))
        except:
            print('Неизвестная ошибка при выборе файлов')
            sys.exit()
        finally:
            if not filenames:
                print('Файлы не выбраны')
                continue
            tkinter_root.destroy()
            break
    return filenames

def get_sitenames(filenames):
    site_names = []
    filenames_ostatki = []
    for filename in filenames:
        if 'Остатки' in filename:
            if 'компкресла' in filename:
                site_names.append('Компкресла')
                filenames_ostatki.append(filename)
            else:
                site_names.extend(['SOT', 'Торуда', 'ПМК'])
                filenames_ostatki.extend(filename for i in range(3))
    return site_names, filenames_ostatki

def initialize_chrome():
    #Инициализация Chrome
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    set_chrome_options(CHROMEOPTIONS_ARGS, chrome_options)
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager(log_level=0, print_first_line=False).install()), 
        options=chrome_options, 
        service_log_path='NULL')
    except WebDriverException:
        webdriver.Chrome(service=Service(ChromeDriverManager(log_level=0, print_first_line=False).install()), 
        options=chrome_options, 
        service_log_path='NULL').quit()
        raise
    except:   
        print('Не удалось инициализировать Webdriver Chrome')
        time.sleep(3)
        sys.exit()
    return driver

def set_chrome_options(args_list, chrome_options):
    for arg in args_list:
        chrome_options.add_argument(arg)

def load_cookies():
    try:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        return cookies
    except:
        cookies = None
        return cookies