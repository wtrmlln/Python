from collections import Counter
from nltk.corpus import stopwords
import re
import string
import tkinter
import sys
from tkinter.filedialog import askopenfilenames
from pymorphy2 import MorphAnalyzer

def choose_files():
    tkinter_root = tkinter.Tk()
    tkinter_root.wm_withdraw()
    while True:
        try:
            filenames = askopenfilenames(title='Автозагрузка',  filetypes=(("txt files", "*.txt"),))
        except:
            print('Неизвестная ошибка при выборе файла')
            sys.exit()
        finally:
            if not filenames:
                print('Файл не выбран')
                continue
            tkinter_root.destroy()
            break
    return filenames

def lemmatize(text, morph):
    lemmatized_text = []
    for token in text:
        token = token.strip()
        token = morph.parse(token)[0]
        token = token.normal_form
        if len(token) > 0:
            lemmatized_text.append(token)
        else:
            pass
    return lemmatized_text

def lowering_text(text):
    return text.lower()

# Удаляем знаки препинания
def remove_punctiation(text):
    text = re.sub(r'[^\w\s]',' ', text)
    return text.replace('  ', ' ')

# Считаем частоту слов без стоп-слов
def calc_occurences(text):
    cleared_text = [word for word in text.split(' ') if word not in stopwords]
    return Counter(cleared_text)

# Считаем классическую тошноту ✔✔✔✔✔
def calc_classic_sickness(occurences_dict):
    return round(occurences_dict.most_common(1)[0][1] ** 0.5, 4)

def calc_academic_sickness(text):
    '''
    X = 100*Y/Z, 
    где Y — количество вхождений, 
    Z — объем текста.
    '''
    text = [word for word in text.split(' ') if word not in stopwords]
    occurences_dict = Counter(text)
    return occurences_dict.most_common(2)[0][1] * 1000 / len(''.join(text))
    #return (100 * occurences_dict.most_common(2)[0][1]) / len(text)

# Считаем количество символов в тексте ✔✔✔✔✔
def calc_symbols(text):
    return len(text)

# Считаем количество символов без пробелов ✔✔✔✔✔
def calc_symbols_without_spaces(text):
    return len(text.replace(" ", ""))

# Считаем количество слов
def calc_words(text):
    return len(text.split(' '))

# Считаем количество уникальных слов ✔✔✔✔✔
def calc_unique_words(text, morph):
    text = text.split(' ')
    text = lemmatize(text, morph)
    
    return len(Counter(text))

# Считаем количество стоп-слов
def calc_stopwords(text):
    stopwords_list = [word for word in text.split(' ') if word in stopwords]
    return len(stopwords_list)

# Удаляем цифры из текста
def remove_digits(text):
    dict_table = str.maketrans('', '', string.digits)
    text = text.translate(dict_table)
    text = text.replace('  ', ' ')
    return text

def main():
    morph = MorphAnalyzer()

    text_filename = choose_files()
    with open(text_filename) as f:
        text = f.read().strip()

    stopwords = set(stopwords.words('russian'))
    symbols = calc_symbols(text) # ✔✔✔✔✔
    symbols_without_spaces = calc_symbols_without_spaces(text) # ✔✔✔✔✔

    text = lowering_text(text)
    text = remove_punctiation(text)
    text = remove_digits(text)

    words = calc_words(text) # ✔✔✔✔✔
    unique_words = calc_unique_words(text, morph) # ✔✔✔✔✔
    stopwords_len = calc_stopwords(text) # ✔✔✔✔✔

    occurences_dict = calc_occurences(text) # ✔✔✔✔✔

    classic_sickness = calc_classic_sickness(occurences_dict) # ✔✔✔✔✔
    academic_sickness = calc_academic_sickness(text) # XXXXX

if __name__ == '__main__':
    main()