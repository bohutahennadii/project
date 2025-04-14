import streamlit as st
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import csv
from langdetect import detect

def dictionaries(string):
    dict = {'Військово-політичне керівництво України всіх рівнів':0,'Правоохоронні органи України':1,'Збройні сили України':2,
                                       'Соціально-політична ситуація в регіонах України (відношення до мобілізації, соціально-економічна стабільність тощо)':3,'Проросійські релігійні організації на території України':4,
                                       'Проросійські рухи, формування концепції «руського миру»':5,'Міжнародний імідж України в ЄС (англійська, німецька, польська, румунська, французька, угорська, українська, російська мови)':6,
                                       'Міжнародний імідж України в США, Канаді та Великобританії (англійська мова)':7,'Міжнародний імідж України в країнах Африки (англійська, французька арабська мови)':8,
                                       'Міжнародний імідж України в країнах Азії (російська, китайська, турецька, арабська, грузинська, казахська, фарсі, киргизька, таджицька, узбецька, японська, корейська мови)':9,
                                       'Україна в інформаційному просторі російської федерації':10,'Україна в інформаційному просторі республіки білорусь':11,
                                       'Соціально-економічна, політична, військова ситуація в російській федерації (відношення до вищого керівництва, мобілізації, погіршення економічного становища тощо)':12}
    key = dict.get(string) + 1
    return key

def get_articles(string):
    art = {'Конституція України, частина четверта статті 32':0, 'Цивільний кодекс України, стаття 278':1, 'Закон України "Про телебачення і радіомовлення", стаття 7':2, 
                                               'Закон України "Про друковані засоби масової інформації (пресу) в Україні", статті 3, 18':3, 'Кодекс України про адміністративні правопорушення, стаття 173-1':4,
                                               'Кримінальний кодекс України, стаття 109':5, 'Кримінальний кодекс України, стаття 259':6, 'Кримінальний кодекс України, стаття 182':7,
                                               'Кримінальний кодекс України, стаття 168':8, 'Кримінальний кодекс України Стаття 232. Розголошення комерційної або банківської таємниці':9,
                                               'Кримінальний кодекс України Стаття 161. Порушення рівноправності громадян залежно від їх расової, національної належності, релігійних переконань, інвалідності та за іншими ознаками':10,
                                               'Закон України «Про медіа» Стаття 36. Обмеження щодо змісту інформації':11}
    key = art.get(string) + 1
    return key

def fetch_news(url):
    response = requests.get(url)

    # Перевірте статус відповіді; 200 означає, що все гаразд
    if response.status_code != 200:
        print(f'Failed to retrieve the page with status code: {response.status_code}')
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Збір новин
    text = []
    final_text = ""
    for article in soup.find_all('p'):
        headline_text = article.text.strip()
        if headline_text:  # Перевірка на наявність тексту
            text.append(headline_text)
    for i in range(len(text)):
        final_text = final_text + text[i] + '\n'
    
            
    return final_text

def show_keys(key):
    string = 'keywords/keywords_' + str(key) + '.csv'

    data = []

    with open(string, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
    # Читання кожного рядка з CSV-файлу
        for row in reader:
            data=",".join(row)  # Виведення тексту з рядка

    data = data.split(',')

    return data

def show_articles(key):
    string = 'articles/articles_' + str(key) + '.csv'

    data = []

    with open(string, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
    # Читання кожного рядка з CSV-файлу
        for row in reader:
            data=",".join(row)  # Виведення тексту з рядка

    data = data.split(',')

    return data

def show_dict_positive(key):
    string = 'dictionaries/positive/dict_' + str(key) + '.csv'

    with open(string, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
    # Читання кожного рядка з CSV-файлу
        for row in reader:
            data=",".join(row)  # Виведення тексту з рядка

    data = data.split(',')

    return data

def show_dict_negative(key):
    string = 'dictionaries/negative/dict_' + str(key) + '.csv'

    with open(string, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
    # Читання кожного рядка з CSV-файлу
        for row in reader:
            data=",".join(row)  # Виведення тексту з рядка

    data = data.split(',')

    return data

def save_dict(key, text, type):
    if type == "Positive":
        string = 'dictionaries/positive/dict_' + str(key) + '.csv'
    else:
        string = 'dictionaries/negative/dict_' + str(key) + '.csv'

    with open(string, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        writer.writerows([text])

def update_dict(key, string, type):
    if type == "Positive":
        data = show_dict_positive(key)
    else:
        data = show_dict_negative(key)

    data.append(string)

    save_dict(key, data, type)

    st.sidebar.write(data)

def remove_dict(key, string, type):
    if type == "Positive":
        data = show_dict_positive(key)
    else:
        data = show_dict_negative(key)

    data.remove(string)

    save_dict(key, data, type)

    st.sidebar.write(data)

def update_key(key, string):
    data = show_keys(key)

    data.append(string)

    save_keys(key, data)

    st.sidebar.write(data)

def update_articles(key, string):
    data = show_articles(key)

    data.append(string)

    save_articles(key, data)

    st.sidebar.write(data)

def remove_key(key, string):
    data = show_keys(key)

    data.remove(string)

    save_keys(key, data)

    st.sidebar.write(data)

def remove_articles(key, string):
    data = show_articles(key)

    data.remove(string)

    save_articles(key, data)

    st.sidebar.write(data)

def save_keys(key, text):
    string = 'keywords/keywords_' + str(key) + '.csv'

    with open(string, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        writer.writerows([text])

def save_articles(key, text):
    string = 'articles/articles_' + str(key) + '.csv'

    with open(string, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        writer.writerows([text])

def check_dict(text):
    dict = ['Військово-політичне керівництво України всіх рівнів','Правоохоронні органи України','Збройні сили України',
                                       'Соціально-політична ситуація в регіонах України (відношення до мобілізації, соціально-економічна стабільність тощо)','Проросійські релігійні організації на території України',
                                       'Проросійські рухи, формування концепції «руського миру»','Міжнародний імідж України в ЄС (англійська, німецька, польська, румунська, французька, угорська, українська, російська мови)',
                                       'Міжнародний імідж України в США, Канаді та Великобританії (англійська мова)','Міжнародний імідж України в країнах Африки (англійська, французька арабська мови)',
                                       'Міжнародний імідж України в країнах Азії (російська, китайська, турецька, арабська, грузинська, казахська, фарсі, киргизька, таджицька, узбецька, японська, корейська мови)',
                                       'Україна в інформаційному просторі російської федерації','Україна в інформаційному просторі республіки білорусь',
                                       'Соціально-економічна, політична, військова ситуація в російській федерації (відношення до вищого керівництва, мобілізації, погіршення економічного становища тощо)']
    result = []
    for i in range(13):
        keys = show_keys(i + 1)
        text = str.lower(text)

        for i in range(len(keys)):
            keys[i] = str.lower(keys[i])
        
        nums = 0

        for i in range(len(keys)):
            if keys[i] in text:
                nums += 1
        
        result.append(nums)
    
    max_ind = result.index(max(result))
    return dict[max_ind]

def check_articles(text):
    art = ['Конституція України, частина четверта статті 32', 'Цивільний кодекс України, стаття 278', 'Закон України "Про телебачення і радіомовлення", стаття 7', 
                                               'Закон України "Про друковані засоби масової інформації (пресу) в Україні", статті 3, 18', 'Кодекс України про адміністративні правопорушення, стаття 173-1',
                                               'Кримінальний кодекс України, стаття 109', 'Кримінальний кодекс України, стаття 259', 'Кримінальний кодекс України, стаття 182',
                                               'Кримінальний кодекс України, стаття 168', 'Кримінальний кодекс України Стаття 232. Розголошення комерційної або банківської таємниці',
                                               'Кримінальний кодекс України Стаття 161. Порушення рівноправності громадян залежно від їх расової, національної належності, релігійних переконань, інвалідності та за іншими ознаками',
                                               'Закон України «Про медіа» Стаття 36. Обмеження щодо змісту інформації']
    result = []
    for i in range(12):
        keys = show_articles(i + 1)
        text = str.lower(text)

        for i in range(len(keys)):
            keys[i] = str.lower(keys[i])

        nums = 0

        for i in range(len(keys)):
            if keys[i] in text:
                nums += 1
        
        result.append(nums)

    if max(result) >= 5:
        max_ind = result.index(max(result))
    else:
        return 'Не зайдено'

    return art[max_ind]

def ton_check(text, main_key, check):
    text = str.lower(text)

    key = dictionaries(main_key)
    
    positive = show_dict_positive(key)
    negative = show_dict_negative(key)
    
    for i in range(len(positive)):
        positive[i] = str.lower(positive[i])

    for i in range(len(negative)):
        negative[i] = str.lower(negative[i])
    
    pos_nums = 0

    neg_nums = 0

    for i in range(len(positive)):
        if positive[i] in text:
            pos_nums += 1

    for i in range(len(negative)):
        if negative[i] in text:
            neg_nums += 1

    result = (pos_nums - neg_nums) * 10
    
    if result > 100:
        result = 100
    elif result < -100:
        result = -100
    
    if check:
        result *= -1

    return result

def split_text(text, max_length=5000):
    parts = []
    while len(text) > max_length:
        split_index = text[:max_length].rfind(' ')
        if split_index == -1:
            split_index = max_length
        parts.append(text[:split_index])
        text = text[split_index:].lstrip()
    parts.append(text)
    return parts

def translate(text):
    detected_lang = detect(text)

    lang = 0

    if detected_lang == 'uk':
        lang = 1
        return text, lang

    translator = GoogleTranslator(source='auto', target='uk')

    text_parts = split_text(text)

    translated_parts = [translator.translate(part) for part in text_parts]

    return " ".join(translated_parts), lang