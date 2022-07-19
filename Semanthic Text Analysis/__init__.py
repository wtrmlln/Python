from collections import Counter
from tkinter import Text
from nltk.corpus import stopwords
import re
import string
import pymorphy2
from pymorphy2 import MorphAnalyzer

morph = MorphAnalyzer()

text_test = 'Наши пончо – самые что ни на есть пончо! Они пошиты из шкур элитных кракозябр и подвергнуты трехступенчатой сертификации качества. Кроме того, у Вашего любимца ни за что не возникнет аллергия, поскольку все пончо гипоаллергенны и безопасны для здоровья людей и животных. В каталоге представлены модели всевозможных расцветок и фасонов. Недавно поступили пончо из новой коллекции: торопитесь сделать покупку по выгодной цене!'
stopwords = set(stopwords.words('russian'))

def lemmatize(text):
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
def calc_unique_words(text):
    text = text.split(' ')
    text = lemmatize(text)
    
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

symbols = calc_symbols(text_test) # ✔✔✔✔✔
symbols_without_spaces = calc_symbols_without_spaces(text_test) # ✔✔✔✔✔

text_test = lowering_text(text_test)
text_test = remove_punctiation(text_test)
text_test = remove_digits(text_test)

words = calc_words(text_test) # ✔✔✔✔✔
unique_words = calc_unique_words(text_test) # ✔✔✔✔✔
stopwords_len = calc_stopwords(text_test) # ✔✔✔✔✔

occurences_dict = calc_occurences(text_test) # ✔✔✔✔✔

classic_sickness = calc_classic_sickness(occurences_dict) # ✔✔✔✔✔
academic_sickness = calc_academic_sickness(text_test) # XXXXX

x = 0