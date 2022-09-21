import pandas as pd
import requests
import re
from multiprocessing.dummy import Pool as ThreadPool
import tqdm
import os
from datetime import datetime

def main():

    urls_to_parse = pd.read_csv(input('Введите путь до файла csv формата, содержащего URL ссылки для парсинга Title: '), squeeze=True, error_bad_lines=False, encoding='utf-8').tolist()
    path_to_save = 'C:\\Users\\' + os.getlogin() + '\\Desktop\\Результаты Title парсинга\\'
    titles_list = []
    
    def parse_title(url):

        try:
            r = requests.get(url, timeout=5)
            html = r.text
            html_title = re.search('<\W*title\W*(.*)</title', html, re.IGNORECASE)
            if html_title == None:
                return None
            else:
                return html_title.group(1)
        except requests.exceptions.RequestException as e:
            return None

    pool = ThreadPool(1024)

    titles_list = list(tqdm.tqdm(pool.imap_unordered(parse_title, urls_to_parse), total=len(urls_to_parse)))
    titles_df = pd.DataFrame({'title':titles_list})
    
    try:
        os.makedirs(path_to_save)
    except FileExistsError:
        pass
    
    i = 0
    while os.path.exists(path_to_save): 
        try:
            titles_df.to_csv(path_to_save + 'parsed_titles' + datetime.now().strftime('%Y-%m-%d') + '.csv')
            break
        except:
            i += 1
            pass
    
if __name__ == '__main__':
    main()

