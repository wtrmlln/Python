from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from lxml import etree
import pandas as pd
from time import sleep

def multiple_dfs(df_list, sheet_name, file_name, spaces):
    writer = pd.ExcelWriter(file_name,engine='xlsxwriter')   
    row = 0
    for dataframe in df_list:
        dataframe.to_excel(writer,sheet_name=sheet_name,startrow=row , startcol=0)   
        row = row + len(dataframe.index) + spaces + 1
    writer.save()

def testing(text, sheet_name):

    driver.get('https://advego.com/text/seo/')
    
    sleep(5)
    
    text_box =  driver.find_element(By.ID, 'job_text_seo')
    text_box.send_keys(text)

    check_button = driver.find_element(By.LINK_TEXT, 'Проверить')
    check_button.click()

    while True:
        try:
            driver.find_element(By.ID, 'service_busy')
            
            sleep(10)
            
            driver.get('https://advego.com/text/seo/')
            text_box =  driver.find_element(By.ID, 'job_text_seo')
            text_box.send_keys(text)

            check_button = driver.find_element(By.LINK_TEXT, 'Проверить')
            check_button.click()
        except:
            break

    timeout = 5
    element_present = EC.element_to_be_clickable((By.XPATH, "//div[@id='text_check_results_form' and h3[contains(text(),'Статистика текста')]]"))
    WebDriverWait(driver, timeout).until(element_present)

    html_table = driver.find_element(By.XPATH, "//div[@id='text_check_results_form' and h3[contains(text(),'Статистика текста')]]").get_attribute('innerHTML')

    tables_indexes = [2, 4, 6, 8]
    tables_list = []

    for index in tables_indexes:
        tables_list.append(pd.read_html(html_table.split('h3')[index])[0])
        
    # run function
    multiple_dfs(tables_list, sheet_name, 'test1.xlsx', 1)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                        options=chrome_options, 
                        service_log_path='NULL') 

texts_list = ['Она подошла к окну, взяла цветочный горшок, обернулась ко мне. Я никогда не видел ее такой счастливой. Глаза одновременно наполнялись слезами и так глубоко сияли, что я понял: у нее случилось что-то очень важное. Тонкие руки бережно держали горшок с невзрачным растением. Казалось, она не дышит, чтобы не потревожить свое сокровище.',
              'Рассказывают, что древние греки очень любили виноград и после его сбора устраивали праздник в честь бога винограда Диониса. Свиту Диониса составляли козлоногие существа — сатиры. Изображая их, эллины надевали козлиные шкуры, бешено скакали и пели — словом, самозабвенно предавались веселью. Такие представления назывались трагедиями, что по-древнегречески означало «пение козлов».',
              'Правда, иногда появлялся «бог из машины» (машиной называли специальный кран, на котором «бога» опускали на сцену) и нежданно- негаданно спасал героя. Был ли это действительно настоящий бог или всё-таки актер — неясно до сих пор, но зато доподлинно известно, что и слово «машина», и театральные краны были придуманы в Древней Греции.']
sheet_names_list = []

for j in range(1, 5):
    for i in range(len(texts_list)):
        sheet_names_list.append('Текст №'+str(i))
        testing(texts_list[i], sheet_names_list[i])

